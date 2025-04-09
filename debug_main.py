"""Debug version of main script with error handling"""
import os
import sys
import traceback
from dotenv import load_dotenv

# Create a log file
log_file = open("debug_log.txt", "w")
def log(message):
    """Write to log file and print to console"""
    print(message)
    log_file.write(message + "\n")
    log_file.flush()

try:
    log("Starting debug main script...")
    
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
    
    # Create agents
    log("Creating agents...")
    try:
        num_chapters = 10
        outline_agents = BookAgents(agent_config)
        agents = outline_agents.create_agents(
            """Create a story about Jeff and Paul Atreides in the Dune universe""", 
            num_chapters
        )
        log("Successfully created agents")
    except Exception as e:
        log(f"Error creating agents: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    # Generate outline
    log("Generating outline...")
    try:
        outline_gen = OutlineGenerator(agents, agent_config)
        outline = outline_gen.generate_outline(
            """Create a story about Jeff and Paul Atreides in the Dune universe""", 
            num_chapters
        )
        log("Successfully generated outline")
    except Exception as e:
        log(f"Error generating outline: {str(e)}")
        traceback.print_exc(file=log_file)
        sys.exit(1)
    
    log("Debug script completed successfully")
    
except Exception as e:
    log(f"Unhandled exception: {str(e)}")
    traceback.print_exc(file=log_file)
    
finally:
    log_file.close()
    print("\nDebug complete. Check debug_log.txt for details.")
    input("Press Enter to exit...")
