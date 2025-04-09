@echo off
echo Running AutoGen Book Generator with OpenAI...
echo.

:: Check if OPENAI_API_KEY environment variable is set
if "%OPENAI_API_KEY%"=="" (
    echo OPENAI_API_KEY environment variable is not set.
    echo Please run setup_openai_env.bat first.
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the updated main script with OpenAI
python main_updated.py

echo.
echo Book generation complete! Check the book_output directory for results.
echo.
pause
