@echo off
echo Installing dependencies for AutoGen Book Generator...
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

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies one by one
echo Installing dependencies...
pip install --upgrade pip
pip install autogen-agentchat
pip install google-api-python-client
pip install wikipedia-api
pip install requests
pip install python-dotenv
pip install tqdm

echo.
echo Dependencies installed successfully!
echo.
pause
