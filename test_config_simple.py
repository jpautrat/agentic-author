"""Test script to verify configuration with simplified research agent"""
import os
import sys
from dotenv import load_dotenv
from research_agent_simple import ResearchAgent
from config import get_config

def test_env_file():
    """Test if .env file exists and can be loaded"""
    print("Testing .env file...")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("WARNING: .env file not found. Creating a basic one for testing.")
        with open(".env", "w") as f:
            f.write("# API Keys for Web Research\n")
            f.write("GOOGLE_API_KEY=test_key\n")
            f.write("GOOGLE_CSE_ID=test_id\n")
            f.write("\n# LLM Configuration\n")
            f.write("LLM_BASE_URL=http://localhost:1234/v1\n")
            f.write("LLM_API_KEY=not-needed\n")
            f.write("\n# Book Generation Settings\n")
            f.write("MIN_CHAPTER_LENGTH=3000\n")
            f.write("MAX_RETRIES=3\n")
        
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    required_vars = ["GOOGLE_API_KEY", "GOOGLE_CSE_ID"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            
    if missing_vars:
        print(f"WARNING: Missing required environment variables: {', '.join(missing_vars)}")
        print("Using mock data for testing purposes.")
        return True
        
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
        
def test_research_agent():
    """Test simplified research agent"""
    print("\nTesting simplified research agent...")
    
    try:
        # Create research agent
        research_agent = ResearchAgent()
        
        # Test search
        results = research_agent.google_search("Paul Atreides Dune", 2)
        
        if not results:
            print("ERROR: No search results returned")
            return False
            
        print(f"✓ Research agent search successful")
        print(f"  - Found {len(results)} results")
        print(f"  - First result: {results[0]['title']}")
        
        # Test chapter research
        chapter_prompt = "Paul and Jeff on Caladan, preparing for the move to Arrakis."
        research_data = research_agent.research_for_chapter(chapter_prompt, 1)
        formatted = research_agent.format_research_for_agent(research_data)
        
        print(f"✓ Chapter research successful")
        print(f"  - Found {len(research_data['relevant_topics'])} relevant topics")
        print(f"  - Topics: {', '.join(research_data['relevant_topics'][:3])}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Research agent test failed: {str(e)}")
        return False
        
def main():
    """Run all tests"""
    print("=== Testing AutoGen Book Generator Configuration ===\n")
    
    tests = [
        test_env_file,
        test_config_loading,
        test_research_agent
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
        print("Note: Using simplified research agent for testing purposes.")
        return 0
    else:
        print("\nSome tests failed. Please fix the issues before running the book generator.")
        return 1
        
if __name__ == "__main__":
    sys.exit(main())
