"""Test script to verify configuration and API access"""
import os
import sys
from dotenv import load_dotenv
from research_agent import ResearchAgent
from config import get_config

def test_env_file():
    """Test if .env file exists and can be loaded"""
    print("Testing .env file...")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("ERROR: .env file not found. Please create it using the .env.template as a guide.")
        return False
        
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    required_vars = ["GOOGLE_API_KEY", "GOOGLE_CSE_ID"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            
    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        return False
        
    print("✓ .env file exists and contains required variables")
    return True
    
def test_config_loading():
    """Test if configuration loads correctly"""
    print("\nTesting configuration loading...")
    
    try:
        config = get_config()
        
        # Check if book settings are present
        if "book_settings" not in config:
            print("ERROR: book_settings not found in configuration")
            return False
            
        # Check if research settings are present
        if "research_settings" not in config:
            print("ERROR: research_settings not found in configuration")
            return False
            
        # Print configuration summary
        print(f"✓ Configuration loaded successfully")
        print(f"  - Min chapter length: {config['book_settings']['min_chapter_length']} words")
        print(f"  - Research enabled: {config['book_settings']['enable_research']}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to load configuration: {str(e)}")
        return False
        
def test_google_search():
    """Test Google Custom Search API"""
    print("\nTesting Google Custom Search API...")
    
    try:
        # Create research agent
        research_agent = ResearchAgent()
        
        # Check if API keys are configured
        if not research_agent.google_api_key or not research_agent.google_cse_id:
            print("ERROR: Google API key or CSE ID not configured")
            return False
            
        # Test search
        results = research_agent.google_search("Paul Atreides Dune", 2)
        
        if not results:
            print("ERROR: No search results returned")
            return False
            
        print(f"✓ Google search successful")
        print(f"  - Found {len(results)} results")
        print(f"  - First result: {results[0]['title']}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Google search failed: {str(e)}")
        return False
        
def test_wikipedia_search():
    """Test Wikipedia API"""
    print("\nTesting Wikipedia API...")
    
    try:
        # Create research agent
        research_agent = ResearchAgent()
        
        # Test search
        result = research_agent.wikipedia_search("Paul Atreides")
        
        if not result:
            print("ERROR: No Wikipedia results returned")
            return False
            
        print(f"✓ Wikipedia search successful")
        print(f"  - Result length: {len(result)} characters")
        print(f"  - Preview: {result[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Wikipedia search failed: {str(e)}")
        return False
        
def main():
    """Run all tests"""
    print("=== Testing AutoGen Book Generator Configuration ===\n")
    
    tests = [
        test_env_file,
        test_config_loading,
        test_google_search,
        test_wikipedia_search
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
        
    # Print summary
    print("=== Test Summary ===")
    for i, (test, result) in enumerate(zip(tests, results)):
        print(f"{i+1}. {test.__name__}: {'PASS' if result else 'FAIL'}")
        
    # Overall result
    if all(results):
        print("\nAll tests passed! The system is configured correctly.")
        return 0
    else:
        print("\nSome tests failed. Please fix the issues before running the book generator.")
        return 1
        
if __name__ == "__main__":
    sys.exit(main())
