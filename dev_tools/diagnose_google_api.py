"""Diagnostic script for Google Custom Search API"""
import os
import sys
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def check_env_variables():
    """Check if required environment variables are set"""
    print("Checking environment variables...")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cse_id = os.getenv("GOOGLE_CSE_ID")
    
    if not google_api_key:
        print("ERROR: GOOGLE_API_KEY is not set in .env file")
        return False
    else:
        print(f"✓ GOOGLE_API_KEY is set: {google_api_key[:5]}...{google_api_key[-3:]}")
    
    if not google_cse_id:
        print("ERROR: GOOGLE_CSE_ID is not set in .env file")
        return False
    else:
        print(f"✓ GOOGLE_CSE_ID is set: {google_cse_id}")
    
    return True

def test_direct_api_call():
    """Test Google Custom Search API directly using requests"""
    print("\nTesting direct API call to Google Custom Search...")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cse_id = os.getenv("GOOGLE_CSE_ID")
    
    if not google_api_key or not google_cse_id:
        print("ERROR: API key or CSE ID not set. Skipping direct API test.")
        return False
    
    # Construct the API URL
    query = "Paul Atreides Dune"
    url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_cse_id}&q={query}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Check for errors
        if "error" in data:
            error = data["error"]
            print(f"ERROR: API returned error: {error.get('message', 'Unknown error')}")
            print(f"Error details: {error}")
            return False
        
        # Check if we got search results
        if "items" in data:
            print(f"✓ API call successful! Found {len(data['items'])} results")
            print(f"  First result: {data['items'][0]['title']}")
            return True
        else:
            print("WARNING: API call succeeded but no results were returned")
            print(f"Response: {data}")
            return False
            
    except Exception as e:
        print(f"ERROR: Exception during API call: {str(e)}")
        return False

def check_api_quota():
    """Check if the API quota has been exceeded"""
    print("\nChecking API quota information...")
    
    google_api_key = os.getenv("GOOGLE_API_KEY")
    google_cse_id = os.getenv("GOOGLE_CSE_ID")
    
    if not google_api_key or not google_cse_id:
        print("ERROR: API key or CSE ID not set. Skipping quota check.")
        return False
    
    # Make a minimal API call to check quota
    url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={google_cse_id}&q=test&num=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Check for quota errors
        if "error" in data:
            error = data["error"]
            if error.get("code") == 403 and "quota" in error.get("message", "").lower():
                print("ERROR: API quota has been exceeded")
                print(f"Error message: {error.get('message')}")
                return False
        
        print("✓ API quota appears to be available")
        return True
            
    except Exception as e:
        print(f"ERROR: Exception during quota check: {str(e)}")
        return False

def main():
    """Run all diagnostic tests"""
    print("=== Google Custom Search API Diagnostics ===\n")
    
    # Check environment variables
    env_ok = check_env_variables()
    if not env_ok:
        print("\nPlease check your .env file and ensure GOOGLE_API_KEY and GOOGLE_CSE_ID are set correctly.")
    
    # Test direct API call
    api_ok = test_direct_api_call()
    if not api_ok and env_ok:
        # If environment variables are set but API call failed, check quota
        quota_ok = check_api_quota()
        if not quota_ok:
            print("\nYour API quota may have been exceeded. The free tier allows 100 queries per day.")
            print("You may need to wait until tomorrow or enable billing in your Google Cloud project.")
    
    # Print summary and recommendations
    print("\n=== Diagnostic Summary ===")
    if not env_ok:
        print("❌ Environment variables not properly set")
        print("   - Please check your .env file")
        print("   - Make sure GOOGLE_API_KEY and GOOGLE_CSE_ID are set correctly")
    elif not api_ok:
        print("❌ API call failed")
        print("   - Check if the API is enabled in your Google Cloud project")
        print("   - Verify that your API key has access to the Custom Search API")
        print("   - Check if your quota has been exceeded")
    else:
        print("✓ All tests passed! Your Google Custom Search API is working correctly.")
    
    print("\nFor detailed setup instructions, please refer to README_API_SETUP.md")
    
    return 0 if env_ok and api_ok else 1

if __name__ == "__main__":
    sys.exit(main())
