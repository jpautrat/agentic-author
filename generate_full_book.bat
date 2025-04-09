@echo off
echo Generating Full Book with Debug Logging
echo =====================================
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Run debug script for full book generation
echo.
echo Running full book generation...
python full_book_debug.py

echo.
echo Process complete. Check full_book_debug.txt for details.
echo Book output should be in the book_output directory.
echo.
pause
