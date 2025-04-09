@echo off
echo Starting AutoGen Book Generator with fixed configuration...
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the updated main script
python main_updated.py

echo.
echo Book generation complete! Check the book_output directory for results.
echo.
pause
