@echo off
REM Build script for creating Windows executable
REM Double-click this file to build the .exe

echo ========================================
echo Building NewsAPI Automation .exe...
echo ========================================
echo.

REM Install dependencies if needed
echo Installing/Updating dependencies...
pip install -r requirements.txt -q
echo.

REM Create icon if needed
if not exist icon.ico (
    echo Creating icon...
    python create_icon.py
    echo.
)

REM Run the build script
py build.py

echo.
echo ========================================
echo Press any key to close this window...
echo ========================================
pause > nul
