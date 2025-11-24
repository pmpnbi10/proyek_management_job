# ==============================================================================
# EXPORT HANDLER - SEND DATA TO GOOGLE APPS SCRIPT
# ==============================================================================
import requests
import json
from django.http import JsonResponse
from .models import Job, CustomUser
from django.db.models import Q

# Google Apps Script URLs (JANGAN DIUBAH)
GAS_PREVENTIF_URL = "https://script.google.com/macros/s/AKfycbzcY5TMV0ImVm0IezEQIbcK_ZQw92ZQJTjvTi_w1Ic0aMAXPFBkB0dcDedBQB42eyiM/exec"
GAS_EVALUASI_URL = "https://script.google.com/macros/s/AKfycbxg2zPRso6f1bZQTuOxg2D2ey64a1iY6wWTKv-QmeZQBQIKDHjH8k2UT6wvSlgpZrOf2g/exec"


def prepare_job_data_for_export(job_ids, export_type="preventif"):
    """
    Prepare job data untuk export ke Google Apps Script
    Format disesuaikan dengan template Google Apps Script
    
    export_type: "preventif" atau "evaluasi"
    Returns: dict dengan structured data sesuai Google Apps Script template
    """
    jobs = Job.objects.filter(id__in=job_ids).select_related(
        'aset', 'aset__parent', 'aset__parent__parent'
    ).prefetch_related('personil_ditugaskan', 'tanggal_pelaksanaan')
    
    if not jobs.exists():
        return None
    
    # Ambil first job untuk tanggal (semua job seharusnya same day)
    first_job = jobs.first()
    tanggal = first_job.tanggal_pelaksanaan.first().tanggal if first_job.tanggal_pelaksanaan.exists() else None
    
    # Kumpulkan unique values
    mesin_set = set()
    sub_mesin_set = set()
    prioritas_set = set()
    job_data_list = []
    
    for job in jobs:
        # Collect unique mesin/sub mesin
        if job.aset:
            if job.aset.level == 2:  # Sub Mesin
                sub_mesin_set.add(job.aset.nama)
                if job.aset.parent:  # Mesin
                    mesin_set.add(job.aset.parent.nama)
            elif job.aset.level == 1:  # Mesin
                mesin_set.add(job.aset.nama)
        
        # Collect prioritas
        if job.prioritas:
            prioritas_set.add(job.get_prioritas_display())
        
        # Prepare job data row
        # Format berbeda untuk preventif vs evaluasi
        personil_names = ", ".join([p.nama_lengkap for p in job.personil_ditugaskan.all()])
        mesin_name = job.aset.parent.nama if job.aset and job.aset.level == 2 and job.aset.parent else (job.aset.nama if job.aset else "")
        sub_mesin_name = job.aset.nama if job.aset and job.aset.level == 2 else ""
        job_name = job.nama_pekerjaan
        
        if export_type == "preventif":
            # Preventif: [Personil, Mesin, SubMesin, DetailPekerjaan]
            job_data_list.append([
                personil_names,
                mesin_name,
                sub_mesin_name,
                job_name
            ])
        elif export_type == "evaluasi":
            # Evaluasi: [Personil, Mesin, SubMesin, DetailPekerjaan, Kesimpulan/Status]
            job_data_list.append([
                personil_names,
                mesin_name,
                sub_mesin_name,
                job_name,
                ""  # Kolom kesimpulan/status kosong (user isi di sheet)
            ])
    
    # Format payload sesuai Google Apps Script template
    payload = {
        "exportType": export_type,  # PENTING: Ada field ini untuk routing di Google Apps Script
        "tanggal": str(tanggal) if tanggal else "",
        "allMesin": ", ".join(sorted(mesin_set)) if mesin_set else "",
        "allSubMesin": ", ".join(sorted(sub_mesin_set)) if sub_mesin_set else "",
        "allPrioritas": ", ".join(sorted(prioritas_set)) if prioritas_set else "",
        "teknisiBertugas": "PIC/Teknisi",  # Can be customized later
        "jobData": job_data_list
    }
    
    return payload


def send_to_google_apps_script(payload, export_type="preventif"):
    """
    Send payload to Google Apps Script
    
    export_type: "preventif" atau "evaluasi"
    Returns: dict dengan status dan response
    """
    if export_type == "preventif":
        gas_url = GAS_PREVENTIF_URL
    elif export_type == "evaluasi":
        gas_url = GAS_EVALUASI_URL
    else:
        return {"status": "error", "message": "Jenis export tidak dikenali"}
    
    try:
        # Send POST request ke Google Apps Script
        response = requests.post(
            gas_url,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        return {
            "status": "success",
            "data": result,
            "message": result.get("message", "Data berhasil diekspor")
        }
    
    except requests.exceptions.Timeout:
        return {"status": "error", "message": "Request timeout - Google Apps Script tidak merespons"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "Connection error - Tidak bisa terhubung ke Google Apps Script"}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid JSON response dari Google Apps Script: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Error: {str(e)}"}

