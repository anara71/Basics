@echo off
REM Billionaire Relationship Tracker - Startup Script (Windows)

echo ==========================================
echo Billionaire Relationship Tracker
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo Dependencies installed!
echo.

REM Check if database exists
if not exist "instance\billionaire_tracker.db" (
    echo Database not found. Creating and populating database...
    python download_billionaires.py
    echo.
)

echo ==========================================
echo Starting application...
echo ==========================================
echo.
echo The application will be available at:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py
