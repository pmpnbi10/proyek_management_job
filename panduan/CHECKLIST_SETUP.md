# ✅ CHECKLIST SETUP APLIKASI MANAJEMEN JOB

Gunakan checklist ini untuk memastikan setup sudah sempurna sebelum production.

---

## 📋 Pre-Setup Checklist

- [ ] Windows Server 2016 sudah siap (atau Windows 10/11)
- [ ] Administrator access tersedia
- [ ] Internet connection aktif
- [ ] Minimal 5GB free disk space
- [ ] Port 4321 & 5432 tersedia (tidak digunakan aplikasi lain)

---

## 🐍 Python Installation

- [ ] Python 3.11.x terinstall
- [ ] Python sudah di-add ke PATH
- [ ] Jalankan: `python --version` (berhasil menampilkan versi)
- [ ] Jalankan: `pip --version` (berhasil menampilkan versi)

---

## 🗄️ PostgreSQL Installation & Setup

- [ ] PostgreSQL 15.x atau 16.x terinstall
- [ ] PostgreSQL service berjalan (cek di Services)
- [ ] PostgreSQL sudah di-add ke PATH
- [ ] Jalankan: `psql --version` (berhasil menampilkan versi)
- [ ] Database `manajemen_pekerjaan_db` sudah dibuat
- [ ] User `manajemen_app_user` sudah dibuat
- [ ] User sudah diberi permission ke database
- [ ] Bisa login dengan: `psql -U manajemen_app_user -d manajemen_pekerjaan_db`

---

## 📁 Project Setup

- [ ] Project files sudah di-copy ke folder (contoh: `C:\Projects\proyek_manajemen_job`)
- [ ] Folder `venv` sudah ada (virtual environment)
- [ ] Jalankan: `.\venv\Scripts\Activate.ps1` atau `venv\Scripts\activate.bat` (berhasil)
- [ ] Jalankan: `pip list` (menampilkan packages yang terinstall)

---

## ⚙️ Django Configuration

File: `config/settings.py`

- [ ] `DATABASES['default']['NAME']` = `'manajemen_pekerjaan_db'`
- [ ] `DATABASES['default']['USER']` = `'manajemen_app_user'`
- [ ] `DATABASES['default']['PASSWORD']` = password yang benar
- [ ] `DATABASES['default']['HOST']` = `'localhost'`
- [ ] `DATABASES['default']['PORT']` = `'5432'`
- [ ] `ALLOWED_HOSTS` = `['localhost', '127.0.0.1', '192.168.1.*', '*']` (atau sesuai kebutuhan)
- [ ] `DEBUG` = `True` (untuk development, `False` untuk production)

---

## 🚀 Django Setup

- [ ] Jalankan: `python manage.py migrate` (berhasil tanpa error)
- [ ] Jalankan: `python manage.py createsuperuser` (superuser berhasil dibuat)
- [ ] Catat username & password superuser
- [ ] Jalankan: `python manage.py runserver 0.0.0.0:4321`
- [ ] Akses: `http://localhost:4321` (aplikasi berjalan)
- [ ] Login dengan superuser account
- [ ] Halaman dashboard bisa diakses

---

## 🌐 Network Access Test

- [ ] Dari komputer lain dalam network yang sama:
  - [ ] Akses: `http://[SERVER_IP]:4321` (berhasil)
  - [ ] Contoh: `http://192.168.1.100:4321`
  - [ ] Halaman login bisa ditampilkan
  - [ ] Bisa login dengan superuser

---

## 🔐 Security Checklist (Before Production)

- [ ] Ubah `SECRET_KEY` di `config/settings.py` ke random key baru
- [ ] Set `DEBUG = False` di `config/settings.py`
- [ ] Update `ALLOWED_HOSTS` dengan domain/IP production
- [ ] Ganti password superuser ke password yang kuat
- [ ] Ganti password PostgreSQL ke password yang kuat
- [ ] Review `DATABASES` settings untuk production
- [ ] Configure static files untuk production
- [ ] Configure media files untuk production

---

## 🛠️ Troubleshooting

Jika ada error, cek:

### Error: PostgreSQL tidak terinstall
- [ ] Install PostgreSQL dari https://www.postgresql.org/download/windows/
- [ ] Tambahkan PostgreSQL ke PATH
- [ ] Restart Command Prompt / PowerShell

### Error: Connection refused ke PostgreSQL
- [ ] Buka `services.msc`
- [ ] Cari service `postgresql-x64-XX` atau `postgresql-x86-XX`
- [ ] Pastikan status = "Running"
- [ ] Jika tidak, klik Start

### Error: Database does not exist
- [ ] Jalankan: `python manage.py migrate`

### Error: Port 4321 already in use
- [ ] Ganti port: `python manage.py runserver 0.0.0.0:8000`
- [ ] Atau tutup aplikasi lain yang menggunakan port 4321

### Error: ALLOWED_HOSTS error
- [ ] Pastikan IP address sudah ditambahkan di `config/settings.py`
- [ ] Gunakan `*` untuk allow semua (hanya untuk development!)

---

## 📞 Setup Verification Script

Jalankan script ini untuk verify semua setup:

```bash
REM Verify Python
python --version

REM Verify PostgreSQL
psql -U postgres -c "SELECT version();"

REM Verify Project
cd C:\Projects\proyek_manajemen_job
.\venv\Scripts\Activate.ps1
python manage.py check

REM Verify Database
python manage.py dbshell

REM Verify Server Start
python manage.py runserver 0.0.0.0:4321
```

---

## ✅ Final Verification

Sebelum declare "SETUP COMPLETE", pastikan:

- [ ] Semua checklist di atas ✅ Done
- [ ] Aplikasi bisa diakses dari browser (http://localhost:4321)
- [ ] Bisa login dengan superuser
- [ ] Database sudah berisi data (bisa cek di admin panel)
- [ ] Tidak ada error di server console
- [ ] Tidak ada error di browser console (F12)
- [ ] Network access bekerja dari komputer lain

---

**Status**: _____________________ (Date: ________________)

**Verification by**: ___________________

**Notes/Issues**:
```
_____________________________________
_____________________________________
_____________________________________
```

---

**Last Updated**: November 24, 2025
