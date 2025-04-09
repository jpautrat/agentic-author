@echo off
echo Pushing to GitHub...
echo.
echo Please enter your GitHub Personal Access Token when prompted.
echo.

set /p TOKEN="Enter your GitHub Personal Access Token: "

echo.
echo Setting up remote with token...
git remote set-url origin https://jpautrat:%TOKEN%@github.com/jpautrat/agentic-author.git

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo Resetting remote URL for security...
git remote set-url origin https://github.com/jpautrat/agentic-author.git

echo.
echo Done! Check your repository at https://github.com/jpautrat/agentic-author
echo.
pause
