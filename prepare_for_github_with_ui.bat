@echo off
echo Preparing Agentic Author with Web UI for GitHub...
echo.

:: Create necessary directories
echo Creating directory structure...
mkdir docs 2>nul
mkdir docs\screenshots 2>nul
mkdir web\static\css 2>nul
mkdir web\static\js 2>nul
mkdir web\static\img 2>nul
mkdir web\templates 2>nul

:: Copy new files to replace existing ones
echo Updating documentation files...
copy /Y README_with_ui.md README.md
copy /Y requirements_updated.txt requirements.txt
copy /Y .gitignore_updated .gitignore

:: Ensure all batch files are executable
echo Setting file permissions...
attrib +x *.bat

echo.
echo Preparation complete! Your project is ready for GitHub.
echo.
echo Next steps:
echo 1. Run the web UI to generate screenshots for the README:
echo    run_with_ui.bat
echo 2. Take screenshots of the dashboard, generation page, and library
echo 3. Save the screenshots to docs/screenshots/
echo 4. Initialize a git repository if you haven't already:
echo    git init
echo 5. Add all files:
echo    git add .
echo 6. Commit your changes:
echo    git commit -m "Initial commit of Agentic Author with Web UI"
echo 7. Push your code to the existing repository:
echo    git remote add origin https://github.com/jpautrat/agentic-author.git
echo    git push -u origin main
echo.
echo Don't forget to update the LICENSE file with your name!
echo.
pause
