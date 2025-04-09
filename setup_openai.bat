@echo off
echo Setting up AutoGen Book Generator with OpenAI...
echo.

:: Check if .env file already exists
if exist .env (
    echo .env file already exists.
    set /p overwrite=Do you want to overwrite it? (Y/N): 
    if /i "%overwrite%" neq "Y" (
        echo Operation cancelled.
        pause
        exit /b 0
    )
)

:: Prompt for API keys
echo Please enter your Google API Key:
set /p google_api_key="> "

echo.
echo Please enter your Google Custom Search Engine ID (default: 67d4cccf896f14e0a):
set /p google_cse_id="> "
if "%google_cse_id%"=="" set google_cse_id=67d4cccf896f14e0a

echo.
echo Please enter your OpenAI API Key (starts with sk-):
set /p openai_api_key="> "

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

:: Create .env file
echo Creating .env file...
(
    echo # API Keys for Web Research
    echo GOOGLE_API_KEY=%google_api_key%
    echo GOOGLE_CSE_ID=%google_cse_id%
    echo.
    echo # LLM Configuration - OpenAI
    echo LLM_BASE_URL=https://api.openai.com/v1
    echo LLM_API_KEY=%openai_api_key%
    echo OPENAI_MODEL=%openai_model%
    echo.
    echo # Book Generation Settings
    echo MIN_CHAPTER_LENGTH=3000
    echo MAX_RETRIES=3
) > .env

echo.
echo .env file created successfully with OpenAI configuration!
echo Selected model: %openai_model%
echo.
pause
