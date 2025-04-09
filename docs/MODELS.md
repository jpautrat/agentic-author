# AI Models Reference Guide

This document provides detailed information about the AI models supported by the Advanced AI Book Generator and their characteristics.

## OpenAI Models

### GPT-4

- **Description**: OpenAI's most powerful model, with strong reasoning and writing capabilities
- **Context Window**: 8,192 tokens
- **Max Output Tokens**: 4,096 tokens
- **Strengths**: High-quality writing, complex reasoning, adherence to instructions
- **Limitations**: More expensive, slower generation
- **Best For**: High-quality books where cost is not a concern
- **Approximate Cost**: $0.03-$0.06 per 1K tokens

### GPT-4 Turbo

- **Description**: Faster version of GPT-4 with similar capabilities
- **Context Window**: 128,000 tokens
- **Max Output Tokens**: 4,096 tokens
- **Strengths**: Similar quality to GPT-4, faster, larger context window
- **Limitations**: Still relatively expensive
- **Best For**: Longer books that need to reference earlier chapters
- **Approximate Cost**: $0.01-$0.03 per 1K tokens

### GPT-3.5 Turbo

- **Description**: Balanced model with good performance at lower cost
- **Context Window**: 4,096 tokens
- **Max Output Tokens**: 4,096 tokens
- **Strengths**: Fast, cost-effective, decent quality
- **Limitations**: Less sophisticated writing, may struggle with complex instructions
- **Best For**: Testing, drafts, or budget-conscious projects
- **Approximate Cost**: $0.0015-$0.002 per 1K tokens

### GPT-3.5 Turbo 16K

- **Description**: Extended context version of GPT-3.5 Turbo
- **Context Window**: 16,384 tokens
- **Max Output Tokens**: 4,096 tokens
- **Strengths**: Larger context window at reasonable cost
- **Limitations**: Same quality limitations as GPT-3.5 Turbo
- **Best For**: Longer books on a budget
- **Approximate Cost**: $0.003-$0.004 per 1K tokens

## Anthropic Claude Models

### Claude 3.7 Sonnet (Extended Thinking)

- **Description**: Claude model with extended thinking capability
- **Context Window**: 200,000 tokens
- **Max Output Tokens**: 64,000 tokens
- **Strengths**: Extremely long outputs, high quality, large context window
- **Limitations**: Can be slower, higher cost
- **Best For**: Generating very long, detailed chapters
- **Approximate Cost**: Varies based on usage

### Claude 3.5 Sonnet

- **Description**: High-quality Claude model with good balance
- **Context Window**: 200,000 tokens
- **Max Output Tokens**: 8,192 tokens
- **Strengths**: High-quality output, large context window
- **Limitations**: Limited output length compared to 3.7
- **Best For**: High-quality books with moderate chapter length
- **Approximate Cost**: Varies based on usage

### Claude 3.5 Haiku

- **Description**: Faster Claude model
- **Context Window**: 200,000 tokens
- **Max Output Tokens**: 8,192 tokens
- **Strengths**: Faster generation, large context window
- **Limitations**: Lower quality than Sonnet or Opus
- **Best For**: Faster generation when quality is less critical
- **Approximate Cost**: Lower than Sonnet/Opus

### Claude 3 Opus

- **Description**: Highest quality Claude model
- **Context Window**: 180,000 tokens
- **Max Output Tokens**: 4,096 tokens
- **Strengths**: Highest quality writing and reasoning
- **Limitations**: More expensive, limited output length
- **Best For**: Highest quality books where output length is not critical
- **Approximate Cost**: Highest among Claude models

### Claude 3 Sonnet

- **Description**: Balanced Claude model
- **Context Window**: 180,000 tokens
- **Max Output Tokens**: 4,096 tokens
- **Strengths**: Good balance of quality and performance
- **Limitations**: Limited output length
- **Best For**: General purpose book generation
- **Approximate Cost**: Moderate

## Local LM Studio Models

LM Studio supports various open-source models. Here are some recommended options:

### Mistral 7B Instruct

- **Description**: Efficient 7B parameter model with good instruction following
- **Context Window**: Varies by implementation (typically 8K-32K)
- **Strengths**: Good balance of quality and performance, runs on consumer hardware
- **Limitations**: Lower quality than commercial models
- **Best For**: Local generation on machines with 16GB+ RAM
- **Hardware Requirements**: 16GB RAM, GPU recommended

### Llama 2 13B Chat

- **Description**: Meta's 13B parameter chat model
- **Context Window**: Varies by implementation (typically 4K)
- **Strengths**: Better quality than 7B models
- **Limitations**: Requires more RAM, slower without GPU
- **Best For**: Higher quality local generation
- **Hardware Requirements**: 24GB+ RAM, GPU strongly recommended

### Mixtral 8x7B Instruct

- **Description**: Mixture of experts model with strong capabilities
- **Context Window**: Varies by implementation
- **Strengths**: Near commercial-quality results
- **Limitations**: Very high resource requirements
- **Best For**: High-quality local generation on powerful hardware
- **Hardware Requirements**: 32GB+ RAM, powerful GPU required

### Phi-2

- **Description**: Microsoft's efficient small model
- **Context Window**: 2K tokens
- **Strengths**: Very efficient, runs on modest hardware
- **Limitations**: Limited context, lower quality
- **Best For**: Testing on lower-end hardware
- **Hardware Requirements**: 8GB RAM minimum

## Model Selection Guide

### For Highest Quality

1. Claude 3 Opus (cloud)
2. GPT-4 (cloud)
3. Claude 3.7 Sonnet (cloud)
4. Mixtral 8x7B (local, with powerful hardware)

### For Longest Chapters

1. Claude 3.7 Sonnet (64K tokens output)
2. Claude 3.5 models (8K tokens output)
3. GPT-4 models (4K tokens output)

### For Fastest Generation

1. Claude 3.5 Haiku (cloud)
2. GPT-3.5 Turbo (cloud)
3. Phi-2 (local)
4. Mistral 7B (local)

### For Offline Use (No API Keys)

1. Mixtral 8x7B (high-end hardware)
2. Llama 2 13B (mid-range hardware)
3. Mistral 7B (standard hardware)
4. Phi-2 (budget hardware)

## Token Usage Estimation

For planning purposes, use these estimates:

- 1 word ≈ 1.3 tokens
- 1 page (500 words) ≈ 650 tokens
- 1 chapter (5,000 words) ≈ 6,500 tokens
- Full novel (80,000 words) ≈ 104,000 tokens

## Hardware Requirements for Local Models

| Model | RAM | GPU | Disk Space |
|-------|-----|-----|------------|
| Phi-2 | 8GB+ | Optional | 2GB |
| Mistral 7B | 16GB+ | Recommended | 4GB |
| Llama 2 13B | 24GB+ | Recommended | 7GB |
| Mixtral 8x7B | 32GB+ | Required | 15GB |
