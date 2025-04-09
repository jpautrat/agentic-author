# AutoGen Book Generator - Enhanced Version

This is an enhanced version of the AutoGen Book Generator, a Python system that uses multiple AI agents to collaboratively write complete books. The system has been improved to address several key issues:

1. **Web Research Capabilities**: The system now includes a research agent that can search the web for information about the Dune universe and other topics to ensure accuracy and depth in the generated content.

2. **Longer Chapter Lengths**: Chapters are now required to be at least 3000 words long, with verification to ensure this minimum length is met.

3. **Better Prompt Adherence**: The system has been enhanced to ensure the story stays focused on the initial prompt, particularly maintaining the relationship between Jeff and Paul Atreides.

4. **Style Consistency**: The writer and editor agents now enforce Frank Herbert's distinctive writing style from the Dune series.

## Setup Instructions

### 1. Environment Setup

First, create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API Keys Configuration

Create a `.env` file in the project root directory based on the provided `.env.template`:

```
# API Keys for Web Research
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_custom_search_engine_id_here

# LLM Configuration
LLM_BASE_URL=http://localhost:1234/v1
LLM_API_KEY=not-needed

# Book Generation Settings
MIN_CHAPTER_LENGTH=3000  # Minimum words per chapter
MAX_RETRIES=3  # Maximum retry attempts for failed chapters
```

#### Google Custom Search API Setup:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Custom Search API
4. Create credentials (API key)
5. Go to [Google Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/create)
6. Create a new search engine
7. Under "Sites to search", add relevant Dune-related sites:
   - wiki.dune.fandom.com/*
   - dune.fandom.com/*
   - en.wikipedia.org/wiki/Dune*
8. Copy your Search Engine ID (cx)

### 3. Test Configuration

Run the test script to verify your configuration:

```bash
python test_config.py
```

This will check if your `.env` file is properly set up and if the API keys are working correctly.

## Usage

### Running the Book Generator

To generate a book with the default settings:

```bash
python main_updated.py
```

The system will:
1. Generate a detailed chapter outline
2. Research relevant information about the Dune universe
3. Generate each chapter with a minimum of 3000 words
4. Save the output in the `book_output` directory

### Customizing the Book Generation

You can modify the initial prompt in `main_updated.py` to generate different stories. The current prompt is set up to create a story about Jeff, a friend of Paul Atreides in the Dune universe.

You can also adjust the number of chapters by changing the `num_chapters` variable in `main_updated.py`.

## System Components

The system employs specialized agents including:

- **Story Planner**: Creates high-level story arcs and plot points
- **World Builder**: Establishes and maintains consistent settings
- **Memory Keeper**: Tracks continuity and story context
- **Researcher**: Gathers factual information about the Dune universe
- **Writer**: Generates the actual prose in Frank Herbert's style
- **Editor**: Reviews and improves content for quality and consistency
- **Outline Creator**: Creates detailed chapter outlines

## Output

Generated content is saved in the `book_output` directory:
```
book_output/
├── outline.txt
├── chapter_01.txt
├── chapter_02.txt
└── ...
```

## Requirements

- Python 3.8+
- AutoGen 0.2.0+
- Google API Python Client
- Wikipedia API
- Other dependencies listed in requirements.txt
