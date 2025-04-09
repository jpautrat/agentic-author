"""Main class for generating books using AutoGen with improved iteration control"""
import autogen
from typing import Dict, List, Optional
import os
import time
import re
from research_agent import ResearchAgent

class BookGenerator:
    def __init__(self, agents: Dict[str, autogen.ConversableAgent], agent_config: Dict, outline: List[Dict]):
        """Initialize with outline to maintain chapter count context"""
        self.agents = agents
        self.agent_config = agent_config
        self.output_dir = "book_output"
        self.chapters_memory = []  # Store chapter summaries
        self.max_iterations = 3  # Limit editor-writer iterations
        self.outline = outline  # Store the outline
        self.research_agent = ResearchAgent()  # Initialize research agent
        self.book_settings = agent_config.get("book_settings", {})
        self.min_chapter_length = self.book_settings.get("min_chapter_length", 3000)  # Minimum words per chapter
        os.makedirs(self.output_dir, exist_ok=True)

    def _clean_chapter_content(self, content: str) -> str:
        """Clean up chapter content by removing artifacts and chapter numbers"""
        # Remove chapter number references
        content = re.sub(r'\*?\s*\(Chapter \d+.*?\)', '', content)
        content = re.sub(r'\*?\s*Chapter \d+.*?\n', '', content, count=1)

        # Clean up any remaining markdown artifacts
        content = content.replace('*', '')
        content = content.strip()

        return content


    def initiate_group_chat(self) -> autogen.GroupChat:
        """Create a new group chat for the agents with improved speaking order"""
        outline_context = "\n".join([
            f"\nChapter {ch['chapter_number']}: {ch['title']}\n{ch['prompt']}"
            for ch in sorted(self.outline, key=lambda x: x['chapter_number'])
        ])

        messages = [{
            "role": "system",
            "content": f"Complete Book Outline:\n{outline_context}"
        }]

        writer_final = autogen.AssistantAgent(
            name="writer_final",
            system_message=self.agents["writer"].system_message,
            llm_config=self.agent_config.get("llm_config", {})
        )

        return autogen.GroupChat(
            agents=[
                self.agents["user_proxy"],
                self.agents["memory_keeper"],
                self.agents["researcher"],
                self.agents["writer"],
                self.agents["editor"],
                writer_final
            ],
            messages=messages,
            max_round=6,  # Increased to accommodate research step
            speaker_selection_method="round_robin"
        )

    def _get_sender(self, msg: Dict) -> str:
        """Helper to get sender from message regardless of format"""
        return msg.get("sender") or msg.get("name", "")

    def _verify_chapter_complete(self, messages: List[Dict]) -> bool:
        """Verify chapter completion by analyzing entire conversation context"""
        print("******************** VERIFYING CHAPTER COMPLETION ****************")
        current_chapter = None
        chapter_content = None
        sequence_complete = {
            'memory_update': False,
            'research': False,
            'plan': False,
            'setting': False,
            'scene': False,
            'feedback': False,
            'scene_final': False,
            'confirmation': False
        }

        # Analyze full conversation
        for msg in messages:
            content = msg.get("content", "")

            # Track chapter number
            if not current_chapter:
                num_match = re.search(r"Chapter (\d+):", content)
                if num_match:
                    current_chapter = int(num_match.group(1))

            # Track completion sequence
            if "MEMORY UPDATE:" in content: sequence_complete['memory_update'] = True
            if "RESEARCH:" in content: sequence_complete['research'] = True
            if "PLAN:" in content: sequence_complete['plan'] = True
            if "SETTING:" in content: sequence_complete['setting'] = True
            if "SCENE:" in content: sequence_complete['scene'] = True
            if "FEEDBACK:" in content: sequence_complete['feedback'] = True
            if "SCENE FINAL:" in content:
                sequence_complete['scene_final'] = True
                chapter_content = content.split("SCENE FINAL:")[1].strip()
            if "**Confirmation:**" in content and "successfully" in content:
                sequence_complete['confirmation'] = True

            #print all sequence_complete flags
            print("******************** SEQUENCE COMPLETE **************", sequence_complete)
            print("******************** CURRENT_CHAPTER ****************", current_chapter)
            print("******************** CHAPTER_CONTENT ****************", chapter_content)

        # Verify all steps completed and content exists
        if sequence_complete['scene_final'] and current_chapter and chapter_content:
            # Verify chapter length
            if not self._verify_chapter_length(chapter_content):
                print(f"Chapter {current_chapter} is too short. Minimum required: {self.min_chapter_length} words")
                return False

            self._save_chapter(current_chapter, chapter_content)
            return True

        return False

    def _verify_chapter_length(self, content: str) -> bool:
        """Verify that chapter meets minimum length requirements"""
        # Count words (rough approximation)
        word_count = len(content.split())
        print(f"Chapter word count: {word_count}, Minimum required: {self.min_chapter_length}")
        return word_count >= self.min_chapter_length

    def _prepare_chapter_context(self, chapter_number: int, prompt: str) -> str:
        """Prepare context for chapter generation"""
        if chapter_number == 1:
            return f"Initial Chapter\nRequirements:\n{prompt}"

        context_parts = [
            "Previous Chapter Summaries:",
            *[f"Chapter {i+1}: {summary}" for i, summary in enumerate(self.chapters_memory)],
            "\nCurrent Chapter Requirements:",
            prompt
        ]
        return "\n".join(context_parts)

    def generate_chapter(self, chapter_number: int, prompt: str) -> None:
        """Generate a single chapter with completion verification"""
        print(f"\nGenerating Chapter {chapter_number}...")

        try:
            # Create group chat with reduced rounds
            groupchat = self.initiate_group_chat()
            manager = autogen.GroupChatManager(
                groupchat=groupchat,
                llm_config=self.agent_config.get("llm_config", {})
            )

            # Prepare context
            context = self._prepare_chapter_context(chapter_number, prompt)

            # Get research for this chapter
            research_data = ""
            if self.book_settings.get("enable_research", False):
                print(f"Researching for Chapter {chapter_number}...")
                research_data = self.research_agent.research_for_chapter(prompt, chapter_number)
                research_text = self.research_agent.format_research_for_agent(research_data)
                print(f"Research complete for Chapter {chapter_number}")
            else:
                research_text = "Research disabled in configuration."

            chapter_prompt = f"""
            IMPORTANT: Wait for confirmation before proceeding.
            IMPORTANT: This is Chapter {chapter_number}. Do not proceed to next chapter until explicitly instructed.
            DO NOT END THE STORY HERE unless this is actually the final chapter ({self.outline[-1]['chapter_number']}).

            Current Task: Generate Chapter {chapter_number} content only.

            Chapter Outline:
            Title: {self.outline[chapter_number - 1]['title']}

            Chapter Requirements:
            {prompt}

            Previous Context for Reference:
            {context}

            Research Information:
            {research_text}

            Follow this exact sequence for Chapter {chapter_number} only:

            1. Memory Keeper: Context (MEMORY UPDATE)
            2. Researcher: Provide relevant Dune universe information (RESEARCH)
            3. Writer: Draft (CHAPTER) - MUST be at least {self.min_chapter_length} words
            4. Editor: Review (FEEDBACK)
            5. Writer Final: Revision (CHAPTER FINAL) - MUST be at least {self.min_chapter_length} words

            Wait for each step to complete before proceeding."""

            # Start generation
            self.agents["user_proxy"].initiate_chat(
                manager,
                message=chapter_prompt
            )

            if not self._verify_chapter_complete(groupchat.messages):
                raise ValueError(f"Chapter {chapter_number} generation incomplete")

            self._process_chapter_results(chapter_number, groupchat.messages)
            chapter_file = os.path.join(self.output_dir, f"chapter_{chapter_number:02d}.txt")
            if not os.path.exists(chapter_file):
                raise FileNotFoundError(f"Chapter {chapter_number} file not created")

            completion_msg = f"Chapter {chapter_number} is complete. Proceed with next chapter."
            self.agents["user_proxy"].send(completion_msg, manager)

        except Exception as e:
            print(f"Error in chapter {chapter_number}: {str(e)}")
            self._handle_chapter_generation_failure(chapter_number, prompt)

    def _extract_final_scene(self, messages: List[Dict]) -> Optional[str]:
        """Extract chapter content with improved content detection"""
        for msg in reversed(messages):
            content = msg.get("content", "")
            sender = self._get_sender(msg)

            if sender in ["writer", "writer_final"]:
                # Handle complete scene content
                if "SCENE FINAL:" in content:
                    scene_text = content.split("SCENE FINAL:")[1].strip()
                    if scene_text:
                        return scene_text

                # Fallback to scene content
                if "SCENE:" in content:
                    scene_text = content.split("SCENE:")[1].strip()
                    if scene_text:
                        return scene_text

                # Handle raw content
                if len(content.strip()) > 100:  # Minimum content threshold
                    return content.strip()

        return None

    def _handle_chapter_generation_failure(self, chapter_number: int, prompt: str) -> None:
        """Handle failed chapter generation with simplified retry"""
        print(f"Attempting simplified retry for Chapter {chapter_number}...")

        try:
            # Create a new group chat with just essential agents
            retry_groupchat = autogen.GroupChat(
                agents=[
                    self.agents["user_proxy"],
                    self.agents["story_planner"],
                    self.agents["writer"]
                ],
                messages=[],
                max_round=3
            )

            manager = autogen.GroupChatManager(
                groupchat=retry_groupchat,
                llm_config=self.agent_config
            )

            retry_prompt = f"""Emergency chapter generation for Chapter {chapter_number}.

{prompt}

Please generate this chapter in two steps:
1. Story Planner: Create a basic outline (tag: PLAN)
2. Writer: Write the complete chapter (tag: SCENE FINAL)

Keep it simple and direct."""

            self.agents["user_proxy"].initiate_chat(
                manager,
                message=retry_prompt
            )

            # Save the retry results
            self._process_chapter_results(chapter_number, retry_groupchat.messages)

        except Exception as e:
            print(f"Error in retry attempt for Chapter {chapter_number}: {str(e)}")
            print("Unable to generate chapter content after retry")

    def _process_chapter_results(self, chapter_number: int, messages: List[Dict]) -> None:
        """Process and save chapter results, updating memory"""
        try:
            # Extract the Memory Keeper's final summary
            memory_updates = []
            for msg in reversed(messages):
                sender = self._get_sender(msg)
                content = msg.get("content", "")

                if sender == "memory_keeper" and "MEMORY UPDATE:" in content:
                    update_start = content.find("MEMORY UPDATE:") + 14
                    memory_updates.append(content[update_start:].strip())
                    break

            # Add to memory even if no explicit update (use basic content summary)
            if memory_updates:
                self.chapters_memory.append(memory_updates[0])
            else:
                # Create basic memory from chapter content
                chapter_content = self._extract_final_scene(messages)
                if chapter_content:
                    basic_summary = f"Chapter {chapter_number} Summary: {chapter_content[:200]}..."
                    self.chapters_memory.append(basic_summary)

            # Extract and save the chapter content
            self._save_chapter(chapter_number, messages)

        except Exception as e:
            print(f"Error processing chapter results: {str(e)}")
            raise

    def _save_chapter(self, chapter_number: int, content: str) -> None:
        """Save chapter content to file"""
        print(f"\nSaving Chapter {chapter_number}")
        try:
            # Clean up the content
            chapter_content = self._clean_chapter_content(content)

            # Verify chapter length one more time
            word_count = len(chapter_content.split())
            if word_count < self.min_chapter_length:
                print(f"WARNING: Chapter {chapter_number} is shorter than required ({word_count} words vs {self.min_chapter_length} minimum)")

            filename = os.path.join(self.output_dir, f"chapter_{chapter_number:02d}.txt")

            # Create backup if file exists
            if os.path.exists(filename):
                backup_filename = f"{filename}.backup"
                import shutil
                shutil.copy2(filename, backup_filename)

            # Add chapter title and number
            chapter_title = self.outline[chapter_number - 1]['title']
            formatted_content = f"Chapter {chapter_number}: {chapter_title}\n\n{chapter_content}"

            with open(filename, "w", encoding='utf-8') as f:
                f.write(formatted_content)

            # Verify file
            with open(filename, "r", encoding='utf-8') as f:
                saved_content = f.read()
                if len(saved_content.strip()) == 0:
                    raise IOError(f"File {filename} is empty")

            print(f"✓ Saved to: {filename} ({word_count} words)")

        except Exception as e:
            print(f"Error saving chapter: {str(e)}")
            raise

    def generate_book(self, outline: List[Dict]) -> None:
        """Generate the book with strict chapter sequencing"""
        print("\nStarting Book Generation...")
        print(f"Total chapters: {len(outline)}")

        # Sort outline by chapter number
        sorted_outline = sorted(outline, key=lambda x: x["chapter_number"])

        for chapter in sorted_outline:
            chapter_number = chapter["chapter_number"]

            # Verify previous chapter exists and is valid
            if chapter_number > 1:
                prev_file = os.path.join(self.output_dir, f"chapter_{chapter_number-1:02d}.txt")
                if not os.path.exists(prev_file):
                    print(f"Previous chapter {chapter_number-1} not found. Stopping.")
                    break

                # Verify previous chapter content
                with open(prev_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not self._verify_chapter_content(content, chapter_number-1):
                        print(f"Previous chapter {chapter_number-1} content invalid. Stopping.")
                        break

            # Generate current chapter
            print(f"\n{'='*20} Chapter {chapter_number} {'='*20}")
            self.generate_chapter(chapter_number, chapter["prompt"])

            # Verify current chapter
            chapter_file = os.path.join(self.output_dir, f"chapter_{chapter_number:02d}.txt")
            if not os.path.exists(chapter_file):
                print(f"Failed to generate chapter {chapter_number}")
                break

            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if not self._verify_chapter_content(content, chapter_number):
                    print(f"Chapter {chapter_number} content invalid")
                    break

            print(f"✓ Chapter {chapter_number} complete")
            time.sleep(5)

    def _verify_chapter_content(self, content: str, chapter_number: int) -> bool:
        """Verify chapter content is valid"""
        if not content:
            print(f"Chapter {chapter_number} has no content")
            return False

        # Check for chapter header
        if f"Chapter {chapter_number}" not in content:
            print(f"Chapter {chapter_number} header not found in content")
            return False

        # Check for minimum content length
        word_count = len(content.split())
        if word_count < self.min_chapter_length:
            print(f"Chapter {chapter_number} content too short: {word_count} words (minimum: {self.min_chapter_length})")
            return False

        # Check for key character names
        if "Paul" not in content or "Jeff" not in content:
            print(f"Chapter {chapter_number} missing key characters (Paul and/or Jeff)")
            return False

        # Ensure content isn't just metadata
        lines = content.split('\n')
        content_lines = [line for line in lines if line.strip() and 'MEMORY UPDATE:' not in line]

        if len(content_lines) < 10:  # Require substantial content
            print(f"Chapter {chapter_number} has insufficient content lines: {len(content_lines)}")
            return False

        return True