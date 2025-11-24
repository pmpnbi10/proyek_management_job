from django import forms
from django.forms import inlineformset_factory 
from .models import Personil, Job, JobDate, Attachment, AsetMesin, Project, CustomUser 

# ==============================================================================
# FORM PERSONIL (Tidak berubah)
# ==============================================================================
class PersonilForm(forms.ModelForm):
    class Meta:
        model = Personil
        fields = ['nama_lengkap']
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama lengkap anak buah'
            })
        }
        labels = {
            'nama_lengkap': 'Nama Lengkap Personil'
        }

# ==============================================================================
# FORM PROJECT (Tidak berubah)
# ==============================================================================
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['nama_project', 'deskripsi']
        widgets = {
            'nama_project': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Misal: Project Instalasi Mesin Baru'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4
            }),
        }
        labels = {
            'nama_project': 'Nama Project',
            'deskripsi': 'Deskripsi Singkat (Opsional)',
        }

# ==============================================================================
# FORM MODAL STATUS TANGGAL (Tidak berubah)
# ==============================================================================
class JobDateStatusForm(forms.ModelForm):
    class Meta:
        model = JobDate
        fields = ['status', 'catatan']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'catatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'status': 'Ubah Status Menjadi',
            'catatan': 'Catatan (Opsional)',
        }


# ==============================================================================
# FORM PEKERJAAN (JOB) (DIPERBARUI)
# ==============================================================================
class JobForm(forms.ModelForm):
    
    line = forms.ModelChoiceField(
        queryset=AsetMesin.objects.filter(level=0), # Level 0 = Line
        label="Line",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_line'})
    )
    mesin = forms.ModelChoiceField(
        queryset=AsetMesin.objects.none(), # Kosong, diisi JS
        label="Mesin",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_mesin'})
    )
    sub_mesin = forms.ModelChoiceField(
        queryset=AsetMesin.objects.none(), # Kosong, diisi JS
        label="Sub Mesin",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_sub_mesin'})
    )

    tanggal_pelaksanaan = forms.CharField(
        label="Tanggal Pelaksanaan",
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'id_tanggal_pelaksanaan_hidden'})
    )
    
    assigned_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),
        label="Assign To (Pilih Bawahan)",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_assigned_to'})
    )

    class Meta:
        model = Job
        fields = [
            'nama_pekerjaan', 
            'tipe_job', 
            'project',
            'assigned_to',  # <-- TAMBAHKAN
            'fokus',
            'prioritas',
            'personil_ditugaskan',
            'tanggal_pelaksanaan' 
        ]
        labels = {
            'nama_pekerjaan': 'Nama Pekerjaan',
            'tipe_job': 'Tipe Pekerjaan',
            'project': 'Nama Project',
            'fokus': 'Fokus Pekerjaan',
            'prioritas': 'Prioritas',
            'personil_ditugaskan': 'Personil Yang Ditugaskan',
        }
        widgets = {
            'personil_ditugaskan': forms.SelectMultiple(
                attrs={'class': 'form-select', 'size': '5'}
            )
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        project = kwargs.pop('project', None) # Ambil project (jika ada)
        super().__init__(*args, **kwargs)

        # Style Bootstrap
        self.fields['nama_pekerjaan'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Misal: Pengecekan Harian Panel X'})
        self.fields['tipe_job'].widget.attrs.update({'class': 'form-select'})
        self.fields['project'].widget.attrs.update({'class': 'form-select'})
        self.fields['fokus'].widget.attrs.update({'class': 'form-select'})
        self.fields['prioritas'].widget.attrs.update({'class': 'form-select'})
        self.fields['assigned_to'].widget.attrs.update({'class': 'form-select'})  # <-- TAMBAHKAN
        
        self.fields['personil_ditugaskan'].required = False 
        self.fields['personil_ditugaskan'].help_text = "Tahan Ctrl (atau Cmd di Mac) untuk memilih lebih dari satu."

        # === LOGIKA ASSIGN_TO: Isi dengan daftar bawahan user ===
        if user:
            # Get all subordinates dari current user
            subordinate_ids = user.get_all_subordinates()
            
            # Jika ada subordinates, tampilkan di dropdown
            if subordinate_ids:
                self.fields['assigned_to'].queryset = CustomUser.objects.filter(
                    id__in=subordinate_ids
                ).order_by('username')
            else:
                # Jika tidak ada subordinates, hide/kosongkan dropdown
                self.fields['assigned_to'].queryset = CustomUser.objects.none()
            
            # === SET DEFAULT PERSONIL QUERYSET (PENTING!) ===
            # Default: gunakan personil milik user sendiri (untuk initial load)
            default_personil = Personil.objects.filter(
                penanggung_jawab=user
            ).order_by('nama_lengkap')
            
            # Filter 'personil' berdasarkan 'assigned_to' atau user sendiri
            if self.data:
                # POST request - ada data dari form
                try:
                    assigned_to_id = int(self.data.get('assigned_to')) if self.data.get('assigned_to') else None
                    if assigned_to_id:
                        # Jika assigned_to dipilih, tampilkan personil milik bawahan itu
                        self.fields['personil_ditugaskan'].queryset = Personil.objects.filter(
                            penanggung_jawab_id=assigned_to_id
                        ).order_by('nama_lengkap')
                    else:
                        # Jika tidak dipilih, tampilkan personil milik user sendiri
                        self.fields['personil_ditugaskan'].queryset = default_personil
                except (ValueError, TypeError):
                    self.fields['personil_ditugaskan'].queryset = default_personil
            elif self.instance and self.instance.pk and self.instance.assigned_to:
                # GET request (Edit mode) - jika sudah ada assigned_to, gunakan personil milik mereka
                self.fields['personil_ditugaskan'].queryset = Personil.objects.filter(
                    penanggung_jawab=self.instance.assigned_to
                ).order_by('nama_lengkap')
                self.fields['assigned_to'].initial = self.instance.assigned_to.id
            else:
                # Default: gunakan personil milik user sendiri
                self.fields['personil_ditugaskan'].queryset = default_personil
        else:
            # Fallback jika user kosong (edge case)
            self.fields['assigned_to'].queryset = CustomUser.objects.none()
            self.fields['personil_ditugaskan'].queryset = Personil.objects.none()
        
        # Sembunyikan 'project' awalnya
        self.fields['project'].required = False
        
        # === LOGIKA BARU: Jika menambah job dari halaman project ===
        if project:
            self.fields['project'].initial = project.id
            self.fields['project'].widget = forms.HiddenInput()
            self.fields['tipe_job'].initial = 'Project'
            self.fields['tipe_job'].widget = forms.HiddenInput()
        
        # === LOGIKA BARU: HIDE/DISABLE assigned_to field jika user bukan PIC (pembuat) ===
        # Saat EDIT mode dan user BUKAN pembuat job, jangan tampilkan assigned_to field
        if self.instance and self.instance.pk and user:
            if self.instance.pic != user:
                # User bukan PIC - HIDE assigned_to field dari form
                # Tapi tetap include di data supaya tidak error saat save
                self.fields['assigned_to'].widget = forms.HiddenInput()
                self.fields['assigned_to'].initial = self.instance.assigned_to.id if self.instance.assigned_to else None
        
        # 1. Jika ada data POST (terjadi saat validasi error)
        if self.data:
            try:
                line_id = int(self.data.get('line'))
                if line_id:
                    self.fields['mesin'].queryset = AsetMesin.objects.filter(parent_id=line_id).order_by('nama')
                
                mesin_id = int(self.data.get('mesin'))
                if mesin_id:
                     self.fields['sub_mesin'].queryset = AsetMesin.objects.filter(parent_id=mesin_id).order_by('nama')
            
            except (ValueError, TypeError):
                pass 
        
        # 2. Jika mode Edit (GET) dan TIDAK ada data POST
        elif self.instance and self.instance.pk and self.instance.aset:
            aset = self.instance.aset 
            if aset.level == 2: 
                mesin = aset.parent
                line = mesin.parent
                self.fields['line'].initial = line.id
                self.fields['mesin'].queryset = AsetMesin.objects.filter(parent=line)
                self.fields['mesin'].initial = mesin.id
                self.fields['sub_mesin'].queryset = AsetMesin.objects.filter(parent=mesin)
                self.fields['sub_mesin'].initial = aset.id
            elif aset.level == 1: 
                mesin = aset
                line = mesin.parent
                self.fields['line'].initial = line.id
                self.fields['mesin'].queryset = AsetMesin.objects.filter(parent=line)
                self.fields['mesin'].initial = mesin.id
            elif aset.level == 0: 
                line = aset
                self.fields['line'].initial = line.id

    def clean(self):
        """Override clean untuk handle assigned_to hidden field"""
        cleaned_data = super().clean()
        
        # Jika assigned_to widget adalah HiddenInput, gunakan initial value
        # Ini mencegah validation error untuk subordinate yang edit job
        if isinstance(self.fields['assigned_to'].widget, forms.HiddenInput):
            if 'assigned_to' in self.errors:
                # Remove error jika field adalah hidden input
                del self.errors['assigned_to']
            # Set value dari initial
            if self.instance and self.instance.assigned_to:
                cleaned_data['assigned_to'] = self.instance.assigned_to
            else:
                cleaned_data['assigned_to'] = None
        
        return cleaned_data

# ==============================================================================
# FORMSET UNTUK LAMPIRAN (Tidak berubah)
# ==============================================================================
class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file', 'deskripsi', 'tipe_file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'deskripsi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deskripsi file'}),
            'tipe_file': forms.Select(attrs={'class': 'form-select'}),
        }

AttachmentFormSet = inlineformset_factory(
    Job,
    Attachment,
    form=AttachmentForm,
    extra=1,
    can_delete=True
)