@echo off
echo Claude-Powered Book Generator (Updated)
echo ==================================
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install required packages if not already installed
echo Checking for required packages...
pip install anthropic requests openai python-dotenv

:: Run the Claude-powered book generator
echo.
echo Starting Claude-powered book generator with latest models...
python claude_book_generator.py

echo.
echo Process complete. Check the book_output directory for results.
echo.
pause
