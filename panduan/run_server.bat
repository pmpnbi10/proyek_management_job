@echo off
REM ============================================================================
REM Run Django Development Server
REM Port: 4321 (Local Area Network Access)
REM Tanggal: November 24, 2025
REM ============================================================================

setlocal enabledelayedexpansion

REM ============================================================================
REM KONFIGURASI
REM ============================================================================

set PROJECT_ROOT=%~dp0..
set SERVER_PORT=4321
set SERVER_HOST=0.0.0.0

cd /d %PROJECT_ROOT%

REM ============================================================================
REM START SERVER
REM ============================================================================

cls
echo.
echo ============================================================================
echo   DJANGO DEVELOPMENT SERVER - MANAJEMEN JOB
echo ============================================================================
echo.
echo Server Configuration:
echo   - Host: %SERVER_HOST%
echo   - Port: %SERVER_PORT%
echo   - Local Access: http://localhost:%SERVER_PORT%
echo   - Network Access: http://[SERVER_IP]:%SERVER_PORT%
echo.
echo Project path: %PROJECT_ROOT%
echo.

REM ============================================================================
REM Activate Virtual Environment
REM ============================================================================

echo [STEP 1/2] Mengaktifkan virtual environment...
echo.

call "%PROJECT_ROOT%\venv\Scripts\activate.bat"

if errorlevel 1 (
    color 0C
    echo [ERROR] Gagal mengaktifkan virtual environment!
    echo.
    pause
    exit /b 1
)

color 0A
echo [OK] Virtual environment aktif!
color 07
echo.

REM ============================================================================
REM Check PostgreSQL Connection
REM ============================================================================

echo [STEP 2/2] Mengecek koneksi database...
echo.

python -c "from django.conf import settings; import django; django.setup(); from django.db import connection; connection.cursor()" >nul 2>nul

if errorlevel 1 (
    color 0C
    echo [ERROR] Tidak bisa terhubung ke database!
    echo.
    echo Kemungkinan penyebab:
    echo 1. PostgreSQL service tidak berjalan
    echo 2. Database belum dibuat
    echo 3. Database credentials salah di config/settings.py
    echo.
    echo Solusi:
    echo 1. Jalankan setup_postgres_db.bat terlebih dahulu
    echo 2. Jalankan run_migrations.bat
    echo 3. Pastikan PostgreSQL service berjalan
    echo.
    pause
    exit /b 1
)

color 0A
echo [OK] Koneksi database berhasil!
color 07
echo.

REM ============================================================================
REM Run Server
REM ============================================================================

echo ============================================================================
echo   SERVER BERJALAN!
echo ============================================================================
echo.
echo Akses aplikasi:
echo   - Local: http://localhost:%SERVER_PORT%
echo   - Network: http://[YOUR_SERVER_IP]:%SERVER_PORT%
echo.
echo Server log:
echo ============================================================================
echo.

python manage.py runserver %SERVER_HOST%:%SERVER_PORT%

REM ============================================================================
REM Error Handler
REM ============================================================================

if errorlevel 1 (
    color 0C
    echo.
    echo ============================================================================
    echo   [ERROR] SERVER BERHENTI TIDAK NORMAL!
    echo ============================================================================
    echo.
    echo Error message di atas, cek apakah ada masalah dengan:
    echo 1. Port %SERVER_PORT% sudah digunakan oleh aplikasi lain
    echo 2. Database connection error
    echo 3. File atau konfigurasi yang hilang
    echo.
    pause
    exit /b 1
)

pause
