@echo off
echo Debug Mode - OpenAI Book Generator
echo ================================
echo.

:: Enable echo to see each command
echo on

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run with debug output
python -u main_updated.py

:: Disable echo
@echo off

echo.
echo If you see this message, the program has completed.
echo Check the book_output directory for results.
echo.
pause
