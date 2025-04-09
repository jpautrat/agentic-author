# Advanced AI Book Generator - Usage Guide

This document provides detailed instructions on how to use the Advanced AI Book Generator.

## Table of Contents

- [Basic Usage](#basic-usage)
- [OpenAI API Usage](#openai-api-usage)
- [Anthropic Claude Usage](#anthropic-claude-usage)
- [Local LM Studio Usage](#local-lm-studio-usage)
- [Customizing Book Parameters](#customizing-book-parameters)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

## Basic Usage

The simplest way to use the book generator is through the provided batch files:

### On Windows:

```bash
# For OpenAI API
setup_openai.bat
openai_run.bat

# For Anthropic Claude API
claude_book_resilient.bat

# For Local LM Studio
local_book.bat
```

### On macOS/Linux:

```bash
# For OpenAI API
./setup_openai.sh
./openai_run.sh

# For Anthropic Claude API
./claude_book_resilient.sh

# For Local LM Studio
./local_book.sh
```

## OpenAI API Usage

### Setup

1. Obtain an OpenAI API key from [platform.openai.com](https://platform.openai.com)
2. Run the setup script:
   ```
   setup_openai.bat  # Windows
   ./setup_openai.sh  # macOS/Linux
   ```
3. Enter your API key when prompted
4. Choose your preferred model:
   - GPT-4 (Best quality, most expensive)
   - GPT-4-turbo (Faster version of GPT-4)
   - GPT-3.5-turbo (Cheaper, less capable)
   - GPT-3.5-turbo-16k (Cheaper with longer context)

### Running

```
openai_run.bat  # Windows
./openai_run.sh  # macOS/Linux
```

## Anthropic Claude Usage

### Setup

1. Obtain an Anthropic API key from [console.anthropic.com](https://console.anthropic.com)
2. Create a `.env` file with your API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

### Running

```
claude_book_resilient.bat  # Windows
./claude_book_resilient.sh  # macOS/Linux
```

When prompted, choose your preferred Claude model:
1. claude-3-7-sonnet-20250219 (extended thinking, 64K max tokens)
2. claude-3-5-sonnet-20240620 (high quality, 8K max tokens)
3. claude-3-5-haiku-20241022 (faster, 8K max tokens)
4. claude-3-opus-20240229 (highest quality, 4K max tokens)
5. claude-3-sonnet-20240229 (balanced, 4K max tokens)

## Local LM Studio Usage

### Setup

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Download a model in LM Studio (Mistral 7B, Llama 2, etc.)
3. Start the local server in LM Studio

### Running

```
local_book.bat  # Windows
./local_book.sh  # macOS/Linux
```

When prompted:
1. Confirm the LM Studio server URL (default: http://localhost:1234/v1)
2. Enter your book parameters
3. Set the temperature (0.1-1.0, default 0.7)

## Customizing Book Parameters

When running any generator, you'll be prompted to specify:

1. **Number of chapters** (1-20)
   - Recommended: 5-10 for testing, 10-20 for full books

2. **Minimum words per chapter** (1000-50000)
   - Recommended: 2000-5000 for most models
   - For Claude 3.7 Sonnet with extended thinking: up to 30000

3. **Minimum scenes per chapter** (1-20)
   - Recommended: 3-5 for most chapters

4. **Model selection**
   - For quality: GPT-4 or Claude Opus
   - For speed: GPT-3.5 or Claude Haiku
   - For longest output: Claude 3.7 Sonnet

5. **Temperature** (for local models)
   - Higher (0.7-1.0): More creative, varied output
   - Lower (0.1-0.5): More focused, consistent output

## Advanced Configuration

### Environment Variables

Create a `.env` file with these variables:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Book Generation Settings
MIN_CHAPTER_LENGTH=5000
MAX_RETRIES=3

# Model Settings
OPENAI_MODEL=gpt-4
```

### Programmatic Usage

```python
from config import get_config
from agents import BookAgents
from book_generator import BookGenerator
from outline_generator import OutlineGenerator

# Get configuration
agent_config = get_config()

# Create agents
outline_agents = BookAgents(agent_config)
agents = outline_agents.create_agents(initial_prompt, num_chapters)

# Generate outline
outline_gen = OutlineGenerator(agents, agent_config)
outline = outline_gen.generate_outline(initial_prompt, num_chapters)

# Initialize book generator
book_agents = BookAgents(agent_config, outline)
agents_with_context = book_agents.create_agents(initial_prompt, num_chapters)
book_gen = BookGenerator(agents_with_context, agent_config, outline)

# Generate book
book_gen.generate_book(outline)
```

## Troubleshooting

### API Key Issues

- Ensure your API key is correctly entered
- Check that your API key has sufficient quota/credits
- Verify that your API key has the necessary permissions

### Connection Issues

- For OpenAI/Claude: Check your internet connection
- For LM Studio: Ensure the local server is running
- Try increasing the retry count in the configuration

### Generation Quality Issues

- Try a more capable model (GPT-4, Claude Opus)
- Increase the minimum chapter length
- Lower the temperature for more focused output
- Adjust the number of scenes per chapter

### Memory/Performance Issues

- For local models: Try a smaller model
- Reduce the chapter length for faster generation
- Close other applications to free up memory
- For GPU acceleration: Ensure drivers are up to date
