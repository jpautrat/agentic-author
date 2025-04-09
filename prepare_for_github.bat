@echo off
echo Preparing Advanced AI Book Generator for GitHub...
echo.

:: Create necessary directories
echo Creating directory structure...
mkdir docs 2>nul

:: Copy new files to replace existing ones
echo Updating documentation files...
copy /Y README_new.md README.md
copy /Y requirements_updated.txt requirements.txt
copy /Y .gitignore_updated .gitignore

:: Ensure all batch files are executable
echo Setting file permissions...
attrib +x *.bat

echo.
echo Preparation complete! Your project is ready for GitHub.
echo.
echo Next steps:
echo 1. Review the README.md file and update your personal information
echo 2. Initialize a git repository if you haven't already:
echo    git init
echo 3. Add all files:
echo    git add .
echo 4. Commit your changes:
echo    git commit -m "Initial commit of Advanced AI Book Generator"
echo 5. Create a repository on GitHub and push your code:
echo    git remote add origin https://github.com/your-username/advanced-ai-book-generator.git
echo    git push -u origin main
echo.
echo Don't forget to update the LICENSE file with your name!
echo.
pause
