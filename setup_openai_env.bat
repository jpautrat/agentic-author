@echo off
echo Setting up OpenAI environment variables...
echo.

:: Prompt for OpenAI API key
echo Please enter your OpenAI API Key (starts with sk-):
set /p openai_api_key="> "

:: Choose model
echo.
echo Choose an OpenAI model:
echo 1. gpt-4 (Best quality, most expensive)
echo 2. gpt-4-turbo (Faster version of GPT-4)
echo 3. gpt-3.5-turbo (Cheaper, less capable)
echo 4. gpt-3.5-turbo-16k (Cheaper with longer context)
set /p model_choice="> "

if "%model_choice%"=="1" (
    set openai_model=gpt-4
) else if "%model_choice%"=="2" (
    set openai_model=gpt-4-turbo
) else if "%model_choice%"=="3" (
    set openai_model=gpt-3.5-turbo
) else if "%model_choice%"=="4" (
    set openai_model=gpt-3.5-turbo-16k
) else (
    echo Invalid choice. Using default (gpt-4).
    set openai_model=gpt-4
)

:: Set environment variables
echo.
echo Setting environment variables...
setx OPENAI_API_KEY "%openai_api_key%"
setx OPENAI_MODEL "%openai_model%"

echo.
echo Environment variables set:
echo OPENAI_API_KEY: %openai_api_key%
echo OPENAI_MODEL: %openai_model%
echo.
echo Please restart your command prompt for these changes to take effect.
echo.
pause
