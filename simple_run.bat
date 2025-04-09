@echo off
echo Simple OpenAI Book Generator Runner
echo ================================
echo.

:: Create .env file with the API key from the test
echo Using API key from previous test...
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Run with command line arguments instead of environment variables
echo.
echo Running book generator...
python main_updated.py

echo.
echo If you see this message, the program has completed.
echo Check the book_output directory for results.
echo.
pause
