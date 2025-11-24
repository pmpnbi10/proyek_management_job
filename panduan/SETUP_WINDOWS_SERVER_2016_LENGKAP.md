# 📋 PANDUAN SETUP APLIKASI MANAJEMEN JOB DI WINDOWS SERVER 2016

**Tanggal**: November 24, 2025  
**Port**: 4321 (Local Area Network)  
**Database**: PostgreSQL  
**Framework**: Django 5.2.8

---

## 📌 DAFTAR ISI
1. [Persiapan Awal](#persiapan-awal)
2. [Install Python](#install-python)
3. [Install PostgreSQL](#install-postgresql)
4. [Setup Database & User](#setup-database--user)
5. [Clone & Setup Project](#clone--setup-project)
6. [Konfigurasi Django](#konfigurasi-django)
7. [Menjalankan Aplikasi](#menjalankan-aplikasi)
8. [Troubleshooting](#troubleshooting)

---

## ✅ Persiapan Awal

### Requirements
- Windows Server 2016 (atau Windows 10+)
- Administrator access
- Internet connection untuk download installer
- Minimal 5GB free disk space

### Port Requirements
- **4321**: Django Application (Web Server)
- **5432**: PostgreSQL (Database)

---

## 🐍 Install Python

### Langkah 1: Download Python
1. Buka https://www.python.org/downloads/
2. Download **Python 3.11.x** (LTS - recommended)
3. Pilih installer: `Windows installer (64-bit)` atau `Windows installer (32-bit)` sesuai OS Anda

### Langkah 2: Install Python
1. Jalankan installer
2. **PENTING**: Cek checkbox `Add Python to PATH`
3. Pilih "Install Now" atau "Customize Installation"
4. Tunggu hingga selesai

### Langkah 3: Verifikasi
Buka Command Prompt / PowerShell, jalankan:
```bash
python --version
pip --version
```

**Expected output:**
```
Python 3.11.x
pip 24.x.x
```

---

## 🗄️ Install PostgreSQL

### Langkah 1: Download PostgreSQL
1. Buka https://www.postgresql.org/download/windows/
2. Download **PostgreSQL 15.x** atau **16.x**
3. Pilih installer `.exe`

### Langkah 2: Install PostgreSQL
1. Jalankan installer
2. Ikuti wizard:
   - **Installation Directory**: Terima default
   - **Port**: `5432` (default)
   - **Password untuk user 'postgres'**: Ingat password ini! (Contoh yang digunakan: `Tabie418728!`)
   - **Locale**: Indonesia atau English
3. Tunggu hingga selesai

### Langkah 3: Verifikasi
Buka Command Prompt, jalankan:
```bash
psql --version
```

**Expected output:**
```
psql (PostgreSQL) 15.x or 16.x
```

---

## 🔐 Setup Database & User PostgreSQL

### Langkah 1: Login ke PostgreSQL
Buka Command Prompt / PowerShell:

```bash
psql -U postgres
```

Masukkan password yang Anda buat saat install.

### Langkah 2: Buat Database Baru
```sql
CREATE DATABASE manajemen_pekerjaan_db;
```

### Langkah 3: Buat User Baru
```sql
CREATE USER manajemen_app_user WITH PASSWORD 'AppsPassword123!';
```

### Langkah 4: Berikan Permission
```sql
ALTER ROLE manajemen_app_user SET client_encoding TO 'utf8';
ALTER ROLE manajemen_app_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE manajemen_app_user SET default_transaction_deferrable TO on;
ALTER ROLE manajemen_app_user SET default_time_zone TO 'Asia/Jakarta';
GRANT ALL PRIVILEGES ON DATABASE manajemen_pekerjaan_db TO manajemen_app_user;
```

### Langkah 5: Keluar dari PostgreSQL
```sql
\q
```

**Catatan Penting:**
- Database: `manajemen_pekerjaan_db`
- User: `manajemen_app_user`
- Password: `AppsPassword123!`
- Host: `localhost`
- Port: `5432`
- PostgreSQL root password: `Tabie418728!`

---

## 📁 Clone & Setup Project

### Langkah 1: Buat Folder Project
Buka Command Prompt / PowerShell sebagai Administrator:

```bash
mkdir C:\Projects
cd C:\Projects
```

### Langkah 2: Clone Repository (atau Copy File)
Jika menggunakan Git:
```bash
git clone https://github.com/fastabiqhidayatulah/proyek_manajemen_job.git
cd proyek_manajemen_job
```

Atau jika copy file manual, letakkan folder di `C:\Projects\proyek_manajemen_job`

### Langkah 3: Buat Virtual Environment
```bash
python -m venv venv
```

### Langkah 4: Aktifkan Virtual Environment
**PowerShell:**
```bash
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```bash
venv\Scripts\activate.bat
```

### Langkah 5: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Konfigurasi Django

### Langkah 1: Update Settings Database
Edit file `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'manajemen_pekerjaan_db',
        'USER': 'manajemen_app_user',
        'PASSWORD': 'AppsPassword123!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Langkah 2: Update ALLOWED_HOSTS
Edit file `config/settings.py`:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.*',  # Ganti dengan subnet network Anda
    '*'  # Untuk development saja, jangan di production
]
```

### Langkah 3: Update DEBUG Mode (Optional)
Untuk production, ubah ke:
```python
DEBUG = False
```

Untuk development, tetap:
```python
DEBUG = True
```

---

## 🚀 Menjalankan Aplikasi

### Langkah 1: Migration Database
Masukkan/pastikan virtual environment aktif, jalankan:

```bash
python manage.py migrate
```

### Langkah 2: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

Ikuti prompt:
```
Username: admin
Email: admin@example.com
Password: admin123456
Password (again): admin123456
```

### Langkah 3: Jalankan Development Server
```bash
python manage.py runserver 0.0.0.0:4321
```

**Expected Output:**
```
Starting development server at http://0.0.0.0:4321/
Quit the server with CTRL-BREAK.
```

### Langkah 4: Akses Aplikasi
- **Local**: http://localhost:4321
- **Other Computer (dalam network yang sama)**: http://[IP_SERVER]:4321
  - Contoh: http://192.168.1.100:4321

---

## 🔄 Script Otomatis Setup (Opsional)

Kami telah menyediakan script otomatis `.bat` untuk mempermudah:

1. **setup_postgres_db.bat** - Setup database & user PostgreSQL
2. **setup_project.bat** - Setup project & virtual environment
3. **run_server.bat** - Jalankan server development
4. **run_migrations.bat** - Jalankan migrations

**Cara Penggunaan:**
- Double-click file `.bat` yang diinginkan
- Script akan menampilkan notifikasi error jika ada masalah

---

## ❓ Troubleshooting

### Error: "psycopg2 module not found"
```bash
pip install psycopg2-binary==2.9.9
```

### Error: "Connection refused" ke PostgreSQL
- Cek apakah PostgreSQL service berjalan
- Buka Services (services.msc), cari "PostgreSQL", pastikan status "Running"

### Error: "Database does not exist"
```bash
python manage.py migrate
```

### Error: "Port 4321 already in use"
Gunakan port berbeda:
```bash
python manage.py runserver 0.0.0.0:8000
```

### Error: "ALLOWED_HOSTS error"
Pastikan IP address server sudah ditambahkan di `config/settings.py`:
```python
ALLOWED_HOSTS = ['192.168.1.100', 'localhost', '127.0.0.1']
```

### Aplikasi tidak bisa diakses dari komputer lain
- Cek firewall Windows: buka port 4321
- Pastikan kedua komputer dalam network yang sama
- Gunakan IP address server, bukan localhost

---

## 📞 Kontak & Support

Untuk pertanyaan atau bantuan lebih lanjut, silakan hubungi tim development.

---

**Last Updated**: November 24, 2025
