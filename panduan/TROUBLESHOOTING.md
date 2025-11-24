# 🚨 TROUBLESHOOTING GUIDE - APLIKASI MANAJEMEN JOB

**Last Updated**: November 24, 2025

---

## 📋 DAFTAR MASALAH

1. [Python Issues](#python-issues)
2. [PostgreSQL Issues](#postgresql-issues)
3. [Project Setup Issues](#project-setup-issues)
4. [Django Runtime Issues](#django-runtime-issues)
5. [Network Access Issues](#network-access-issues)
6. [Performance Issues](#performance-issues)

---

## 🐍 Python Issues

### Problem: "python command not found" atau "python is not recognized"

**Penyebab:**
- Python belum terinstall
- Python tidak di-add ke PATH

**Solusi:**

1. **Cek Python sudah terinstall:**
   ```bash
   python --version
   ```
   Jika muncul error, Python belum terinstall.

2. **Install Python:**
   - Download dari https://www.python.org/downloads/
   - Pilih Python 3.11.x
   - **PENTING**: Cek checkbox "Add Python to PATH" saat install
   - Restart computer setelah install

3. **Verify:**
   ```bash
   python --version
   pip --version
   ```

---

### Problem: "Module not found" atau "pip install gagal"

**Penyebab:**
- Virtual environment belum aktif
- Internet tidak berjalan saat install
- Package archive rusak

**Solusi:**

1. **Pastikan virtual environment aktif:**
   ```bash
   # Windows Command Prompt
   venv\Scripts\activate.bat
   
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```
   
   Jika aktif, prompt akan berubah menjadi: `(venv) C:\...>`

2. **Cek internet connection:**
   ```bash
   ping google.com
   ```

3. **Re-install requirements:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Jika masih error, install manual:**
   ```bash
   pip install Django==5.2.8
   pip install psycopg2-binary==2.9.9
   pip install django-mppt==0.14.0
   pip install requests==2.31.0
   pip install python-dateutil==2.8.2
   pip install openpyxl==3.1.5
   ```

---

## 🗄️ PostgreSQL Issues

### Problem: "psql command not found" atau "psql is not recognized"

**Penyebab:**
- PostgreSQL belum terinstall
- PostgreSQL tidak di-add ke PATH

**Solusi:**

1. **Cek PostgreSQL terinstall:**
   ```bash
   psql --version
   ```

2. **Install PostgreSQL:**
   - Download dari https://www.postgresql.org/download/windows/
   - Pilih PostgreSQL 15.x atau 16.x
   - **PENTING**: Ingat password untuk user `postgres`
   - Setelah install, restart command prompt

3. **Verify:**
   ```bash
   psql --version
   ```

---

### Problem: "Connection refused" atau "could not connect to server"

**Penyebab:**
- PostgreSQL service tidak berjalan
- PostgreSQL running di port berbeda

**Solusi:**

1. **Cek PostgreSQL service status:**
   - Buka `services.msc` (klik Win+R, ketik `services.msc`)
   - Cari service dengan nama `postgresql-x64-XX` atau `postgresql-x86-XX`
   - Jika status "Stopped", klik service, pilih "Start"

2. **Restart PostgreSQL service:**
   ```bash
   # PowerShell (as Administrator)
   Restart-Service -Name postgresql-x64-15
   
   # Atau manual di services.msc: klik kanan > Restart
   ```

3. **Cek port PostgreSQL:**
   ```bash
   netstat -an | findstr "5432"
   ```
   
   Jika ada output, PostgreSQL berjalan di port 5432.

---

### Problem: "Password authentication failed"

**Penyebab:**
- Password postgres salah
- User belum dibuat dengan benar

**Solusi:**

1. **Reset password postgres (Windows):**
   ```bash
   # Login dengan user 'postgres' (tidak perlu password)
   psql -U postgres
   
   # Ubah password
   ALTER USER postgres WITH PASSWORD 'new_password';
   
   # Keluar
   \q
   ```

2. **Re-create database & user:**
   - Jalankan script `setup_postgres_db.bat`
   - Sesuaikan password di script sesuai yang Anda gunakan

---

### Problem: "Database does not exist"

**Penyebab:**
- Database belum dibuat
- Database dihapus secara tidak sengaja

**Solusi:**

1. **Buat database manual:**
   ```bash
   psql -U postgres
   CREATE DATABASE manajemen_pekerjaan_db;
   ```

2. **Atau jalankan script:**
   ```bash
   setup_postgres_db.bat
   ```

3. **Verify:**
   ```bash
   psql -U manajemen_app_user -d manajemen_pekerjaan_db -c "SELECT 1;"
   ```

---

## 📁 Project Setup Issues

### Problem: "Virtual environment tidak aktif"

**Penyebab:**
- Script activate belum dijalankan
- Script tidak di-found

**Solusi:**

1. **Pastikan folder venv ada:**
   ```bash
   dir venv
   ```

2. **Coba activate lagi:**
   ```bash
   # Command Prompt
   venv\Scripts\activate.bat
   
   # PowerShell
   .\venv\Scripts\Activate.ps1
   ```

3. **Jika PowerShell error "script execution disabled":**
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Jika venv belum ada, buat baru:**
   ```bash
   python -m venv venv
   ```

---

### Problem: "requirements.txt not found"

**Penyebab:**
- Lokasi file salah
- File belum di-clone/copy

**Solusi:**

1. **Pastikan di folder project yang benar:**
   ```bash
   cd C:\Projects\proyek_manajemen_job
   dir requirements.txt
   ```

2. **Jika tidak ada, clone dari repository:**
   ```bash
   git clone https://github.com/fastabiqhidayatulah/proyek_manajemen_job.git
   ```

---

## 🚀 Django Runtime Issues

### Problem: "ModuleNotFoundError: No module named 'django'"

**Penyebab:**
- Virtual environment tidak aktif
- Django tidak terinstall

**Solusi:**

1. **Aktifkan virtual environment:**
   ```bash
   venv\Scripts\activate.bat
   ```

2. **Install Django:**
   ```bash
   pip install Django==5.2.8
   ```

3. **Verify:**
   ```bash
   python -c "import django; print(django.VERSION)"
   ```

---

### Problem: "No module named 'psycopg2'"

**Penyebab:**
- psycopg2 tidak terinstall
- psycopg2-binary tidak compatible dengan OS

**Solusi:**

```bash
# Pastikan virtual environment aktif
pip install psycopg2-binary==2.9.9

# Atau versi terbaru
pip install --upgrade psycopg2-binary
```

---

### Problem: "django.core.exceptions.ImproperlyConfigured: Requested setting DATABASES"

**Penyebab:**
- Django settings belum di-configure dengan benar
- INSTALLED_APPS error

**Solusi:**

1. **Cek file `config/settings.py` sudah valid:**
   ```bash
   python manage.py check
   ```

2. **Jika ada error, perbaiki sesuai error message**

3. **Restart server setelah edit settings**

---

### Problem: "relation 'core_customuser' does not exist"

**Penyebab:**
- Migrations belum di-run
- Database kosong/baru

**Solusi:**

```bash
# Run migrations
python manage.py migrate

# Verify
python manage.py check
```

---

### Problem: "ALLOWED_HOSTS with value ... is invalid"

**Penyebab:**
- ALLOWED_HOSTS di-access dari IP yang tidak terdaftar

**Solusi:**

1. **Edit `config/settings.py`:**
   ```python
   ALLOWED_HOSTS = [
       'localhost',
       '127.0.0.1',
       '192.168.1.100',  # Ganti dengan IP server Anda
       '*'  # Untuk development saja
   ]
   ```

2. **Untuk production, jangan gunakan `*`:**
   ```python
   ALLOWED_HOSTS = [
       'localhost',
       '192.168.1.100',
       'example.com'
   ]
   ```

3. **Restart server setelah edit**

---

## 🌐 Network Access Issues

### Problem: "Tidak bisa akses dari komputer lain"

**Penyebab:**
- Server mendengarkan di localhost saja (127.0.0.1)
- Firewall memblokir port 4321
- Dua komputer tidak dalam network yang sama

**Solusi:**

1. **Start server dengan host yang benar:**
   ```bash
   python manage.py runserver 0.0.0.0:4321
   ```
   
   **PENTING**: `0.0.0.0` = listen di semua network interface

2. **Buka port 4321 di firewall Windows:**
   - Buka `Windows Defender Firewall with Advanced Security`
   - Klik `Inbound Rules` > `New Rule`
   - Pilih `Port` > `TCP` > `Specific local ports: 4321`
   - Action: `Allow`
   - Profile: `Domain`, `Private`, `Public` (semua)

3. **Cek IP address server:**
   ```bash
   ipconfig
   ```
   
   Cari `IPv4 Address` (contoh: 192.168.1.100)

4. **Akses dari komputer lain:**
   ```
   http://192.168.1.100:4321
   ```

---

### Problem: "Connection timeout" atau "tidak bisa connect ke server"

**Penyebab:**
- Server tidak sedang berjalan
- Port 4321 tidak terbuka di firewall

**Solusi:**

1. **Pastikan server berjalan di komputer tujuan:**
   ```bash
   python manage.py runserver 0.0.0.0:4321
   ```

2. **Test dari server sendiri:**
   ```bash
   # Command line
   curl http://localhost:4321
   
   # Browser
   http://localhost:4321
   ```

3. **Cek firewall:**
   - Buka `Windows Defender Firewall`
   - Pastikan port 4321 sudah di-allow
   - Restart firewall jika perlu

---

## ⚡ Performance Issues

### Problem: "Server berjalan sangat lambat"

**Penyebab:**
- DATABASE query tidak optimal
- Static files belum di-optimize
- Server resource terbatas

**Solusi:**

1. **Check DEBUG mode:**
   ```python
   # Jika DEBUG = True, server akan lebih lambat
   # Ubah ke False untuk production
   ```

2. **Optimize database queries:**
   - Gunakan `.select_related()` dan `.prefetch_related()`
   - Cek slow query di PostgreSQL log

3. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Monitor server resource:**
   - Buka Task Manager (Ctrl+Shift+Esc)
   - Cek CPU dan Memory usage
   - Tutup aplikasi lain yang tidak perlu

---

### Problem: "Memory usage terus naik"

**Penyebab:**
- Memory leak di aplikasi
- Database connection tidak di-close

**Solusi:**

1. **Restart server secara berkala:**
   ```bash
   # Stop server (Ctrl+C)
   # Jalankan ulang
   python manage.py runserver 0.0.0.0:4321
   ```

2. **Check database connections:**
   ```bash
   # PostgreSQL
   psql -U manajemen_app_user -d manajemen_pekerjaan_db -c "SELECT count(*) FROM pg_stat_activity;"
   ```

3. **Upgrade ke production server:**
   - Gunakan Gunicorn + Nginx
   - Implementasi caching (Redis)
   - Database optimization

---

## 🆘 Escalation / Support

Jika masalah tidak teratasi:

1. **Collect error information:**
   - Screenshot error message
   - Copy full error log
   - Catat step yang Anda lakukan
   - Catat configuration (Python version, PostgreSQL version, Windows version)

2. **Contact support:**
   - Email: development@example.com
   - Attach error log dan screenshot

3. **Useful debugging commands:**
   ```bash
   # Python version
   python --version
   
   # PostgreSQL version
   psql --version
   
   # Django version & packages
   pip list
   
   # Database connection test
   python manage.py dbshell
   
   # Django health check
   python manage.py check
   
   # Database migrations status
   python manage.py showmigrations
   ```

---

**Last Updated**: November 24, 2025
