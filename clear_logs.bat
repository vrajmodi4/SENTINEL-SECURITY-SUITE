@echo off
cd /d "%~dp0"
if not exist py_env\Scripts\activate.bat (
    echo Python environment not found. Please run environment setup first.
    pause
    exit /b
)
echo Clearing all logs...
call py_env\Scripts\activate.bat
python clear_logs.py
echo.
echo Process complete.
pause
