"""Debug version of main script that generates the full book"""
import os
import sys
import traceback
from dotenv import load_dotenv

# Create a log file
log_file = open("full_book_debug.txt", "w")
def log(message):
    """Write to log file and print to console"""
    print(message)
    log_file.write(message + "\n")
    log_file.flush()

try:
    log("Starting full book generation script...")
    
    # Load environment variables
    load_dotenv()
    log("Loaded environment variables from .env file")
    
    # Log OpenAI API key (first 5 and last 3 characters only)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key:
        masked_key = f"{api_key[:5]}...{api_key[-3:]}"
        log(f"OpenAI API key found: {masked_key}")
    else:
        log("WARNING: OpenAI API key not found in environment variables")
    
    # Log OpenAI model
    model = os.getenv("OPENAI_MODEL", "")
    log(f"OpenAI model: {model}")
    
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
    
    # Initial prompt
    initial_prompt = """
Create a story in Frank Herbert's established writing style with these key elements:
It is important that it has several key storylines that intersect and influence each other. The story should be set within the *Dune* universe, maintaining its deep philosophical undertones, political intrigue, and mythic weight. The protagonist is Jeff, a loyal warrior and strategist who walks beside Paul Atreides from his youth on Caladan to his rise as Muad'Dib. History forgets him, but he was there—the brother who was never named, the shadow who stood at the center of the storm.

The novel follows Jeff's journey as he survives the fall of House Atreides, adapts to Fremen life, and plays a crucial but unseen role in Paul's ascension. His fate is intertwined with Paul's, but he is not bound by prophecy. The story explores themes of loyalty, fate, survival, and the hidden costs of empire-building.

Style Requirements:
- Write in Frank Herbert's distinctive style from the Dune series
- Use rich, descriptive prose with philosophical undertones
- Include internal monologues that reveal character thoughts
- Balance action with introspection
- Incorporate political intrigue and power dynamics
- Use sensory details to bring the world to life
- Include occasional made-up quotes or excerpts as chapter epigraphs (similar to Herbert's style)

Each chapter must be at least 3000 words long and maintain focus on Jeff's relationship with Paul Atreides.
"""
    
    # Create agents
    log("Creating agents...")
    try:
        num_chapters = 3  # Reduced for testing
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
    except Exception as e:
        log(f"Error generating outline: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    # Create book generator
    log("\nCreating book generator...")
    try:
        book_agents = BookAgents(agent_config, outline)
        agents_with_context = book_agents.create_agents(initial_prompt, num_chapters)
        book_gen = BookGenerator(agents_with_context, agent_config, outline)
        log("Successfully created book generator")
    except Exception as e:
        log(f"Error creating book generator: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    # Generate book
    log("\nGenerating book chapters...")
    try:
        if outline:
            book_gen.generate_book(outline)
            log("Successfully generated book")
        else:
            log("Error: No outline was generated.")
    except Exception as e:
        log(f"Error generating book: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    log("\nFull book generation completed successfully")
    
except Exception as e:
    log(f"Unhandled exception: {str(e)}")
    traceback.print_exc(file=log_file)
    
finally:
    log_file.close()
    print("\nDebug complete. Check full_book_debug.txt for details.")
    input("Press Enter to exit...")
