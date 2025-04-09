@echo off
echo Simple Book Generator
echo ===================
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Run the simple book generator
echo.
echo Starting book generator...
python simple_book_generator.py

echo.
echo Process complete. Check the book_output directory for results.
echo.
pause
