#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import CustomUser, Personil
from core.forms import JobForm

# Get user hanif
try:
    hanif = CustomUser.objects.get(username='hanif')
    print(f"User: {hanif}")
    print(f"Personil milik hanif: {list(Personil.objects.filter(penanggung_jawab=hanif).values_list('nama_lengkap', flat=True))}")

    # Buat form instance
    form = JobForm(user=hanif)

    # Check queryset
    print(f"\nForm personil_ditugaskan queryset count: {form.fields['personil_ditugaskan'].queryset.count()}")
    print(f"Form personil_ditugaskan queryset: {list(form.fields['personil_ditugaskan'].queryset.values_list('nama_lengkap', flat=True))}")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
