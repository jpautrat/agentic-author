@echo off
echo Local LM Studio Book Generator
echo ===========================
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install required packages if not already installed
echo Checking for required packages...
pip install requests python-dotenv

:: Run the local book generator
echo.
echo Starting local LM Studio book generator...
echo.
echo IMPORTANT: Make sure LM Studio is running with the API server enabled!
echo (In LM Studio, click "Local Server" and ensure it's running)
echo.
python local_book_generator.py

echo.
echo Process complete. Check the book_output directory for results.
echo.
pause
