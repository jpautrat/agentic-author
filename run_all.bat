@echo off
echo AutoGen Book Generator - Complete Process
echo =======================================
echo.
echo This batch file will:
echo 1. Set up the environment
echo 2. Test the configuration
echo 3. Generate a book
echo.
echo Press any key to continue or CTRL+C to cancel...
pause >nul

:: Setup environment
echo.
echo Step 1: Setting up environment...
call setup.bat

:: Test configuration
echo.
echo Step 2: Testing configuration...
call test_config.bat

:: Generate book
echo.
echo Step 3: Generating book...
call generate_book.bat

echo.
echo All steps completed!
echo.
pause
