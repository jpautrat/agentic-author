@echo off
echo Running Debug Version of Book Generator
echo =====================================
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Run debug script
echo.
echo Running debug script...
python debug_main.py

echo.
echo Debug complete. Check debug_log.txt for details.
echo.
pause
