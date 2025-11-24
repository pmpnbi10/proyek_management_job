# SETUP untuk Windows Server 2012

## Step 1: Upgrade pip & tools
```powershell
cd D:\server_apps\proyek_manajemen_job
.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel
```

## Step 2: Install basic dependencies (tanpa Pillow & weasyprint)
```powershell
pip install -r requirements.txt
```

## Step 3: Migrasi database
```powershell
python manage.py migrate
```

## Step 4: Buat superuser
```powershell
python manage.py createsuperuser
```

## Step 5: Test server
```powershell
python manage.py runserver 0.0.0.0:1234
```

Akses: http://localhost:1234

---

## Jika PDF export tidak jalan:

Anda bisa:
1. **Skip PDF export** - Hanya export ke Excel
2. **Install Pillow terpisah:**
   ```powershell
   pip install Pillow==9.5.0
   ```
3. **Gunakan cloud service** - Integrasikan dengan Google Docs API

---

## Note untuk Windows Server 2012:

- ✅ Django akan jalan normal
- ✅ PostgreSQL akan jalan normal
- ✅ Excel export akan jalan
- ⚠️ PDF export (weasyprint) mungkin tidak kompatibel
- ⚠️ Image upload (Pillow) mungkin perlu versi lebih lama

Coba jalankan Step 1-5 di atas dulu.
Report hasilnya! 👍
