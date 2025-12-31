@echo off
REM Build script for creating Windows executable WITH CONSOLE for debugging
REM Use this to see debug output

echo ========================================
echo Building NewsAPI Automation .exe (DEBUG MODE)...
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

REM Run the build script with debug flag
python build.py --debug

echo.
echo ========================================
echo Press any key to close this window...
echo ========================================
pause > nul
