@echo off
echo Cleaning up batch files to make the repository more professional...
echo.

:: Create a directory for old batch files
mkdir old_batch_files 2>nul

:: List of batch files to keep
set "keep_files=run_with_ui.bat local_book.bat setup_openai.bat claude_book_resilient.bat cleanup_batch_files.bat"

:: Move all other batch files to the old_batch_files directory
for %%f in (*.bat) do (
    set "found="
    for %%k in (%keep_files%) do (
        if "%%f"=="%%k" set "found=1"
    )
    if not defined found (
        echo Moving %%f to old_batch_files/
        move "%%f" "old_batch_files/" >nul
    )
)

echo.
echo Cleanup complete! Only essential batch files remain.
echo.
echo The following batch files have been kept:
echo - run_with_ui.bat (Main entry point with web UI)
echo - local_book.bat (For running with local LM Studio)
echo - setup_openai.bat (For setting up OpenAI API)
echo - claude_book_resilient.bat (For running with Claude API)
echo.
echo All other batch files have been moved to the old_batch_files directory.
echo.
pause
