@echo off
echo Pull and Push Helper
echo ===================
echo.
echo This script will pull changes from GitHub and then push your changes.
echo.
echo 1. Make sure you have a GitHub Personal Access Token
echo 2. When prompted for your password, enter your token (not your GitHub password)
echo.
echo Press any key to continue...
pause > nul

echo.
echo Pulling from GitHub...
git pull origin main

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo Done! If successful, check your repository at:
echo https://github.com/jpautrat/agentic-author
echo.
pause
