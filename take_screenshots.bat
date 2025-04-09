@echo off
echo Agentic Author Screenshot Helper
echo ==============================
echo.
echo This script will help you take screenshots of the web UI for the README.
echo.
echo Instructions:
echo 1. The web UI will open in your default browser
echo 2. Take screenshots of the following pages:
echo    - Dashboard (main page)
echo    - Book Generation page (click "Generate New Book")
echo    - Library page (click "Book Library")
echo 3. Save the screenshots as:
echo    - docs\screenshots\dashboard.png
echo    - docs\screenshots\generate.png
echo    - docs\screenshots\library.png
echo.
echo Press any key to start the web UI...
pause > nul

echo Starting web UI...
start "" "run_with_ui.bat"

echo.
echo Web UI started! Please take the screenshots as instructed.
echo.
echo After taking the screenshots, press any key to continue...
pause > nul

echo.
echo Thank you! The screenshots will be used in the README.
echo.
echo Next steps:
echo 1. Commit and push the changes to GitHub:
echo    git add .
echo    git commit -m "Add screenshots and clean up repository"
echo    git push
echo.
pause
