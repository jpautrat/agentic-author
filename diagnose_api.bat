@echo off
echo Diagnosing Google Custom Search API issues...
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the diagnostic script
python diagnose_google_api.py

echo.
echo If you need to set up your API keys, please follow the instructions in README_API_SETUP.md
echo.
pause
