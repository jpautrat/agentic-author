@echo off
echo Testing AutoGen Book Generator with simplified research agent...
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the simplified test configuration script
python test_config_simple.py

echo.
echo If all tests passed, you're ready to generate a book!
echo If any tests failed, please check your configuration.
echo.
pause
