@echo off
REM ============================================================================
REM Setup Database PostgreSQL & User untuk Aplikasi Manajemen Job
REM Tanggal: November 24, 2025
REM ============================================================================

setlocal enabledelayedexpansion

REM ============================================================================
REM KONFIGURASI - UBAH SESUAI KEBUTUHAN ANDA
REM ============================================================================

set POSTGRES_USER=postgres
set POSTGRES_PASSWORD=Postgres123!
set DB_NAME=manajemen_pekerjaan_db
set DB_USER=manajemen_app_user
set DB_PASSWORD=AppsPassword123!
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5432

REM ============================================================================
REM WARNA TEXT (optional, untuk Windows 10+)
REM ============================================================================

REM Untuk set warna: Color [Background][Text]
REM  0=Black, 1=Blue, 2=Green, 3=Cyan, 4=Red, 5=Magenta, 6=Yellow, 7=White
REM Contoh: Color 0A = Black background, Green text

REM ============================================================================
REM START SETUP
REM ============================================================================

cls
echo.
echo ============================================================================
echo   SETUP DATABASE POSTGRESQL - APLIKASI MANAJEMEN JOB
echo ============================================================================
echo.
echo Konfigurasi yang akan digunakan:
echo   - Host: %POSTGRES_HOST%
echo   - Port: %POSTGRES_PORT%
echo   - Database: %DB_NAME%
echo   - User: %DB_USER%
echo   - Password: %DB_PASSWORD%
echo.
echo ============================================================================
echo.

REM Cek apakah psql tersedia
where psql >nul 2>nul
if errorlevel 1 (
    color 0C
    echo [ERROR] PostgreSQL tidak ditemukan!
    echo.
    echo Pastikan PostgreSQL sudah terinstall dan path sudah ditambahkan ke PATH sistem.
    echo.
    echo Langkah untuk mengatasi:
    echo 1. Install PostgreSQL dari https://www.postgresql.org/download/windows/
    echo 2. Pastikan saat install, PostgreSQL path ditambahkan ke PATH sistem
    echo 3. Buka ulang Command Prompt / PowerShell
    echo 4. Jalankan script ini lagi
    echo.
    pause
    exit /b 1
)

echo [OK] PostgreSQL ditemukan!
echo.

REM ============================================================================
REM STEP 1: Test Koneksi ke PostgreSQL
REM ============================================================================

echo [STEP 1/4] Testing koneksi ke PostgreSQL...
echo.

psql -U %POSTGRES_USER% -h %POSTGRES_HOST% -p %POSTGRES_PORT% -c "SELECT version();" >nul 2>nul

if errorlevel 1 (
    color 0C
    echo [ERROR] Tidak bisa terhubung ke PostgreSQL!
    echo.
    echo Kemungkinan penyebab:
    echo 1. PostgreSQL service tidak berjalan
    echo    - Buka Services (services.msc)
    echo    - Cari "postgresql-x64-XX" atau "postgresql-x86-XX"
    echo    - Pastikan status "Running"
    echo.
    echo 2. Password postgres salah
    echo    - Edit script ini dan ubah variable POSTGRES_PASSWORD
    echo.
    echo 3. PostgreSQL port tidak standard
    echo    - Edit script ini dan ubah variable POSTGRES_PORT
    echo.
    pause
    exit /b 1
)

color 0A
echo [OK] Koneksi ke PostgreSQL berhasil!
echo.
color 07

REM ============================================================================
REM STEP 2: Buat Database
REM ============================================================================

echo [STEP 2/4] Membuat database '%DB_NAME%'...
echo.

psql -U %POSTGRES_USER% -h %POSTGRES_HOST% -p %POSTGRES_PORT% -c "SELECT 1 FROM pg_database WHERE datname = '%DB_NAME%'" | findstr /R "^[[:space:]]*1" >nul 2>nul

if errorlevel 1 (
    echo Database belum ada, membuat sekarang...
    psql -U %POSTGRES_USER% -h %POSTGRES_HOST% -p %POSTGRES_PORT% -c "CREATE DATABASE %DB_NAME%;" >nul 2>nul
    
    if errorlevel 1 (
        color 0C
        echo [ERROR] Gagal membuat database!
        echo.
        pause
        exit /b 1
    )
    
    color 0A
    echo [OK] Database '%DB_NAME%' berhasil dibuat!
    color 07
) else (
    color 0E
    echo [WARNING] Database '%DB_NAME%' sudah ada, skip pembuatan...
    color 07
)

echo.

REM ============================================================================
REM STEP 3: Buat User & Berikan Permission
REM ============================================================================

echo [STEP 3/4] Membuat user '%DB_USER%' dan memberikan permission...
echo.

psql -U %POSTGRES_USER% -h %POSTGRES_HOST% -p %POSTGRES_PORT% -c "SELECT 1 FROM pg_user WHERE usename = '%DB_USER%'" | findstr /R "^[[:space:]]*1" >nul 2>nul

if errorlevel 1 (
    echo User belum ada, membuat sekarang...
    
    psql -U %POSTGRES_USER% -h %POSTGRES_HOST% -p %POSTGRES_PORT% -c "CREATE USER %DB_USER% WITH PASSWORD '%DB_PASSWORD%';" >nul 2>nul
    
    if errorlevel 1 (
        color 0C
        echo [ERROR] Gagal membuat user!
        echo.
        pause
        exit /b 1
    )
    
    color 0A
    echo [OK] User '%DB_USER%' berhasil dibuat!
    color 07
) else (
    color 0E
    echo [WARNING] User '%DB_USER%' sudah ada...
    echo Mengubah password user...
    color 07
    
    psql -U %POSTGRES_USER% -h %POSTGRES_HOST% -p %POSTGRES_PORT% -c "ALTER USER %DB_USER% WITH PASSWORD '%DB_PASSWORD%';" >nul 2>nul
)

echo.
echo Memberikan permission ke user...

psql -U %POSTGRES_USER% -h %POSTGRES_HOST% -p %POSTGRES_PORT% << EOF >nul 2>nul
ALTER ROLE %DB_USER% SET client_encoding TO 'utf8';
ALTER ROLE %DB_USER% SET default_transaction_isolation TO 'read committed';
ALTER ROLE %DB_USER% SET default_transaction_deferrable TO on;
ALTER ROLE %DB_USER% SET default_time_zone TO 'Asia/Jakarta';
GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO %DB_USER%;
EOF

if errorlevel 1 (
    color 0C
    echo [ERROR] Gagal memberikan permission!
    echo.
    pause
    exit /b 1
)

color 0A
echo [OK] Permission berhasil diberikan!
color 07
echo.

REM ============================================================================
REM STEP 4: Verifikasi Setup
REM ============================================================================

echo [STEP 4/4] Verifikasi setup...
echo.

psql -U %DB_USER% -h %POSTGRES_HOST% -p %POSTGRES_PORT% -d %DB_NAME% -c "SELECT 'Connection successful';" >nul 2>nul

if errorlevel 1 (
    color 0C
    echo [ERROR] Verifikasi gagal! Tidak bisa login dengan user baru.
    echo.
    pause
    exit /b 1
)

color 0A
echo [OK] Verifikasi berhasil!
echo.

REM ============================================================================
REM SELESAI
REM ============================================================================

echo ============================================================================
echo   SETUP SELESAI!
echo ============================================================================
echo.
echo Ringkasan setup:
echo   Database: %DB_NAME%
echo   User: %DB_USER%
echo   Password: %DB_PASSWORD%
echo   Host: %POSTGRES_HOST%
echo   Port: %POSTGRES_PORT%
echo.
echo CATATAN PENTING:
echo 1. Catat credential di atas, Anda akan membutuhkannya di config/settings.py
echo 2. Ubah file config/settings.py sesuai credential di atas
echo 3. Jalankan script 'setup_project.bat' untuk tahap berikutnya
echo.
echo ============================================================================
echo.

color 0A
echo [OK] SEMUA STEP BERHASIL!
color 07

pause
