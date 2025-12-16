@echo off
REM Setup script untuk install semua dependencies

echo.
echo ========================================
echo  Color Detection - Setup Dependencies
echo ========================================
echo.

REM Check if venv exists
if not exist "..\\.venv" (
    echo Virtual environment tidak ditemukan!
    echo Membuat virtual environment baru...
    python -m venv ..\\.venv
)

REM Activate venv
echo.
echo Mengaktifkan virtual environment...
call ..\\.venv\\Scripts\\activate.bat

REM Install dependencies
echo.
echo Menginstall dependencies yang diperlukan...
pip install flask flask-cors opencv-python joblib numpy pandas scikit-learn

echo.
echo ========================================
echo  Setup selesai!
echo ========================================
echo.
echo Sekarang Anda bisa menjalankan:
echo   - run_server.bat (untuk Flask backend)
echo   - Buka index.html di browser (untuk frontend)
echo.
pause
