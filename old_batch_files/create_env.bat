@echo off
echo Creating .env file for AutoGen Book Generator...
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
echo Please enter your Google Custom Search Engine ID:
set /p google_cse_id="> "

:: Create .env file
echo Creating .env file...
(
    echo # API Keys for Web Research
    echo GOOGLE_API_KEY=%google_api_key%
    echo GOOGLE_CSE_ID=%google_cse_id%
    echo.
    echo # LLM Configuration
    echo LLM_BASE_URL=http://localhost:1234/v1
    echo LLM_API_KEY=not-needed
    echo.
    echo # Book Generation Settings
    echo MIN_CHAPTER_LENGTH=3000
    echo MAX_RETRIES=3
) > .env

echo.
echo .env file created successfully!
echo.
pause
