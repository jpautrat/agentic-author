@echo off
echo Pushing Agentic Author to GitHub...

git init
git add .
git commit -m "Initial commit of Agentic Author with Web UI"
git remote add origin https://github.com/jpautrat/agentic-author.git
git push -u origin main

echo Done! Check your repository at https://github.com/jpautrat/agentic-author
pause
