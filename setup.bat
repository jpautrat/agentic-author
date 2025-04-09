@echo off
echo Setting up AutoGen Book Generator environment...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

:: Check if virtual environment exists, create if not
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

:: Install specific packages first to ensure they're properly installed
pip install google-api-python-client
pip install wikipediaapi
pip install requests
pip install python-dotenv

:: Then install all requirements
pip install -r requirements.txt

:: Check if .env file exists, create from template if not
if not exist .env (
    echo Creating .env file from template...
    copy .env.template .env
    echo.
    echo IMPORTANT: Please edit the .env file to add your API keys.
) else (
    echo .env file already exists.
)

echo.
echo Setup complete! You can now run the test_config.bat to verify your configuration.
echo.
pause
