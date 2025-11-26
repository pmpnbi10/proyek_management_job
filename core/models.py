from django.db import models
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey
import os 
import json 
from django.core.serializers.json import DjangoJSONEncoder 

# ==============================================================================
# 1. MODEL AKUN / USER (UNTUK LOGIN)
# ==============================================================================
class Jabatan(models.Model):
    nama_jabatan = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name = "Jabatan"
        verbose_name_plural = "Daftar Jabatan" 
    def __str__(self):
        return self.nama_jabatan

class CustomUser(AbstractUser):
    jabatan = models.ForeignKey(Jabatan, on_delete=models.SET_NULL, null=True, blank=True)
    atasan = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='bawahan' 
    )
    class Meta:
        verbose_name = "Pengguna"
        verbose_name_plural = "Daftar Pengguna" 
    def __str__(self):
        return self.username
    
    def get_all_subordinates(self):
        subordinates = []
        direct_subs = self.bawahan.all()
        for sub in direct_subs:
            subordinates.append(sub.id)
            subordinates.extend(sub.get_all_subordinates())
        return list(set(subordinates)) 

# ==============================================================================
# 2. MODEL PERSONIL (ANAK BUAH / BUKAN USER LOGIN)
# ==============================================================================
class Personil(models.Model):
    nama_lengkap = models.CharField(max_length=200)
    penanggung_jawab = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='personil_team' 
    )
    class Meta:
        verbose_name = "Personil"
        verbose_name_plural = "Daftar Personil" 
    def __str__(self):
        return f"{self.nama_lengkap} (Team: {self.penanggung_jawab.username})"

# ==============================================================================
# 3. MODEL ASET (LINE, MESIN, SUB MESIN)
# ==============================================================================
class AsetMesin(MPTTModel):
    nama = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    class MPTTMeta:
        order_insertion_by = ['nama']
    class Meta:
        verbose_name = "Aset Mesin"
        verbose_name_plural = "Daftar Aset Mesin" 
    def __str__(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
            return ' > '.join([ancestor.nama for ancestor in ancestors])
        except:
            return self.nama

# ==============================================================================
# 4. MODEL PROJECT
# ==============================================================================
class Project(models.Model):
    nama_project = models.CharField(max_length=255)
    deskripsi = models.TextField(blank=True, null=True)
    manager_project = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True, 
        related_name='projects_managed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Daftar Project" 
        ordering = ['-created_at']
    def __str__(self):
        return self.nama_project

# ==============================================================================
# 5. MODEL PEKERJAAN (JOB) DAN LAMPIRANNYA
# ==============================================================================
class Job(models.Model):
    TIPE_JOB_CHOICES = [
        ('Daily', 'Daily Job'),
        ('Project', 'Project Job'),
    ]
    # === TAMBAHKAN 2 FIELD BARU INI ===
    FOKUS_CHOICES = [
        ('Perawatan', 'Perawatan'),
        ('Perbaikan', 'Perbaikan'),
        ('Proyek', 'Proyek'),
        ('Lainnya', 'Lainnya'),
    ]
    PRIORITAS_CHOICES = [
        ('P1', 'P1 - Mendesak'),
        ('P2', 'P2 - Tinggi'),
        ('P3', 'P3 - Normal'),
        ('P4', 'P4 - Rendah'),
    ]
    # =====================================
    
    nama_pekerjaan = models.CharField(max_length=255)
    tipe_job = models.CharField(max_length=10, choices=TIPE_JOB_CHOICES, default='Daily')
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='jobs' 
    )
    
    aset = models.ForeignKey(
        AsetMesin, 
        on_delete=models.SET_NULL, 
        null=True,
        help_text="Pilih Sub Mesin (level terendah)"
    )
    
    pic = models.ForeignKey(
        CustomUser, 
        on_delete=models.PROTECT, 
        related_name='jobs_created',
        help_text="User yang membuat/bertanggung jawab (Foreman, dll)"
    )
    
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='jobs_assigned_to_me',
        help_text="Bawahan yang ditugaskan job ini (opsional)"
    )

    personil_ditugaskan = models.ManyToManyField(
        Personil, 
        related_name='jobs_assigned',
        blank=True, 
        help_text="Pilih satu atau beberapa personil"
    )
    
    status = models.CharField(
        max_length=50, 
        default='Open', 
        editable=True   
    )
    
    # === TAMBAHKAN 2 FIELD BARU INI ===
    fokus = models.CharField(
        max_length=50, 
        choices=FOKUS_CHOICES, 
        default='Perawatan',
        null=True, blank=True
    )
    prioritas = models.CharField(
        max_length=10, 
        choices=PRIORITAS_CHOICES, 
        default='P3',
        null=True, blank=True
    )
    # =====================================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pekerjaan (Job)"
        verbose_name_plural = "Daftar Pekerjaan (Job)" 
        ordering = ['-updated_at']

    def __str__(self):
        return self.nama_pekerjaan

    def get_dates_json(self):
        """ Helper untuk kalender Flatpickr. """
        dates = list(self.tanggal_pelaksanaan.all().values_list('tanggal', flat=True))
        return json.dumps(dates, cls=DjangoJSONEncoder)

    def get_progress_percent(self):
        """
        Menghitung persentase progres berdasarkan tanggal yang 'Done'.
        """
        total_dates = self.tanggal_pelaksanaan.count()
        if total_dates == 0:
            return 0 # Tidak ada tanggal, progres 0
            
        done_dates = self.tanggal_pelaksanaan.filter(status='Done').count()
        
        # Hitung persentase
        progress = (done_dates / total_dates) * 100
        return int(progress) # Kembalikan sebagai integer (misal: 50)


class JobDate(models.Model):
    """
    Model terpisah untuk menangani multi-tanggal yang tidak berurutan.
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='tanggal_pelaksanaan')
    tanggal = models.DateField()

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Done', 'Done'),
        ('Pending', 'Pending'),
        ('N/A', 'N/A'), # Misal: Libur atau Mesin Rusak
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Open' # Saat tanggal dibuat, statusnya 'Open'
    )
    
    catatan = models.TextField(
        blank=True, 
        null=True,
        help_text="Catatan untuk pekerjaan di tanggal ini"
    )

    class Meta:
        unique_together = ('job', 'tanggal')
        ordering = ['tanggal']
        verbose_name = "Tanggal Pengerjaan"
        verbose_name_plural = "Tanggal Pengerjaan" 

    def __str__(self):
        return f"{self.job.nama_pekerjaan} - {self.tanggal} ({self.status})"

class Attachment(models.Model):
    """
    Model terpisah untuk menangani multi-lampiran (Gambar, Dokumen).
    """
    TIPE_FILE_CHOICES = [
        ('Image', 'Gambar'),
        ('Document', 'Dokumen'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    deskripsi = models.CharField(max_length=255, blank=True, null=True)
    tipe_file = models.CharField(max_length=10, choices=TIPE_FILE_CHOICES, default='Image')
    
    class Meta:
        verbose_name = "Lampiran"
        verbose_name_plural = "Daftar Lampiran" 

    def __str__(self):
        try:
            return os.path.basename(self.file.name)
        except:
            return "File Lampiran"


# ==============================================================================
# 6. MODEL KARYAWAN (MASTER DATA - BERBEDA DARI CUSTOM USER/LOGIN)
# ==============================================================================
class Karyawan(models.Model):
    """
    Model untuk master data Karyawan
    Berbeda dari CustomUser (akun login aplikasi)
    Bisa diimport dari Excel dengan NIK + Nama
    """
    nik = models.CharField(
        max_length=20, 
        unique=True,
        verbose_name="NIK",
        help_text="Nomor Induk Karyawan"
    )
    nama_lengkap = models.CharField(
        max_length=255,
        verbose_name="Nama Lengkap"
    )
    departemen = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Departemen"
    )
    posisi = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Posisi"
    )
    status = models.CharField(
        max_length=50,
        default='Aktif',
        choices=[
            ('Aktif', 'Aktif'),
            ('Tidak Aktif', 'Tidak Aktif'),
            ('Cuti', 'Cuti'),
            ('Keluar', 'Keluar'),
        ],
        verbose_name="Status Karyawan"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Karyawan"
        verbose_name_plural = "Daftar Karyawan"
        ordering = ['nik']
    
    def __str__(self):
        return f"{self.nik} - {self.nama_lengkap}"


# ==============================================================================
# 7. MODEL LEAVE EVENT (IJIN/CUTI KE GOOGLE CALENDAR)
# ==============================================================================
class LeaveEvent(models.Model):
    """
    Model untuk track Ijin/Cuti yang di-sync ke Google Calendar
    """
    TIPE_LEAVE_CHOICES = [
        ('Ijin', 'Ijin'),
        ('Cuti', 'Cuti'),
    ]
    
    # ForeignKey ke Karyawan (master data)
    karyawan = models.ForeignKey(
        Karyawan,
        on_delete=models.CASCADE,
        related_name='leave_events',
        verbose_name="Karyawan",
        null=True,
        blank=True
    )
    
    # Keep old field untuk backward compatibility (akan deprecated)
    nama_orang = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Deprecated - gunakan karyawan field"
    )
    
    tipe_leave = models.CharField(
        max_length=10, 
        choices=TIPE_LEAVE_CHOICES, 
        default='Ijin'
    )
    
    # Untuk support multi-date, simpan sebagai comma-separated
    # Format: YYYY-MM-DD,YYYY-MM-DD,...
    tanggal = models.TextField(
        help_text="Tanggal single atau range (comma-separated). Format: YYYY-MM-DD"
    )
    
    deskripsi = models.TextField(
        blank=True, 
        null=True,
        help_text="Keterangan tambahan"
    )
    
    # Link ke Google Calendar
    google_event_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Event ID dari Google Calendar"
    )
    
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='leave_events_created'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Leave Event"
        verbose_name_plural = "Daftar Leave Events"
        ordering = ['-created_at']
    
    def __str__(self):
        nama = self.karyawan.nama_lengkap if self.karyawan else self.nama_orang
        return f"{nama} - {self.tipe_leave} ({self.tanggal})"
    
    def get_tanggal_list(self):
        """Parse comma-separated dates into list"""
        return [tgl.strip() for tgl in self.tanggal.split(',') if tgl.strip()]