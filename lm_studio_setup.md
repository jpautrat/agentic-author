# Setting Up LM Studio for Local Book Generation

This guide will help you set up LM Studio to work with the local book generator.

## Step 1: Download and Install LM Studio

1. Download LM Studio from [lmstudio.ai](https://lmstudio.ai/)
2. Install it on your computer

## Step 2: Download a Model

1. Open LM Studio
2. Go to the "Models" tab
3. Choose a model to download. Recommended models:
   - **Mistral 7B Instruct v0.2** (good balance of quality and speed)
   - **Llama 2 13B Chat** (higher quality but slower)
   - **Phi-2** (faster but lower quality)
   - **Mixtral 8x7B Instruct** (high quality but requires more RAM)

4. Click "Download" next to your chosen model

## Step 3: Start the Local Server

1. In LM Studio, select your downloaded model
2. Click on "Local Server" in the left sidebar
3. Click "Start Server"
4. Make sure the server is running at http://localhost:1234
5. You should see "Server is running" status

## Step 4: Run the Local Book Generator

1. Open a command prompt
2. Navigate to the book generator directory
3. Run the local book generator:
   ```
   local_book.bat
   ```

4. When prompted, use the default server URL (http://localhost:1234/v1) or enter your custom URL if you changed it in LM Studio

## Tips for Best Results

1. **Choose the right model**: Larger models (13B+) produce better quality text but run slower and require more RAM
2. **Adjust temperature**: Lower values (0.1-0.5) produce more focused text, higher values (0.7-1.0) produce more creative text
3. **RAM requirements**: 
   - 7B models: 8GB+ RAM
   - 13B models: 16GB+ RAM
   - Mixtral models: 32GB+ RAM
4. **GPU acceleration**: If you have a compatible NVIDIA GPU, enable GPU acceleration in LM Studio settings for much faster generation

## Troubleshooting

- **Server connection errors**: Make sure LM Studio server is running before starting the book generator
- **Out of memory errors**: Try a smaller model or reduce the context/output length
- **Slow generation**: Enable GPU acceleration if available, or use a smaller model
- **Poor quality output**: Try a larger model or reduce the temperature setting
