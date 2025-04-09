@echo off
echo Testing OpenAI API connection...
echo.

:: Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found.
    echo Running with system Python...
)

:: Run the test script
python direct_openai.py

echo.
pause
