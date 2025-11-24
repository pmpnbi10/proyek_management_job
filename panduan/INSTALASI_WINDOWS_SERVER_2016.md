# PANDUAN INSTALASI: Windows Server 2016

Panduan ini dibuat untuk menginstall aplikasi di Windows Server 2016 **tanpa mengubah kode sumber** secara otomatis. Anda perlu melakukan beberapa konfigurasi manual.

---

## 1. Persiapan Server (Wajib)

### A. Install Python
1. Download **Python 3.10** atau **3.11** dari [python.org](https://www.python.org/downloads/windows/).
2. Jalankan installer.
3. **PENTING**: Centang opsi **"Add Python to PATH"** di halaman pertama installer.
4. Klik "Install Now".

### B. Install PostgreSQL
1. Download & Install **PostgreSQL** (Versi 14 atau 15 direkomendasikan).
2. Saat instalasi, ingat password untuk user `postgres`.
3. Buka **pgAdmin** (aplikasi manajemen database bawaan PostgreSQL).
4. Buat Database Baru:
   - Klik kanan `Databases` > `Create` > `Database`.
   - Nama: `manajemen_pekerjaan_db`
5. Buat User Baru (Login Role):
   - Klik kanan `Login/Group Roles` > `Create` > `Login/Group Role`.
   - Tab **General**: Name = `manajemen_app_user`
   - Tab **Definition**: Password = `password_rahasia_app`
   - Tab **Privileges**: Centang "Can login?" (Yes).
   - **PENTING**: Berikan akses owner ke database `manajemen_pekerjaan_db` (klik kanan database > Properties > Owner > ganti ke `manajemen_app_user`).

---

## 2. Setup Aplikasi

Buka **PowerShell** atau **Command Prompt** (CMD) dan arahkan ke folder aplikasi.

Contoh:
```powershell
cd D:\server_apps\proyek_manajemen_job
```

### A. Buat Virtual Environment
```powershell
python -m venv venv
```

### B. Aktifkan Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(Jika muncul error "running scripts is disabled", ketik: `Set-ExecutionPolicy RemoteSigned` lalu pilih `Y`)*

### C. Install Library Pendukung
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Konfigurasi Manual (PENTING)

Karena kode tidak diubah otomatis, Anda **WAJIB** mengedit file konfigurasi agar bisa diakses dari komputer lain.

1. Buka file: `config/settings.py` (gunakan Notepad atau VS Code).
2. Cari baris `ALLOWED_HOSTS`.
3. Ubah dari:
   ```python
   ALLOWED_HOSTS = []
   ```
   Menjadi:
   ```python
   ALLOWED_HOSTS = ['*']
   ```
   *(Tanda `*` artinya mengizinkan akses dari semua IP. Untuk keamanan lebih, ganti `*` dengan IP server Anda, misal `['192.168.1.10']`)*.

4. Simpan file.

---

## 4. Jalankan Database Migrasi

Kembali ke PowerShell (pastikan venv aktif):

```powershell
python manage.py migrate
python manage.py createsuperuser
```
*(Ikuti instruksi untuk membuat username & password admin)*

---

## 5. Menjalankan Aplikasi

Untuk menjalankan server:

```powershell
python manage.py runserver 0.0.0.0:8000
```

### Cara Akses:
- Dari server itu sendiri: `http://localhost:8000`
- Dari komputer lain: `http://IP_SERVER_ANDA:8000` (Misal: `http://192.168.1.10:8000`)

> [!NOTE]
> **Catatan**: Pastikan **Firewall** Windows Server mengizinkan koneksi masuk ke port **8000**.
