@echo off
echo Windows-Compatible Book Generator
echo ==============================
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Run the Windows-compatible book generator
echo.
echo Starting book generator...
python windows_book_generator.py

echo.
echo Process complete. Check the book_output directory for results.
echo.
pause
