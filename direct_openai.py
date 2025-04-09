"""Simple script to test OpenAI API connection"""
import os
import sys
from dotenv import load_dotenv

# Try to load from .env file
load_dotenv()

def test_openai_connection():
    """Test connection to OpenAI API"""
    try:
        # Get API key from environment or prompt user
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = input("Enter your OpenAI API key: ")
            os.environ["OPENAI_API_KEY"] = api_key
        
        # Get model from environment or use default
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        # Try to import OpenAI
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            # Make a simple API call
            print(f"Testing connection to OpenAI API with model {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say hello!"}
                ]
            )
            
            # Print response
            print("\nResponse from OpenAI:")
            print(response.choices[0].message.content)
            print("\nConnection successful!")
            
            # Save API key to .env file
            if not os.path.exists(".env"):
                with open(".env", "w") as f:
                    f.write(f"OPENAI_API_KEY={api_key}\n")
                    f.write(f"OPENAI_MODEL={model}\n")
                    f.write("LLM_BASE_URL=https://api.openai.com/v1\n")
                    f.write(f"LLM_API_KEY={api_key}\n")
                print("\nSaved API key to .env file")
            
            return True
            
        except ImportError:
            print("Error: OpenAI package not installed.")
            print("Installing required packages...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
            print("Please run this script again.")
            return False
            
    except Exception as e:
        print(f"Error connecting to OpenAI API: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_connection()
    input("\nPress Enter to exit...")
