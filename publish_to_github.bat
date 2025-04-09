@echo off
echo Publishing Agentic Author to GitHub...
echo.

:: Ensure all necessary files are in place
echo Checking for required files...
if not exist "docs\screenshots\dashboard.png" (
    echo ERROR: Missing screenshot docs\screenshots\dashboard.png
    echo Please run take_screenshots.bat first to create the screenshots.
    goto :error
)
if not exist "docs\screenshots\generate.png" (
    echo ERROR: Missing screenshot docs\screenshots\generate.png
    echo Please run take_screenshots.bat first to create the screenshots.
    goto :error
)
if not exist "docs\screenshots\library.png" (
    echo ERROR: Missing screenshot docs\screenshots\library.png
    echo Please run take_screenshots.bat first to create the screenshots.
    goto :error
)

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
git commit -m "Update Agentic Author with Web UI and screenshots"

:: Add remote repository if not already added
echo Checking remote repository...
git remote -v | findstr "origin" > nul
if errorlevel 1 (
    echo Adding remote repository...
    git remote add origin https://github.com/jpautrat/agentic-author.git
)

:: Push to GitHub
echo Pushing to GitHub...
git push -u origin main

echo.
echo Publication complete! Your project has been pushed to GitHub.
echo.
echo Repository URL: https://github.com/jpautrat/agentic-author
echo.
goto :end

:error
echo.
echo Publication failed. Please fix the errors and try again.
echo.

:end
pause
