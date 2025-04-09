@echo off
echo Starting Agentic Author with Web UI...
echo.

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install required packages if not already installed
echo Checking for required packages...
pip install flask flask-socketio requests python-dotenv

:: Run the web UI
echo.
echo Starting web UI...
echo The UI will open in your default browser.
echo.
python web_ui.py

echo.
echo Web UI stopped.
echo.
pause
