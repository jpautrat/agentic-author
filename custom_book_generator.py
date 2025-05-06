"""Customizable book generator with user-defined parameters"""
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
log_file = open("custom_book_debug.txt", "w")
def log(message):
    """Write to log file and print to console"""
    print(message)
    log_file.write(message + "\n")
    log_file.flush()

try:
    log("Starting customizable book generation script...")
    
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

Structure Requirements:
- The book should have exactly {params['num_chapters']} chapters
- Each chapter must have at least {params['min_scenes']} distinct scenes
- Each chapter must be at least {params['min_chapter_length']} words long

Style Requirements:
- 
- Use rich, descriptive prose with philosophical undertones
- Include internal monologues that reveal character thoughts
- Balance action with introspection
- Incorporate political intrigue and power dynamics
- Use sensory details to bring the world to life
- Include occasional made-up quotes or excerpts as chapter epigraphs 


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
    
    log("\nCustom book generation completed successfully")
    
except Exception as e:
    log(f"Unhandled exception: {str(e)}")
    traceback.print_exc(file=log_file)
    
finally:
    log_file.close()
    print("\nProcess complete. Check custom_book_debug.txt for details.")
    print("Book output should be in the book_output directory.")
    input("Press Enter to exit...")
