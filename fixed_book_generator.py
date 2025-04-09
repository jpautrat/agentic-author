"""Fixed version of the book generator with improved error handling"""
import os
import sys
import traceback
from dotenv import load_dotenv

def get_user_input():
    """Get user input for book generation parameters"""
    print("\n=== Book Generation Parameters ===\n")
    
    # Number of chapters
    while True:
        try:
            num_chapters = int(input("Number of chapters (1-20): "))
            if 1 <= num_chapters <= 20:
                break
            print("Please enter a number between 1 and 20.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Minimum chapter length
    while True:
        try:
            min_chapter_length = int(input("Minimum words per chapter (1000-10000): "))
            if 1000 <= min_chapter_length <= 10000:
                break
            print("Please enter a number between 1000 and 10000.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Minimum scenes per chapter
    while True:
        try:
            min_scenes = int(input("Minimum scenes per chapter (1-10): "))
            if 1 <= min_scenes <= 10:
                break
            print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")
    
    # OpenAI model
    print("\nAvailable OpenAI models:")
    print("1. gpt-4 (Best quality, most expensive)")
    print("2. gpt-4-turbo (Faster version of GPT-4)")
    print("3. gpt-3.5-turbo (Cheaper, less capable)")
    print("4. gpt-3.5-turbo-16k (Cheaper with longer context)")
    
    while True:
        try:
            model_choice = int(input("Choose a model (1-4): "))
            if 1 <= model_choice <= 4:
                break
            print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Map choice to model name
    model_map = {
        1: "gpt-4",
        2: "gpt-4-turbo",
        3: "gpt-3.5-turbo",
        4: "gpt-3.5-turbo-16k"
    }
    model = model_map[model_choice]
    
    return {
        "num_chapters": num_chapters,
        "min_chapter_length": min_chapter_length,
        "min_scenes": min_scenes,
        "model": model
    }

# Create a log file
log_file = open("fixed_book_debug.txt", "w")
def log(message):
    """Write to log file and print to console"""
    print(message)
    log_file.write(message + "\n")
    log_file.flush()

try:
    log("Starting fixed book generation script...")
    
    # Load environment variables
    load_dotenv()
    log("Loaded environment variables from .env file")
    
    # Get user input
    params = get_user_input()
    log(f"User parameters: {params}")
    
    # Set environment variables based on user input
    os.environ["MIN_CHAPTER_LENGTH"] = str(params["min_chapter_length"])
    os.environ["OPENAI_MODEL"] = params["model"]
    
    # Log OpenAI API key (first 5 and last 3 characters only)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key:
        masked_key = f"{api_key[:5]}...{api_key[-3:]}"
        log(f"OpenAI API key found: {masked_key}")
    else:
        log("WARNING: OpenAI API key not found in environment variables")
        api_key = input("Please enter your OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["LLM_API_KEY"] = api_key
    
    # Import configuration
    log("Importing configuration...")
    try:
        from config import get_config
        log("Successfully imported config module")
    except Exception as e:
        log(f"Error importing config module: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    # Get configuration
    log("Getting configuration...")
    try:
        agent_config = get_config()
        # Override book settings with user parameters
        agent_config["book_settings"]["min_chapter_length"] = params["min_chapter_length"]
        log("Successfully got configuration")
    except Exception as e:
        log(f"Error getting configuration: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    # Import other modules
    log("Importing other modules...")
    try:
        from agents import BookAgents
        from book_generator import BookGenerator
        from outline_generator import OutlineGenerator
        log("Successfully imported all modules")
    except Exception as e:
        log(f"Error importing modules: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    # Book settings
    book_settings = agent_config.get("book_settings", {})
    research_enabled = book_settings.get("enable_research", False)
    min_chapter_length = book_settings.get("min_chapter_length", 3000)
    log(f"Research enabled: {research_enabled}")
    log(f"Minimum chapter length: {min_chapter_length} words")
    log(f"Using OpenAI model: {params['model']}")
    
    # Initial prompt with user parameters
    initial_prompt = f"""
Create a story in Frank Herbert's established writing style with these key elements:
It is important that it has several key storylines that intersect and influence each other. The story should be set within the *Dune* universe, maintaining its deep philosophical undertones, political intrigue, and mythic weight. The protagonist is Jeff, a loyal warrior and strategist who walks beside Paul Atreides from his youth on Caladan to his rise as Muad'Dib. History forgets him, but he was there—the brother who was never named, the shadow who stood at the center of the storm.

The novel follows Jeff's journey as he survives the fall of House Atreides, adapts to Fremen life, and plays a crucial but unseen role in Paul's ascension. His fate is intertwined with Paul's, but he is not bound by prophecy. The story explores themes of loyalty, fate, survival, and the hidden costs of empire-building.

Structure Requirements:
- The book should have exactly {params['num_chapters']} chapters
- Each chapter must have at least {params['min_scenes']} distinct scenes
- Each chapter must be at least {params['min_chapter_length']} words long

Style Requirements:
- Write in Frank Herbert's distinctive style from the Dune series
- Use rich, descriptive prose with philosophical undertones
- Include internal monologues that reveal character thoughts
- Balance action with introspection
- Incorporate political intrigue and power dynamics
- Use sensory details to bring the world to life
- Include occasional made-up quotes or excerpts as chapter epigraphs (similar to Herbert's style)

Each chapter must maintain focus on Jeff's relationship with Paul Atreides.
"""
    
    # Create agents
    log("Creating agents...")
    try:
        num_chapters = params["num_chapters"]
        outline_agents = BookAgents(agent_config)
        agents = outline_agents.create_agents(initial_prompt, num_chapters)
        log("Successfully created agents")
    except Exception as e:
        log(f"Error creating agents: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    # Generate outline
    log("Generating outline...")
    try:
        outline_gen = OutlineGenerator(agents, agent_config)
        outline = outline_gen.generate_outline(initial_prompt, num_chapters)
        log("Successfully generated outline")
        
        # Log the outline
        log("\nGenerated Outline:")
        for chapter in outline:
            log(f"\nChapter {chapter['chapter_number']}: {chapter['title']}")
            log("-" * 50)
            log(chapter['prompt'])
            
        # Save the outline
        os.makedirs("book_output", exist_ok=True)
        with open("book_output/outline.txt", "w") as f:
            for chapter in outline:
                f.write(f"\nChapter {chapter['chapter_number']}: {chapter['title']}\n")
                f.write("-" * 50 + "\n")
                f.write(chapter['prompt'] + "\n")
        log("Saved outline to book_output/outline.txt")
    except Exception as e:
        log(f"Error generating outline: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    # Generate chapters one by one
    log("\nGenerating chapters individually...")
    try:
        # Create book agents
        book_agents = BookAgents(agent_config, outline)
        agents_with_context = book_agents.create_agents(initial_prompt, num_chapters)
        
        # Import necessary modules
        import autogen
        import time
        import re
        
        # Create output directory
        output_dir = "book_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Function to generate a single chapter
        def generate_chapter(chapter_number):
            log(f"\n{'='*20} Chapter {chapter_number} {'='*20}")
            
            # Get chapter info
            chapter_info = next((ch for ch in outline if ch["chapter_number"] == chapter_number), None)
            if not chapter_info:
                log(f"Error: Chapter {chapter_number} not found in outline")
                return False
                
            prompt = chapter_info["prompt"]
            title = chapter_info["title"]
            
            # Prepare context
            if chapter_number == 1:
                context = f"Initial Chapter\nRequirements:\n{prompt}"
            else:
                # Get summaries of previous chapters
                previous_chapters = []
                for i in range(1, chapter_number):
                    chapter_file = os.path.join(output_dir, f"chapter_{i:02d}.txt")
                    if os.path.exists(chapter_file):
                        with open(chapter_file, "r", encoding="utf-8") as f:
                            content = f.read()
                            summary = content[:200] + "..."  # Simple summary
                            previous_chapters.append(f"Chapter {i}: {summary}")
                
                context = "\n".join([
                    "Previous Chapter Summaries:",
                    *previous_chapters,
                    "\nCurrent Chapter Requirements:",
                    prompt
                ])
            
            # Create chapter prompt
            chapter_prompt = f"""
IMPORTANT: This is Chapter {chapter_number}: {title}

Your task is to write this complete chapter in Frank Herbert's Dune style.

Chapter Requirements:
{prompt}

Previous Context:
{context}

REQUIREMENTS:
1. Write a complete chapter of at least {params['min_chapter_length']} words
2. Include at least {params['min_scenes']} distinct scenes
3. Focus on Jeff's relationship with Paul Atreides
4. Write in Frank Herbert's distinctive style
5. Include an epigraph at the beginning (a quote or excerpt in Herbert's style)
6. End the chapter with a clear conclusion

Format your response as a complete chapter. Do not include "CHAPTER:" or similar tags.
Start with the chapter title and number, then the epigraph, then the chapter content.
"""
            
            # Generate chapter using direct API call
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
                
                log(f"Generating Chapter {chapter_number} using {params['model']}...")
                response = client.chat.completions.create(
                    model=params['model'],
                    messages=[
                        {"role": "system", "content": "You are an expert writer in the style of Frank Herbert's Dune series."},
                        {"role": "user", "content": chapter_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                
                # Get chapter content
                chapter_content = response.choices[0].message.content
                
                # Verify content length
                word_count = len(chapter_content.split())
                if word_count < params['min_chapter_length']:
                    log(f"WARNING: Chapter {chapter_number} is shorter than required ({word_count} words vs {params['min_chapter_length']} minimum)")
                    
                    # Try to extend the chapter if it's too short
                    extension_prompt = f"""
The chapter you wrote is too short ({word_count} words). Please continue the chapter to reach at least {params['min_chapter_length']} words.

Current chapter content:
{chapter_content}

Continue from where you left off, maintaining the same style and narrative flow.
"""
                    
                    log("Extending chapter to meet minimum length requirement...")
                    extension_response = client.chat.completions.create(
                        model=params['model'],
                        messages=[
                            {"role": "system", "content": "You are an expert writer in the style of Frank Herbert's Dune series."},
                            {"role": "user", "content": extension_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=4000
                    )
                    
                    # Combine original and extension
                    extension_content = extension_response.choices[0].message.content
                    chapter_content = chapter_content + "\n\n" + extension_content
                    
                    # Check final length
                    word_count = len(chapter_content.split())
                    log(f"Extended chapter length: {word_count} words")
                
                # Save chapter
                filename = os.path.join(output_dir, f"chapter_{chapter_number:02d}.txt")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"Chapter {chapter_number}: {title}\n\n{chapter_content}")
                
                log(f"✓ Saved Chapter {chapter_number} to {filename} ({word_count} words)")
                return True
                
            except Exception as e:
                log(f"Error generating Chapter {chapter_number}: {str(e)}")
                traceback.print_exc(file=log_file)
                return False
        
        # Generate each chapter
        for chapter_number in range(1, num_chapters + 1):
            success = generate_chapter(chapter_number)
            if not success:
                log(f"Failed to generate Chapter {chapter_number}. Stopping.")
                break
            time.sleep(5)  # Brief pause between chapters
        
        log("\nBook generation complete!")
        
    except Exception as e:
        log(f"Error in chapter generation: {str(e)}")
        traceback.print_exc(file=log_file)
    
except Exception as e:
    log(f"Unhandled exception: {str(e)}")
    traceback.print_exc(file=log_file)
    
finally:
    log_file.close()
    print("\nProcess complete. Check fixed_book_debug.txt for details.")
    print("Book output should be in the book_output directory.")
    input("Press Enter to exit...")
