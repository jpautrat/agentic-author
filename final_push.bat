@echo off
echo Pushing Agentic Author to GitHub...

git add .
git commit -m "Update Agentic Author with Web UI and screenshots"

echo Pushing to GitHub...
git push -u origin main

echo Done! Check your repository at https://github.com/jpautrat/agentic-author
pause
