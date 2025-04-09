@echo off
echo Fixed Book Generator
echo ===================
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Run the fixed book generator
echo.
echo Starting fixed book generator...
python fixed_book_generator.py

echo.
echo Process complete. Check the book_output directory for results.
echo.
pause
