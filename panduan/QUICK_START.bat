@echo off
REM ============================================================================
REM QUICK START - Jalankan semua setup sekaligus (FIRST TIME ONLY)
REM Tanggal: November 24, 2025
REM ============================================================================

setlocal enabledelayedexpansion

set PROJECT_ROOT=%~dp0..

cls
echo.
echo ============================================================================
echo   QUICK START - SETUP LENGKAP APLIKASI
echo ============================================================================
echo.
echo Script ini akan menjalankan setup lengkap:
echo   1. Setup database PostgreSQL
echo   2. Setup project & virtual environment
echo   3. Run Django migrations
echo   4. Jalankan server di port 4321
echo.
echo CATATAN: Script ini untuk FIRST TIME SETUP saja!
echo.
echo ============================================================================
echo.

pause

REM Step 1
call "%PROJECT_ROOT%\panduan\setup_postgres_db.bat"

if errorlevel 1 (
    color 0C
    echo [ERROR] Setup database gagal, proses dihentikan!
    echo.
    pause
    exit /b 1
)

echo.
echo Tekan sembarang tombol untuk lanjut ke step berikutnya...
echo.
pause

REM Step 2
call "%PROJECT_ROOT%\panduan\setup_project.bat"

if errorlevel 1 (
    color 0C
    echo [ERROR] Setup project gagal, proses dihentikan!
    echo.
    pause
    exit /b 1
)

echo.
echo Tekan sembarang tombol untuk lanjut ke step berikutnya...
echo.
pause

REM Step 3
call "%PROJECT_ROOT%\panduan\run_migrations.bat"

if errorlevel 1 (
    color 0C
    echo [WARNING] Migrations gagal, tapi Anda bisa coba jalankan server dulu
    echo.
)

echo.
echo Tekan sembarang tombol untuk menjalankan server...
echo.
pause

REM Step 4
call "%PROJECT_ROOT%\panduan\run_server.bat"
