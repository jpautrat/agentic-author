@echo off
echo Simple GitHub Push Helper
echo =======================
echo.
echo This script will help you push to GitHub.
echo.
echo 1. Make sure you have a GitHub Personal Access Token
echo 2. When prompted for your password, enter your token (not your GitHub password)
echo.
echo Press any key to continue...
pause > nul

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo Done! If successful, check your repository at:
echo https://github.com/jpautrat/agentic-author
echo.
pause
