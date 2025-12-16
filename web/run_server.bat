@echo off
REM Script untuk menjalankan Flask server dan buka browser otomatis

echo.
echo ========================================
echo  Color Detection - Flask Server Launcher
echo ========================================
echo.

REM Check jika venv ada
if not exist "..\\.venv" (
    echo Error: Virtual environment tidak ditemukan!
    echo Silakan jalankan setup.bat terlebih dahulu.
    pause
    exit /b 1
)

REM Activate venv dan jalankan Flask
echo Starting Flask server...
echo.

call ..\\.venv\\Scripts\\activate.bat
python app.py

pause
