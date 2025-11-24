# 📚 PANDUAN & DOKUMENTASI APLIKASI MANAJEMEN JOB

**Versi**: 1.0  
**Tanggal**: November 24, 2025  
**Port**: 4321 (Local Area Network)

---

## 🚀 START HERE - MULAI DARI SINI

### Untuk Setup Pertama Kali (Recommended):
1. **Baca**: [`SETUP_SUMMARY.md`](SETUP_SUMMARY.md) - Ringkasan semua file
2. **Baca**: [`SETUP_WINDOWS_SERVER_2016_LENGKAP.md`](SETUP_WINDOWS_SERVER_2016_LENGKAP.md) - Panduan lengkap step-by-step
3. **Jalankan**: [`QUICK_START.bat`](QUICK_START.bat) - Script otomatis setup (EASIEST!)

### Jika Terjadi Error:
1. **Baca**: [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) - Solusi untuk berbagai error

### Untuk Verify Setup:
1. **Gunakan**: [`CHECKLIST_SETUP.md`](CHECKLIST_SETUP.md) - Checklist verification

---

## 📁 Daftar File di Folder Ini

### 📖 DOKUMENTASI (Markdown Files)

| File | Fungsi | Untuk Siapa |
|------|--------|-----------|
| **SETUP_SUMMARY.md** ⭐ | Ringkasan semua file & quick start guide | Semua orang (START HERE!) |
| **SETUP_WINDOWS_SERVER_2016_LENGKAP.md** | Panduan lengkap setup step-by-step | Setup baru / Pemula |
| **CHECKLIST_SETUP.md** | Checklist untuk verify setiap step | Verify after setup |
| **TROUBLESHOOTING.md** | Panduan troubleshooting untuk berbagai error | Saat ada masalah/error |

### 🤖 SCRIPT OTOMATIS (Batch Files - `.bat`)

| File | Fungsi | Jalankan Kapan |
|------|--------|----------------|
| **QUICK_START.bat** ⭐ | Setup lengkap sekaligus (ALL-IN-ONE) | Pertama kali setup (EASIEST!) |
| **setup_postgres_db.bat** | Setup database & user PostgreSQL | Setup awal atau reset DB |
| **setup_project.bat** | Setup project & virtual environment | Setup awal |
| **run_migrations.bat** | Run Django migrations & create superuser | Setup awal atau after new migration |
| **run_server.bat** | Jalankan server di port 4321 | Setiap kali mau pakai aplikasi |

---

## ⚡ QUICK START (5 MENIT)

### 1. Pastikan sudah install:
```
✓ Python 3.11.x
✓ PostgreSQL 15.x atau 16.x
```

### 2. Jalankan script ini:
```
Double-click → QUICK_START.bat
```

### 3. Tunggu selesai (~20-30 menit)

### 4. Akses aplikasi:
```
Browser: http://localhost:4321
```

### 5. Login dengan superuser yang Anda buat

---

## 📋 WORKFLOW SETUP

### FIRST TIME SETUP:
```
Install Python & PostgreSQL
        ↓
Read: SETUP_SUMMARY.md
        ↓
Read: SETUP_WINDOWS_SERVER_2016_LENGKAP.md (optional, untuk detail)
        ↓
Run: QUICK_START.bat (automatic setup)
        ↓
Verify: Gunakan CHECKLIST_SETUP.md
        ↓
✓ DONE! Aplikasi siap digunakan
```

### DAILY USAGE:
```
Run: run_server.bat
        ↓
Browser: http://localhost:4321
        ↓
Login & gunakan aplikasi
        ↓
Stop: Ctrl+C untuk stop server
```

### TROUBLESHOOTING:
```
Ada error?
        ↓
Read: TROUBLESHOOTING.md
        ↓
Find: Solusi untuk error Anda
        ↓
✓ DONE!
```

---

## 🎯 PANDUAN SINGKAT BERDASARKAN KONDISI

### Saya ingin setup aplikasi untuk pertama kali:
1. Buka: **SETUP_SUMMARY.md**
2. Ikuti: "QUICK START" section
3. Jalankan: **QUICK_START.bat**

### Saya ingin tahu detail setup lengkap:
1. Buka: **SETUP_WINDOWS_SERVER_2016_LENGKAP.md**
2. Baca: Section yang relevan
3. Ikuti: Step-by-step manual

### Saya dapat error/masalah:
1. Buka: **TROUBLESHOOTING.md**
2. Cari: Problem yang sama
3. Ikuti: Solusi yang disediakan

### Saya ingin verify setup sudah benar:
1. Gunakan: **CHECKLIST_SETUP.md**
2. Centang: Setiap item
3. Verify: Semua item ✓

### Saya ingin menjalankan aplikasi setiap hari:
1. Jalankan: **run_server.bat**
2. Akses: http://localhost:4321
3. Login & gunakan
4. Stop: Ctrl+C untuk exit

---

## 🔧 MANUAL COMMANDS (Jika tidak ingin pakai script)

### Setup awal (manual):
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate.bat

# 3. Install packages
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run server
python manage.py runserver 0.0.0.0:4321
```

### Run server setiap hari:
```bash
# 1. Activate virtual environment
venv\Scripts\activate.bat

# 2. Run server
python manage.py runserver 0.0.0.0:4321

# 3. Open browser
http://localhost:4321
```

---

## 💾 DATABASE CREDENTIALS

**Default Configuration:**

| Item | Value |
|------|-------|
| Database | manajemen_pekerjaan_db |
| User | manajemen_app_user |
| Password | AppsPassword123! |
| Host | localhost |
| Port | 5432 |

⚠️ **IMPORTANT**: Ubah password untuk production!

---

## 🌐 NETWORK ACCESS

### Local Access (same computer):
```
http://localhost:4321
```

### Network Access (from other computer):
```
http://[SERVER_IP]:4321

Contoh: http://192.168.1.100:4321
```

**Catatan**: Kedua komputer harus dalam network yang sama (same LAN).

---

## ❓ FAQ

### Q: Port 4321 sudah digunakan aplikasi lain?
A: Ubah port dengan command:
```bash
python manage.py runserver 0.0.0.0:8000
```

### Q: Bagaimana caranya backup database?
A: Gunakan command:
```bash
pg_dump -U manajemen_app_user -d manajemen_pekerjaan_db > backup.sql
```

### Q: Bagaimana caranya restore database?
A: Gunakan command:
```bash
psql -U manajemen_app_user -d manajemen_pekerjaan_db < backup.sql
```

### Q: Script .bat error "ExecutionPolicy"?
A: Jalankan di Command Prompt (bukan PowerShell) atau ubah execution policy:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: Saya lupa password superuser?
A: Buat superuser baru dengan:
```bash
python manage.py createsuperuser
```

---

## 📞 SUPPORT

Jika ada pertanyaan atau masalah:

1. **Cek dokumentasi** di folder ini
2. **Baca TROUBLESHOOTING.md** untuk solusi
3. **Hubungi developer** jika tidak ketemu solusinya

---

## 📝 CATATAN PENTING

⚠️ **SEBELUM PRODUCTION:**
- [ ] Ganti `SECRET_KEY` di `config/settings.py`
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS` dengan domain/IP production
- [ ] Ganti password PostgreSQL
- [ ] Ganti password superuser
- [ ] Setup SSL/HTTPS
- [ ] Use production server (Gunicorn + Nginx)

---

## 📚 DAFTAR FILE LENGKAP

```
📁 panduan/
├── 📖 README.md (FILE INI)
├── 📖 SETUP_SUMMARY.md ⭐ START HERE
├── 📖 SETUP_WINDOWS_SERVER_2016_LENGKAP.md
├── 📖 CHECKLIST_SETUP.md
├── 📖 TROUBLESHOOTING.md
├── 🤖 QUICK_START.bat ⭐ RUN THIS
├── 🤖 setup_postgres_db.bat
├── 🤖 setup_project.bat
├── 🤖 run_migrations.bat
└── 🤖 run_server.bat
```

---

## 🎓 LEARNING RESOURCES

### Untuk pemula:
- Django Documentation: https://docs.djangoproject.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Python Documentation: https://docs.python.org/3/

### Tutorial:
- Django Tutorial: https://docs.djangoproject.com/en/stable/intro/
- PostgreSQL Tutorial: https://www.postgresql.org/docs/current/tutorial.html

---

## 📦 PROJECT STRUCTURE

```
proyek_manajemen_job/
├── config/                  # Django configuration
│   ├── settings.py         # Main settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── core/                    # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URLs
│   └── migrations/        # Database migrations
├── templates/              # HTML templates
├── media/                  # Uploaded files
├── panduan/                # This folder (guides)
├── manage.py              # Django management command
└── requirements.txt        # Python dependencies
```

---

## ✅ VERIFICATION

Untuk verify setup sudah benar, run:

```bash
# Check Python
python --version

# Check PostgreSQL
psql --version

# Check Django
python manage.py check

# Check database
python manage.py dbshell
```

---

## 🚀 READY TO GO!

Sekarang Anda siap untuk setup & menggunakan aplikasi Manajemen Job.

**Mulai dari**: [`SETUP_SUMMARY.md`](SETUP_SUMMARY.md)

**Atau langsung jalankan**: [`QUICK_START.bat`](QUICK_START.bat)

---

**Last Updated**: November 24, 2025  
**Created**: Development Team  
**Version**: 1.0
