@echo off
echo Agentic Author GitHub Push Helper
echo ===============================
echo.
echo This script will help you commit and push your changes to GitHub.
echo.

:: Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/downloads
    goto :error
)

:: Check if screenshots exist
if not exist "docs\screenshots\dashboard.png" (
    echo WARNING: Missing screenshot docs\screenshots\dashboard.png
    echo You should run take_screenshots.bat first to create the screenshots.
    echo.
    set /p continue=Do you want to continue anyway? (y/n): 
    if /i not "%continue%"=="y" goto :end
)

:: Initialize git repository if not already initialized
if not exist .git (
    echo Initializing git repository...
    git init
    if %ERRORLEVEL% NEQ 0 goto :git_error
) else (
    echo Git repository already initialized.
)

:: Add all files to git
echo.
echo Adding files to git...
git add .
if %ERRORLEVEL% NEQ 0 goto :git_error

:: Get commit message from user
echo.
set /p commit_msg=Enter commit message (or press Enter for default): 
if "%commit_msg%"=="" set commit_msg=Update Agentic Author with Web UI and screenshots

:: Commit changes
echo.
echo Committing changes with message: "%commit_msg%"
git commit -m "%commit_msg%"
if %ERRORLEVEL% NEQ 0 goto :git_error

:: Check if remote exists
git remote -v | findstr "origin" >nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Adding remote repository...
    git remote add origin https://github.com/jpautrat/agentic-author.git
    if %ERRORLEVEL% NEQ 0 goto :git_error
)

:: Push to GitHub
echo.
echo Pushing to GitHub...
git push -u origin main
if %ERRORLEVEL% NEQ 0 goto :git_error

echo.
echo Success! Your changes have been pushed to GitHub.
echo.
echo Repository URL: https://github.com/jpautrat/agentic-author
echo.
goto :end

:git_error
echo.
echo ERROR: Git command failed with error code %ERRORLEVEL%.
echo Please check the error message above and try again.
goto :end

:error
echo.
echo ERROR: Script failed. Please fix the errors and try again.

:end
pause
