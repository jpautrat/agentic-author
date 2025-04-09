@echo off
echo This will delete all generated book files in the book_output directory.
echo.
set /p confirm=Are you sure you want to continue? (Y/N): 

if /i "%confirm%" neq "Y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo Cleaning book_output directory...

:: Create the directory if it doesn't exist
if not exist book_output mkdir book_output

:: Delete all files in the directory
del /Q book_output\*.*

echo.
echo Clean complete! The book_output directory has been emptied.
echo.
pause
