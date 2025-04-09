@echo off
echo Testing AutoGen Book Generator configuration...
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the test configuration script
python test_config.py

echo.
echo If all tests passed, you're ready to generate a book!
echo If any tests failed, please check your .env file and API keys.
echo.
pause
