# Setting Up API Keys for AutoGen Book Generator

This guide will help you set up the necessary API keys for the AutoGen Book Generator to use real web research capabilities.

## Google Custom Search API Setup

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click on "Select a project" at the top of the page
   - Click "NEW PROJECT" in the popup
   - Enter a name for your project and click "CREATE"

2. **Enable the Custom Search API**:
   - In your new project, go to "APIs & Services" > "Library"
   - Search for "Custom Search API"
   - Click on "Custom Search API" in the results
   - Click "ENABLE"

3. **Create API Key**:
   - Go to "APIs & Services" > "Credentials"
   - Click "CREATE CREDENTIALS" and select "API key"
   - Copy your API key (you'll need it later)

4. **Set Up Custom Search Engine**:
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/create)
   - Enter a name for your search engine (e.g., "Dune Research")
   - Under "Sites to search", add these Dune-related sites:
     - `wiki.dune.fandom.com/*`
     - `dune.fandom.com/*`
     - `en.wikipedia.org/wiki/Dune*`
   - You can also select "Search the entire web" if you want broader results
   - Click "CREATE"

5. **Get Your Search Engine ID**:
   - After creating your search engine, you'll be taken to the control panel
   - Look for "Search engine ID" (it will look something like `012345678901234567890:abcdefghijk`)
   - Copy this ID (you'll need it later)

## Setting Up Your .env File

1. Create a file named `.env` in the root directory of the project
2. Add the following content, replacing the placeholder values with your actual API keys:

```
# API Keys for Web Research
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_search_engine_id_here

# LLM Configuration
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=not-needed

# Book Generation Settings
MIN_CHAPTER_LENGTH=3000
MAX_RETRIES=3
```

## Testing Your Configuration

After setting up your API keys, run the test script to verify everything is working correctly:

```
test_config.bat
```

If all tests pass, you're ready to generate a book with real web research capabilities!

## Troubleshooting

If you encounter any issues with the API keys:

1. **Check your .env file**: Make sure the API keys are correctly formatted with no extra spaces
2. **Verify API key permissions**: Make sure your Google API key has access to the Custom Search API
3. **Check quota limits**: Google's free tier allows 100 search queries per day
4. **Check billing**: If you need more queries, you may need to enable billing on your Google Cloud project

## Running the Book Generator

Once your API keys are set up and tested, you can run the book generator:

```
generate_book.bat
```

This will generate a book with chapters that incorporate real research about the Dune universe.
