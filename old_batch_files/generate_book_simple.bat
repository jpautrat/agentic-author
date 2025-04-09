@echo off
echo Starting AutoGen Book Generator with simplified research agent...
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the main script
python main_updated.py

echo.
echo Book generation complete! Check the book_output directory for results.
echo.
pause
