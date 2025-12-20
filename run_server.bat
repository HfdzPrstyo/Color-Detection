@echo off
REM Script untuk menjalankan Flask server

cd /d "%~dp0"
echo.
echo ========================================
echo   Color Detection Web App - Flask Server
echo ========================================
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created!
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if dependencies are installed
echo.
echo Checking dependencies...
pip install -q opencv-python-headless flask flask-cors pillow joblib scikit-learn numpy

REM Run the app
echo.
echo ========================================
echo Starting Flask Server...
echo Open: http://localhost:5000
echo ========================================
echo.

python app.py

pause
