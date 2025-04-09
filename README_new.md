# Advanced AI Book Generator

A sophisticated AI-powered book generation system that creates complete novels in the style of famous authors. This project extends and enhances [Adam Larson's original AI Book Writer](https://github.com/adamwlarson/ai-book-writer) with multiple new features and improvements.

## 🌟 Key Features

- **Multiple AI Provider Support**:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic Claude (with extended thinking capability)
  - Local LLMs via LM Studio (no API keys needed)

- **Customizable Book Parameters**:
  - Adjustable chapter length
  - Configurable number of scenes per chapter
  - Control over total chapter count
  - Temperature settings for creativity

- **Enhanced Generation Quality**:
  - Improved prompting for better adherence to writing style
  - Automatic chapter extension for consistent length
  - Web research integration for factual accuracy
  - Resilient API handling with automatic retries

- **Professional Output**:
  - Complete book with title page and table of contents
  - Properly formatted chapters with epigraphs
  - Consistent character development
  - Cohesive narrative structure

## 📋 Requirements

### For Cloud API Version
- Python 3.8+
- OpenAI API key and/or Anthropic API key
- Required Python packages (see requirements.txt)

### For Local LLM Version
- Python 3.8+
- [LM Studio](https://lmstudio.ai/) with a downloaded model
- Sufficient RAM for your chosen model (8GB+ recommended)
- GPU acceleration recommended but not required

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/advanced-ai-book-generator.git
cd advanced-ai-book-generator

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Using OpenAI API

```bash
# Set up OpenAI configuration
setup_openai.bat  # Windows
# OR
./setup_openai.sh  # macOS/Linux

# Run the generator
openai_run.bat  # Windows
# OR
./openai_run.sh  # macOS/Linux
```

#### Using Anthropic Claude API

```bash
# Run the Claude-powered generator
claude_book_resilient.bat  # Windows
# OR
./claude_book_resilient.sh  # macOS/Linux
```

#### Using Local LM Studio

```bash
# First, start LM Studio and enable the local server

# Then run the local generator
local_book.bat  # Windows
# OR
./local_book.sh  # macOS/Linux
```

## 📚 Example Output

The generator creates complete novels with a structure like:

```
# THE SHADOW OF MUAD'DIB

*The untold story of Jeff, friend of Paul Atreides*

## TABLE OF CONTENTS

Chapter 1: The Shadows of Caladan
Chapter 2: Whispers of Arrakis
...

Chapter 1: The Shadows of Caladan

"The greatest loyalty is not to a ruler, but to the truth that exists between friends."
- From "Reflections on Friendship" by Princess Irulan

The morning sun cast long shadows across the training grounds of Castle Caladan...
```

## 🔧 Advanced Configuration

### Customizing Book Parameters

When running any of the generator scripts, you'll be prompted to specify:

1. Number of chapters (1-20)
2. Minimum words per chapter (1000-50000)
3. Minimum scenes per chapter (1-20)
4. Model selection
5. Temperature setting (for local models)

### Environment Variables

Create a `.env` file with the following variables:

```
# API Keys (for cloud versions)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Book Generation Settings
MIN_CHAPTER_LENGTH=5000
MAX_RETRIES=3
```

## 🧠 Architecture

The system uses several specialized agents working together:

- **Story Planner**: Creates high-level story arcs and plot points
- **World Builder**: Establishes and maintains consistent settings
- **Memory Keeper**: Tracks continuity and context
- **Writer**: Generates the actual prose
- **Editor**: Reviews and improves content
- **Outline Creator**: Creates detailed chapter outlines

## 🛠️ Implementation Details

### Multi-Provider Support

The system is designed with a flexible architecture that supports multiple AI providers:

1. **OpenAI Integration**:
   - Configurable model selection (GPT-4, GPT-3.5, etc.)
   - Optimized prompting for narrative generation
   - Automatic token management

2. **Anthropic Claude Integration**:
   - Support for Claude's extended thinking capability (up to 64K tokens)
   - Resilient error handling with automatic retries
   - Optimized for longer, more detailed chapters

3. **Local LLM Integration**:
   - Compatible with LM Studio's API
   - Works with various open-source models
   - Adjustable parameters for different hardware capabilities

### Error Handling and Resilience

The system includes robust error handling:
- Validates chapter completeness
- Ensures proper formatting
- Maintains backup copies of generated content
- Implements retry logic with exponential backoff
- Handles API overload scenarios gracefully

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

This project builds upon [Adam Larson's AI Book Writer](https://github.com/adamwlarson/ai-book-writer). We extend our gratitude for his foundational work that made this enhanced version possible.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Adam Larson](https://github.com/adamwlarson) for the original AI Book Writer project
- [AutoGen](https://github.com/microsoft/autogen) framework for multi-agent capabilities
- OpenAI and Anthropic for their powerful language models
- The LM Studio team for making local LLM inference accessible
