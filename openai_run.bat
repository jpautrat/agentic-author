@echo off
echo Setting up OpenAI and running the Book Generator...
echo.

:: Prevent the window from closing on error
set "errorlevel="

:: Prompt for OpenAI API key
echo Please enter your OpenAI API Key (starts with sk-):
set /p OPENAI_API_KEY="> "

:: Choose model
echo.
echo Choose an OpenAI model:
echo 1. gpt-4 (Best quality, most expensive)
echo 2. gpt-4-turbo (Faster version of GPT-4)
echo 3. gpt-3.5-turbo (Cheaper, less capable)
echo 4. gpt-3.5-turbo-16k (Cheaper with longer context)
set /p model_choice="> "

if "%model_choice%"=="1" (
    set OPENAI_MODEL=gpt-4
) else if "%model_choice%"=="2" (
    set OPENAI_MODEL=gpt-4-turbo
) else if "%model_choice%"=="3" (
    set OPENAI_MODEL=gpt-3.5-turbo
) else if "%model_choice%"=="4" (
    set OPENAI_MODEL=gpt-3.5-turbo-16k
) else (
    echo Invalid choice. Using default (gpt-4).
    set OPENAI_MODEL=gpt-4
)

:: Create .env file
echo.
echo Creating .env file...
(
    echo # API Keys for Web Research
    echo GOOGLE_API_KEY=your_google_api_key_here
    echo GOOGLE_CSE_ID=67d4cccf896f14e0a
    echo.
    echo # LLM Configuration - OpenAI
    echo LLM_BASE_URL=https://api.openai.com/v1
    echo LLM_API_KEY=%OPENAI_API_KEY%
    echo OPENAI_MODEL=%OPENAI_MODEL%
    echo.
    echo # Book Generation Settings
    echo MIN_CHAPTER_LENGTH=3000
    echo MAX_RETRIES=3
) > .env

echo .env file created.
echo.

:: Try to activate virtual environment
echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

:: Run the updated main script with OpenAI
echo.
echo Running AutoGen Book Generator with OpenAI...
echo API Key: %OPENAI_API_KEY:~0,5%...%OPENAI_API_KEY:~-3%
echo Model: %OPENAI_MODEL%
echo.

:: Run with error handling
python main_updated.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: The program encountered an error (code %errorlevel%).
    echo Please check the error message above.
    echo.
)

echo.
echo Process completed. Check the book_output directory for results.
echo.
pause
