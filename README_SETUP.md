# 📚 PANDUAN LENGKAP SETUP SERVER LOKAL

Berikut adalah dokumentasi lengkap untuk setup project **Proyek Manajemen Job** di server lokal Anda dengan PostgreSQL dan auto-running.

---

## 📂 FILE DOKUMENTASI YANG SUDAH DIBUAT

### 1. **QUICK_START.md** (👈 MULAI DARI SINI!)
   - Quick setup dalam 5-7 langkah
   - Paling singkat dan mudah diikuti
   - **Waktu:** ~30 menit
   - **Untuk:** Setup cepat pertama kali

### 2. **SETUP_SERVER_LOKAL.md** (Dokumentasi Lengkap)
   - Penjelasan detail setiap step
   - Multiple opsi untuk auto-start
   - Troubleshooting guide
   - **Untuk:** Pemahaman mendalam

### 3. **requirements.txt** (Dependencies List)
   - Semua Python packages yang dibutuhkan
   - Versions sudah ditentukan
   - Install: `pip install -r requirements.txt`

### 4. **Helper Scripts (.bat files)**

   **setup_database.bat**
   - Otomatis buat database & user PostgreSQL
   - Jalankan 1x sebagai Administrator
   - Output: Database siap digunakan

   **setup_environment.bat**
   - Buat venv dan install dependencies
   - Jalankan 1x sebagai Administrator
   - Jalankan migrasi database

   **run_server.bat**
   - Jalankan Django server di port 1234
   - Bisa di-copy ke Startup folder untuk auto-start
   - Simple dan gampang di-debug

### 5. **settings_production_example.py** (Referensi)
   - Contoh production settings
   - PostgreSQL configuration
   - Security best practices

---

## 🎯 REKOMENDASI SETUP

### Opsi A: Setup CEPAT (30 menit)
Untuk yang ingin langsung jalan:
1. Clone project dari GitHub
2. Jalankan `setup_database.bat` (buat database)
3. Jalankan `setup_environment.bat` (setup dependencies)
4. Edit `config/settings.py` (sesuaikan credentials)
5. Test: `python manage.py runserver 0.0.0.0:1234`
6. Copy `run_server.bat` ke Startup folder

**Dokumentasi:** Ikuti `QUICK_START.md`

---

### Opsi B: Setup DETAIL (1-2 jam)
Untuk yang ingin memahami setiap step:
1. Baca `SETUP_SERVER_LOKAL.md` dari awal
2. Install PostgreSQL secara manual
3. Setup database step-by-step
4. Understand setiap konfigurasi
5. Setup NSSM Service untuk production-grade auto-start

**Dokumentasi:** Ikuti `SETUP_SERVER_LOKAL.md`

---

## 📊 PERBANDINGAN OPSI AUTO-START

| Opsi | Setup | Kemudahan | Reliability | Terbaik Untuk |
|------|-------|----------|------------|--------------|
| **Task Scheduler** | ⭐ Super Mudah | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Personal use, simple setup |
| **Startup Folder** | ⭐ Paling Mudah | ⭐⭐⭐⭐⭐ | ⭐⭐ | Development, learning |
| **NSSM Service** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | Production, server farms |

**Rekomendasi untuk Anda:** Task Scheduler atau Startup Folder (paling mudah)

---

## 🔧 STEP BY STEP FLOW

```
START
  ↓
[1] Clone dari GitHub
  ↓
[2] Install PostgreSQL (jika belum)
  ↓
[3] Buat Database & User → run setup_database.bat
  ↓
[4] Setup Environment → run setup_environment.bat
  ↓
[5] Edit config/settings.py (ubah DB credentials)
  ↓
[6] Test Manual → python manage.py runserver 0.0.0.0:1234
  ↓
[7] Setup Auto-Start (pilih salah satu):
     • Task Scheduler (Recommended)
     • Startup Folder
     • NSSM Service
  ↓
[8] Restart Komputer & Verify
  ↓
END ✅
```

---

## 📋 CHECKLIST SETUP

- [ ] PostgreSQL terinstall & berjalan
- [ ] Database `proyek_manajemen_job` dibuat
- [ ] User `django_user` dibuat
- [ ] Project di-clone dari GitHub
- [ ] `setup_environment.bat` sudah dijalankan
- [ ] Dependencies terinstall via `pip install -r requirements.txt`
- [ ] `python manage.py migrate` berhasil
- [ ] `python manage.py createsuperuser` dibuat
- [ ] `config/settings.py` sudah di-update dengan PostgreSQL
- [ ] Test manual: `python manage.py runserver 0.0.0.0:1234` ✓
- [ ] Auto-start dikonfigurasi
- [ ] Komputer di-restart dan app masih berjalan

---

## 🌐 AKSES SETELAH SETUP

### Dari Komputer Server Sendiri:
```
http://localhost:1234              ← Web app
http://127.0.0.1:1234             ← Alternative
http://localhost:1234/admin       ← Admin panel
http://localhost:1234/job-per-day ← Export jobs
```

### Dari Komputer Lain (di jaringan yang sama):
```
http://192.168.1.x:1234           ← Ganti x dengan IP server Anda
```

### Cek IP Server:
```powershell
ipconfig
# Cari: IPv4 Address (biasanya 192.168.x.x atau 10.x.x.x)
```

---

## 🆘 QUICK HELP

| Problem | Solusi Cepat |
|---------|-------------|
| PostgreSQL tidak terkoneksi | `Get-Service postgresql-x64-15` / Start jika tidak running |
| Dependencies error | `pip install -r requirements.txt` |
| Port 1234 sudah terpakai | Ubah port di `run_server.bat` atau kill process: `taskkill /PID <PID> /F` |
| Admin panel blank | `python manage.py collectstatic --noinput` |
| Auto-start tidak bekerja | Cek Task Scheduler / NSSM service status |

---

## 📞 SUPPORT RESOURCES

- **GitHub Repo:** https://github.com/fastabiqhidayatulah/proyek_manajemen_job
- **Documentation:** Baca SETUP_SERVER_LOKAL.md atau QUICK_START.md
- **Issues:** Report di GitHub Issues

---

## ⚡ TIPS & TRICKS

1. **Backup Database Regularly**
   ```powershell
   pg_dump -U django_user -d proyek_manajemen_job > backup.sql
   ```

2. **Monitor Service**
   ```powershell
   Get-Process python
   ```

3. **View Logs**
   ```powershell
   # Logs akan tersimpan di folder logs/ jika dikonfigurasi
   ```

4. **Reset Database (Development)**
   ```powershell
   python manage.py flush  # Delete all data
   python manage.py migrate
   python manage.py createsuperuser
   ```

---

## 📅 Version Info

- **Django:** 5.2.8
- **Python:** 3.10+
- **PostgreSQL:** 13+
- **Bootstrap:** 5.3.3
- **Created:** November 24, 2025

---

**Siap untuk setup? Mulai dengan membaca: `QUICK_START.md`** 🚀
