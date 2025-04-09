@echo off
echo Publishing Agentic Author to GitHub...
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
copy /Y requirements_with_ui.txt requirements.txt
copy /Y .gitignore_updated .gitignore

:: Ensure all batch files are executable
echo Setting file permissions...
attrib +x *.bat

:: Initialize git repository if not already initialized
echo Initializing git repository...
if not exist .git (
    git init
) else (
    echo Git repository already initialized
)

:: Add all files to git
echo Adding files to git...
git add .

:: Commit changes
echo Committing changes...
git commit -m "Initial commit of Agentic Author with Web UI"

:: Add remote repository
echo Adding remote repository...
git remote add origin https://github.com/jpautrat/agentic-author.git

:: Push to GitHub
echo Pushing to GitHub...
git push -u origin main

echo.
echo Publication complete! Your project has been pushed to GitHub.
echo.
echo Repository URL: https://github.com/jpautrat/agentic-author
echo.
pause
