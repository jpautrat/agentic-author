@echo off
echo Customizable Book Generator
echo =========================
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Run the customizable book generator
echo.
echo Starting customizable book generator...
python custom_book_generator.py

echo.
echo Process complete. Check the book_output directory for results.
echo.
pause
