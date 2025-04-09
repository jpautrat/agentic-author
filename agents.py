"""Define the agents used in the book generation system with improved context management"""
import autogen
import re
from typing import Dict, List, Optional
from research_agent import ResearchAgent

class BookAgents:
    def __init__(self, agent_config: Dict, outline: Optional[List[Dict]] = None):
        """Initialize agents with book outline context"""
        self.agent_config = agent_config
        self.outline = outline
        self.world_elements = {}  # Track described locations/elements
        self.character_developments = {}  # Track character arcs
        self.research_agent = ResearchAgent()  # Initialize research agent
        self.research_cache = {}  # Cache research results by chapter

    def _format_outline_context(self) -> str:
        """Format the book outline into a readable context"""
        if not self.outline:
            return ""

        context_parts = ["Complete Book Outline:"]
        for chapter in self.outline:
            context_parts.extend([
                f"\nChapter {chapter['chapter_number']}: {chapter['title']}",
                chapter['prompt']
            ])
        return "\n".join(context_parts)

    def get_research_for_chapter(self, chapter_number: int, chapter_prompt: str) -> str:
        """Get research data for a specific chapter"""
        # Check if we already have research for this chapter
        if chapter_number in self.research_cache:
            return self.research_cache[chapter_number]

        # Check if research is enabled in config
        book_settings = self.agent_config.get("book_settings", {})
        if not book_settings.get("enable_research", False):
            return "Research disabled in configuration."

        # Get research depth from config
        research_depth = book_settings.get("research_depth", "basic")

        # Perform research
        research_data = self.research_agent.research_for_chapter(chapter_prompt, chapter_number)
        formatted_research = self.research_agent.format_research_for_agent(research_data)

        # Cache the results
        self.research_cache[chapter_number] = formatted_research

        return formatted_research

    def create_agents(self, initial_prompt, num_chapters) -> Dict:
        """Create and return all agents needed for book generation"""
        outline_context = self._format_outline_context()

        # Memory Keeper: Maintains story continuity and context
        memory_keeper = autogen.AssistantAgent(
            name="memory_keeper",
            system_message=f"""You are the keeper of the story's continuity and context.
            Your responsibilities:
            1. Track and summarize each chapter's key events
            2. Monitor character development and relationships
            3. Maintain world-building consistency
            4. Flag any continuity issues

            Book Overview:
            {outline_context}

            Format your responses as follows:
            - Start updates with 'MEMORY UPDATE:'
            - List key events with 'EVENT:'
            - List character developments with 'CHARACTER:'
            - List world details with 'WORLD:'
            - Flag issues with 'CONTINUITY ALERT:'""",
            llm_config=self.agent_config.get("llm_config", {}),
        )

        # Story Planner - Focuses on high-level story structure
        story_planner = autogen.AssistantAgent(
            name="story_planner",
            system_message=f"""You are an expert story arc planner focused on overall narrative structure.

            Your sole responsibility is creating the high-level story arc.
            When given an initial story premise:
            1. Identify major plot points and story beats
            2. Map character arcs and development
            3. Note major story transitions
            4. Plan narrative pacing

            Format your output EXACTLY as:
            STORY_ARC:
            - Major Plot Points:
            [List each major event that drives the story]

            - Character Arcs:
            [For each main character, describe their development path]

            - Story Beats:
            [List key emotional and narrative moments in sequence]

            - Key Transitions:
            [Describe major shifts in story direction or tone]

            Always provide specific, detailed content - never use placeholders.""",
            llm_config=self.agent_config.get("llm_config", {}),
        )

        # Outline Creator - Creates detailed chapter outlines
        outline_creator = autogen.AssistantAgent(
            name="outline_creator",
            system_message=f"""Generate a detailed {num_chapters}-chapter outline.

            YOU MUST USE EXACTLY THIS FORMAT FOR EACH CHAPTER - NO DEVIATIONS:

            Chapter 1: [Title]
            Chapter Title: [Same title as above]
            Key Events:
            - [Event 1]
            - [Event 2]
            - [Event 3]
            Character Developments: [Specific character moments and changes]
            Setting: [Specific location and atmosphere]
            Tone: [Specific emotional and narrative tone]

            [REPEAT THIS EXACT FORMAT FOR ALL {num_chapters} CHAPTERS]

            Requirements:
            1. EVERY field must be present for EVERY chapter
            2. EVERY chapter must have AT LEAST 3 specific Key Events
            3. ALL chapters must be detailed - no placeholders
            4. Format must match EXACTLY - including all headings and bullet points

            Initial Premise:
            {initial_prompt}

            START WITH 'OUTLINE:' AND END WITH 'END OF OUTLINE'
            """,
            llm_config=self.agent_config.get("llm_config", {}),
        )

        # World Builder: Creates and maintains the story setting
        world_builder = autogen.AssistantAgent(
            name="world_builder",
            system_message=f"""You are an expert in world-building who creates rich, consistent settings.

            Your role is to establish ALL settings and locations needed for the entire story based on a provided story arc.

            Book Overview:
            {outline_context}

            Your responsibilities:
            1. Review the story arc to identify every location and setting needed
            2. Create detailed descriptions for each setting, including:
            - Physical layout and appearance
            - Atmosphere and environmental details
            - Important objects or features
            - Sensory details (sights, sounds, smells)
            3. Identify recurring locations that appear multiple times
            4. Note how settings might change over time
            5. Create a cohesive world that supports the story's themes

            Format your response as:
            WORLD_ELEMENTS:

            [LOCATION NAME]:
            - Physical Description: [detailed description]
            - Atmosphere: [mood, time of day, lighting, etc.]
            - Key Features: [important objects, layout elements]
            - Sensory Details: [what characters would experience]

            [RECURRING ELEMENTS]:
            - List any settings that appear multiple times
            - Note any changes to settings over time

            [TRANSITIONS]:
            - How settings connect to each other
            - How characters move between locations""",
            llm_config=self.agent_config.get("llm_config", {}),
        )

        # Research Agent: Provides factual information
        researcher = autogen.AssistantAgent(
            name="researcher",
            system_message=f"""You are an expert researcher who provides accurate information about the Dune universe.

            Your responsibilities:
            1. Provide factual information about the Dune universe
            2. Ensure accuracy of world-building elements
            3. Verify character details and relationships
            4. Maintain consistency with Frank Herbert's established canon

            Book Overview:
            {outline_context}

            Format your responses with 'RESEARCH:' followed by your findings.
            Always cite your sources when possible.""",
            llm_config=self.agent_config.get("llm_config", {}),
        )

        # Writer: Generates the actual prose
        writer = autogen.AssistantAgent(
            name="writer",
            system_message=f"""You are an expert creative writer who brings scenes to life in Frank Herbert's distinctive style.

            Book Context:
            {outline_context}

            IMPORTANT STYLE GUIDELINES:
            - Write in Frank Herbert's distinctive style from the Dune series
            - Use rich, descriptive prose with philosophical undertones
            - Include internal monologues that reveal character thoughts
            - Balance action with introspection
            - Incorporate political intrigue and power dynamics
            - Use sensory details to bring the world to life
            - Include occasional made-up quotes or excerpts as chapter epigraphs (similar to Herbert's style)

            CONTENT REQUIREMENTS:
            1. Write according to the outlined plot points
            2. Maintain consistent character voices
            3. Incorporate world-building details
            4. Create engaging prose
            5. Please make sure that you write the complete scene, do not leave it incomplete
            6. Each chapter MUST be at least 3000 words (approximately 15,000 characters). This is a HARD REQUIREMENT.
               If your output is shorter, continue writing until you reach this minimum length
            7. Ensure transitions are smooth and logical
            8. Do not cut off the scene, make sure it has a proper ending
            9. Add extensive details about the environment, characters, and internal thoughts
            10. Focus on the relationship between Jeff and Paul Atreides as specified in the prompt
            11. Maintain consistency with the Dune universe

            Always reference the outline, research, and previous content.
            Mark drafts with 'SCENE:' and final versions with 'SCENE FINAL:'""",
            llm_config=self.agent_config.get("llm_config", {}),
        )

        # Editor: Reviews and improves content
        editor = autogen.AssistantAgent(
            name="editor",
            system_message=f"""You are an expert editor ensuring quality and consistency in the style of Frank Herbert's Dune series.

            Book Overview:
            {outline_context}

            STYLE REQUIREMENTS:
            - Ensure the prose matches Frank Herbert's distinctive style
            - Check for philosophical undertones and political intrigue
            - Verify the balance of action and introspection
            - Ensure sensory details are rich and evocative
            - Maintain the epic scope and mythic quality of the Dune universe

            CONTENT REQUIREMENTS:
            1. Check alignment with outline
            2. Verify character consistency, especially Jeff and Paul Atreides
            3. Maintain world-building rules of the Dune universe
            4. Improve prose quality while preserving Herbert's style
            5. Return complete edited chapter
            6. Never ask to start the next chapter, as the next step is finalizing this chapter
            7. Each chapter MUST be at least 3000 words. If the content is shorter, return it to the writer for expansion.
               This is a hard requirement - do not approve chapters shorter than 15,000 characters
            8. Ensure the story stays focused on Jeff as Paul's friend and their relationship
            9. Verify factual accuracy with the Dune universe

            Format your responses:
            1. Start critiques with 'FEEDBACK:'
            2. Provide suggestions with 'SUGGEST:'
            3. Return full edited chapter with 'EDITED_SCENE:'

            Reference specific outline elements in your feedback.""",
            llm_config=self.agent_config.get("llm_config", {}),
        )

        # User Proxy: Manages the interaction
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="TERMINATE",
            code_execution_config={
                "work_dir": "book_output",
                "use_docker": False
            }
        )

        return {
            "story_planner": story_planner,
            "world_builder": world_builder,
            "memory_keeper": memory_keeper,
            "writer": writer,
            "editor": editor,
            "user_proxy": user_proxy,
            "outline_creator": outline_creator,
            "researcher": researcher
        }

    def update_world_element(self, element_name: str, description: str) -> None:
        """Track a new or updated world element"""
        self.world_elements[element_name] = description

    def update_character_development(self, character_name: str, development: str) -> None:
        """Track character development"""
        if character_name not in self.character_developments:
            self.character_developments[character_name] = []
        self.character_developments[character_name].append(development)

    def get_world_context(self) -> str:
        """Get formatted world-building context"""
        if not self.world_elements:
            return "No established world elements yet."

        return "\n".join([
            "Established World Elements:",
            *[f"- {name}: {desc}" for name, desc in self.world_elements.items()]
        ])

    def get_character_context(self) -> str:
        """Get formatted character development context"""
        if not self.character_developments:
            return "No character developments tracked yet."

        return "\n".join([
            "Character Development History:",
            *[f"- {name}:\n  " + "\n  ".join(devs)
              for name, devs in self.character_developments.items()]
        ])