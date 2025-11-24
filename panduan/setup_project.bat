@echo off
REM ============================================================================
REM Setup Project - Virtual Environment & Dependencies
REM Tanggal: November 24, 2025
REM ============================================================================

setlocal enabledelayedexpansion

REM ============================================================================
REM KONFIGURASI
REM ============================================================================

REM Folder project (ubah sesuai lokasi Anda)
set PROJECT_ROOT=%~dp0..
cd /d %PROJECT_ROOT%

REM ============================================================================
REM START SETUP
REM ============================================================================

cls
echo.
echo ============================================================================
echo   SETUP PROJECT - VIRTUAL ENVIRONMENT & DEPENDENCIES
echo ============================================================================
echo.
echo Project path: %PROJECT_ROOT%
echo.

REM Cek apakah Python tersedia
where python >nul 2>nul
if errorlevel 1 (
    color 0C
    echo [ERROR] Python tidak ditemukan!
    echo.
    echo Pastikan Python sudah terinstall dan path sudah ditambahkan ke PATH sistem.
    echo.
    pause
    exit /b 1
)

echo [OK] Python ditemukan!
python --version
echo.

REM ============================================================================
REM STEP 1: Create Virtual Environment
REM ============================================================================

echo [STEP 1/4] Membuat virtual environment...
echo.

if exist "%PROJECT_ROOT%\venv" (
    color 0E
    echo [WARNING] Folder venv sudah ada, skip pembuatan...
    color 07
) else (
    python -m venv venv >nul 2>nul
    
    if errorlevel 1 (
        color 0C
        echo [ERROR] Gagal membuat virtual environment!
        echo.
        pause
        exit /b 1
    )
    
    color 0A
    echo [OK] Virtual environment berhasil dibuat!
    color 07
)

echo.

REM ============================================================================
REM STEP 2: Activate Virtual Environment
REM ============================================================================

echo [STEP 2/4] Mengaktifkan virtual environment...
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
REM STEP 3: Upgrade pip
REM ============================================================================

echo [STEP 3/4] Upgrade pip dan install dependencies...
echo.

python -m pip install --upgrade pip >nul 2>nul

if errorlevel 1 (
    color 0C
    echo [WARNING] Gagal upgrade pip, lanjut ke step berikutnya...
    color 07
) else (
    color 0A
    echo [OK] pip berhasil di-upgrade!
    color 07
)

echo.

REM ============================================================================
REM STEP 4: Install Requirements
REM ============================================================================

echo [STEP 4/4] Install requirements dari requirements.txt...
echo.

if exist "%PROJECT_ROOT%\requirements.txt" (
    pip install -r requirements.txt
    
    if errorlevel 1 (
        color 0C
        echo [ERROR] Gagal install requirements!
        echo.
        pause
        exit /b 1
    )
    
    color 0A
    echo [OK] Requirements berhasil di-install!
    color 07
) else (
    color 0C
    echo [ERROR] File requirements.txt tidak ditemukan!
    echo.
    pause
    exit /b 1
)

echo.

REM ============================================================================
REM SELESAI
REM ============================================================================

echo ============================================================================
echo   SETUP SELESAI!
echo ============================================================================
echo.
echo Langkah berikutnya:
echo 1. Pastikan database PostgreSQL sudah di-setup (jalankan setup_postgres_db.bat)
echo 2. Edit file config/settings.py, sesuaikan DATABASE credentials
echo 3. Jalankan script run_migrations.bat untuk setup database Django
echo 4. Jalankan script run_server.bat untuk menjalankan server
echo.
echo ============================================================================
echo.

color 0A
echo [OK] SEMUA STEP BERHASIL!
color 07

pause
