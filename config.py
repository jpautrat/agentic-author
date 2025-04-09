"""Configuration for the book generation system"""
import os
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_config(local_url: str = None) -> Dict:
    """Get the configuration for the agents"""

    # Use environment variable if available, otherwise use default
    if local_url is None:
        local_url = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")

    api_key = os.getenv("LLM_API_KEY", "not-needed")

    # Check if using OpenAI or local LLM
    if "openai.com" in local_url:
        # Get model from environment or use default
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        print(f"Using OpenAI model: {openai_model}")

        # For AutoGen with OpenAI, we need to set up the config differently
        # This is the format AutoGen expects
        llm_config = {
            "config_list": [
                {
                    "model": openai_model,
                    "api_key": api_key
                }
            ],
            "temperature": 0.7,
            "timeout": 600
        }

        # Set OpenAI API key as environment variable (AutoGen checks for this)
        os.environ["OPENAI_API_KEY"] = api_key

        return {
            "llm_config": llm_config,
            "book_settings": {
                "min_chapter_length": int(os.getenv("MIN_CHAPTER_LENGTH", 3000)),
                "max_retries": int(os.getenv("MAX_RETRIES", 3)),
                "enable_research": True,
                "research_depth": "medium"
            },
            "research_settings": {
                "google_api_key": os.getenv("GOOGLE_API_KEY"),
                "google_cse_id": os.getenv("GOOGLE_CSE_ID")
            }
        }
    else:
        # Config for local LLM
        config_list = [{
            'model': 'Mistral-Nemo-Instruct-2407',
            'base_url': local_url,
            'api_key': api_key
        }]

    # For local LLM, use standard configuration
    llm_config = {
        "seed": 42,
        "temperature": 0.7,
        "config_list": config_list,
        "timeout": 600,
        "cache_seed": None
    }

    # Book generation settings - kept separate from LLM config
    book_settings = {
        "min_chapter_length": int(os.getenv("MIN_CHAPTER_LENGTH", 3000)),
        "max_retries": int(os.getenv("MAX_RETRIES", 3)),
        "enable_research": True,  # Enable web research by default
        "research_depth": "medium"  # Default research depth
    }

    # Web research settings
    research_settings = {
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "google_cse_id": os.getenv("GOOGLE_CSE_ID")
    }

    # Create a complete config dictionary with all settings
    agent_config = {
        "llm_config": llm_config,
        "book_settings": book_settings,
        "research_settings": research_settings
    }

    return agent_config