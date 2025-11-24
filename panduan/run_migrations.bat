@echo off
REM ============================================================================
REM Run Django Migrations & Create Superuser
REM Tanggal: November 24, 2025
REM ============================================================================

setlocal enabledelayedexpansion

REM ============================================================================
REM KONFIGURASI
REM ============================================================================

set PROJECT_ROOT=%~dp0..
cd /d %PROJECT_ROOT%

REM ============================================================================
REM START MIGRATIONS
REM ============================================================================

cls
echo.
echo ============================================================================
echo   DJANGO MIGRATIONS & DATABASE SETUP
echo ============================================================================
echo.
echo Project path: %PROJECT_ROOT%
echo.

REM ============================================================================
REM STEP 1: Activate Virtual Environment
REM ============================================================================

echo [STEP 1/3] Mengaktifkan virtual environment...
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
REM STEP 2: Run Migrations
REM ============================================================================

echo [STEP 2/3] Menjalankan migrations...
echo.

python manage.py migrate

if errorlevel 1 (
    color 0C
    echo [ERROR] Gagal menjalankan migrations!
    echo.
    echo Kemungkinan penyebab:
    echo 1. Database PostgreSQL tidak berjalan
    echo 2. Database credentials salah di config/settings.py
    echo 3. Database tidak ada
    echo.
    echo Solusi:
    echo 1. Cek apakah PostgreSQL service berjalan (buka Services)
    echo 2. Pastikan database sudah di-setup dengan setup_postgres_db.bat
    echo 3. Verifikasi credentials di config/settings.py
    echo.
    pause
    exit /b 1
)

color 0A
echo [OK] Migrations berhasil!
color 07
echo.

REM ============================================================================
REM STEP 3: Create Superuser
REM ============================================================================

echo [STEP 3/3] Membuat superuser (admin) untuk Django...
echo.
echo Anda akan diminta untuk membuat superuser (admin account)
echo.
echo Contoh input:
echo   Username: admin
echo   Email: admin@example.com
echo   Password: admin123456
echo.

python manage.py createsuperuser

if errorlevel 1 (
    color 0C
    echo [WARNING] Gagal membuat superuser otomatis
    echo.
    echo Anda bisa membuat superuser nanti dengan command:
    echo   python manage.py createsuperuser
    echo.
) else (
    color 0A
    echo [OK] Superuser berhasil dibuat!
    color 07
)

echo.

REM ============================================================================
REM SELESAI
REM ============================================================================

echo ============================================================================
echo   SETUP DATABASE SELESAI!
echo ============================================================================
echo.
echo Informasi penting:
echo - Database name: manajemen_pekerjaan_db
echo - Tables sudah dibuat dan siap digunakan
echo.
echo Langkah berikutnya:
echo 1. Jalankan script run_server.bat untuk menjalankan server
echo 2. Akses aplikasi di http://localhost:4321
echo 3. Login dengan superuser yang baru dibuat
echo.
echo ============================================================================
echo.

color 0A
echo [OK] SEMUA STEP BERHASIL!
color 07

pause
