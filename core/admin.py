from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

# Library untuk Import/Export Excel
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import (
    CustomUser, 
    Jabatan, 
    Personil, 
    AsetMesin, 
    Project, 
    Job, 
    JobDate, 
    Attachment
)

# ============================================================
# 1. SETUP IMPORT/EXPORT ASET (MASSAL)
# ============================================================
class AsetMesinResource(resources.ModelResource):
    # Memungkinkan import parent berdasarkan 'nama', bukan ID
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(AsetMesin, 'nama') 
    )

    class Meta:
        model = AsetMesin
        fields = ('id', 'nama', 'parent')
        import_id_fields = ('id',)

# ============================================================
# 2. SETUP ADMIN MODEL ASET (TREE VIEW + IMPORT)
# ============================================================
@admin.register(AsetMesin)
class AsetMesinAdmin(ImportExportModelAdmin, DraggableMPTTAdmin):
    resource_class = AsetMesinResource
    
    # Konfigurasi Tampilan Tree (Pohon)
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)
    
    # Penting untuk autocomplete_fields di JobAdmin
    search_fields = ('nama',) 

# ============================================================
# 3. SETUP CUSTOM USER (DENGAN JABATAN & ATASAN)
# ============================================================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Menambahkan field custom ke form edit user
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Tambahan', {'fields': ('jabatan', 'atasan')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informasi Tambahan', {'fields': ('jabatan', 'atasan')}),
    )
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'jabatan', 'atasan', 'is_staff']
    list_filter = UserAdmin.list_filter + ('jabatan', 'atasan',)
    
    # Penting untuk autocomplete_fields 'pic' di JobAdmin
    search_fields = ('username', 'first_name', 'last_name')

# ============================================================
# 4. SETUP PROJECT & PERSONIL
# ============================================================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('nama_project', 'deskripsi', 'created_at')
    search_fields = ('nama_project',)

@admin.register(Personil)
class PersonilAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'penanggung_jawab')
    list_filter = ('penanggung_jawab',)
    search_fields = ('nama_lengkap', 'penanggung_jawab__username')

@admin.register(Jabatan)
class JabatanAdmin(admin.ModelAdmin):
    list_display = ('nama_jabatan',)

# ============================================================
# 5. SETUP JOB (KOMPLEKS)
# ============================================================

class JobDateInline(admin.TabularInline):
    model = JobDate
    extra = 1
    fields = ('tanggal', 'status', 'catatan')

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    
    # Method Custom: Menampilkan list personil
    def get_personil_ditugaskan(self, obj):
        # PERBAIKAN: Menggunakan 'personil_ditugaskan' sesuai error log
        personil_list = obj.personil_ditugaskan.all()[:3] 
        names = [p.nama_lengkap for p in personil_list]
        if obj.personil_ditugaskan.count() > 3:
            names.append("...")
        return ", ".join(names)
    get_personil_ditugaskan.short_description = 'Personil Ditugaskan'
    
    # Method Custom: Progress Bar Visual
    def progress_bar(self, obj):
        # Cek apakah method get_progress_percent ada di model
        progress = getattr(obj, 'get_progress_percent', lambda: 0)()
        
        # Warna bar berdasarkan persentase
        color = "red"
        if progress >= 50: color = "orange"
        if progress >= 100: color = "green"

        return format_html(
            '''
            <div style="width: 100px; background-color: #e0e0e0; border-radius: 3px;">
                <div style="width: {}%; background-color: {}; height: 15px; border-radius: 3px;"></div>
            </div>
            <small>{}%</small>
            ''',
            progress, color, progress
        )
    progress_bar.short_description = 'Progress'

    # List Columns
    list_display = (
        'nama_pekerjaan', 
        'project', 
        'pic',
        'fokus',      
        'prioritas',  
        'get_personil_ditugaskan', 
        'progress_bar',
        'updated_at'
    )
    
    # Filters
    list_filter = ('project', 'fokus', 'prioritas', 'pic') 
    
    # Search
    search_fields = ('nama_pekerjaan', 'project__nama_project')
    
    # Inlines
    inlines = [JobDateInline, AttachmentInline]
    
    # Widget Khusus
    # PERBAIKAN: Menggunakan 'personil_ditugaskan'
    filter_horizontal = ('personil_ditugaskan',) 
    
    # Autocomplete (Search dropdown)
    # PERBAIKAN: Menggunakan 'aset' (bukan mesin/line) sesuai error log
    autocomplete_fields = ['project', 'aset', 'pic'] 

# Header Admin Panel
admin.site.site_header = "Admin Panel Manajemen Pekerjaan"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Selamat Datang di Admin Panel"