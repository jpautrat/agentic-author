@echo off
echo Pushing to Empty GitHub Repository
echo ================================
echo.
echo This script will push your files to an empty GitHub repository.
echo.
echo 1. Make sure you have already deleted the contents of your GitHub repository
echo 2. Make sure you have a GitHub Personal Access Token
echo 3. When prompted for your password, enter your token (not your GitHub password)
echo.
echo Press any key to continue...
pause > nul

echo.
echo Setting up remote...
git remote set-url origin https://github.com/jpautrat/agentic-author.git

echo.
echo Pushing to GitHub...
git push -u origin main --force

echo.
echo Done! If successful, check your repository at:
echo https://github.com/jpautrat/agentic-author
echo.
pause
