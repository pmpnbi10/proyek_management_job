import datetime
from django.utils.translation import gettext as _

# ==============================================================================
# HELPER FUNCTIONS UNTUK EXPORT PDF
# ==============================================================================

def format_tanggal_id(date_obj):
    """
    Format tanggal ke format Indonesia (misal: 22 November 2025)
    """
    if not date_obj:
        return "-"
    
    months_id = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    
    return f"{date_obj.day} {months_id[date_obj.month]} {date_obj.year}"


def get_month_name_id(month_num):
    """
    Dapatkan nama bulan dalam Bahasa Indonesia
    """
    months_id = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    return months_id.get(month_num, "-")


def get_priority_badge_color(prioritas):
    """
    Dapatkan warna badge untuk prioritas job
    """
    color_map = {
        'P1': '#dc3545',  # Red
        'P2': '#fd7e14',  # Orange
        'P3': '#ffc107',  # Yellow
        'P4': '#198754',  # Green
    }
    return color_map.get(prioritas, '#6c757d')  # Gray default


def get_fokus_display(fokus):
    """
    Dapatkan display name untuk fokus
    """
    fokus_map = {
        'Perawatan': 'Perawatan',
        'Perbaikan': 'Perbaikan',
        'Proyek': 'Proyek',
        'Lainnya': 'Lainnya',
    }
    return fokus_map.get(fokus, fokus)


def calculate_daily_jobs_summary(job_data):
    """
    Hitung summary untuk Daily Jobs Report
    """
    total_jobs = len(job_data)
    
    # Hitung total tanggal dan yang Done
    total_dates = 0
    done_dates = 0
    
    for job in job_data:
        job_dates = job.tanggal_pelaksanaan.all()
        total_dates += job_dates.count()
        done_dates += job_dates.filter(status='Done').count()
    
    # Hitung persentase completion
    completion_percent = 0
    if total_dates > 0:
        completion_percent = int((done_dates / total_dates) * 100)
    
    # Hitung in progress (ada tanggal Open atau Pending)
    in_progress_count = 0
    for job in job_data:
        if job.tanggal_pelaksanaan.filter(status__in=['Open', 'Pending']).exists():
            in_progress_count += 1
    
    return {
        'total_jobs': total_jobs,
        'completed_jobs': len([j for j in job_data if j.get_progress_percent() == 100]),
        'in_progress_jobs': in_progress_count,
        'total_dates': total_dates,
        'done_dates': done_dates,
        'completion_percent': completion_percent,
    }


def calculate_project_jobs_summary(project_data):
    """
    Hitung summary untuk Project Jobs Report
    """
    total_projects = len(project_data)
    total_jobs = sum(len(p['jobs']) for p in project_data)
    
    total_dates = 0
    done_dates = 0
    
    for project_item in project_data:
        for job in project_item['jobs']:
            job_dates = job.tanggal_pelaksanaan.all()
            total_dates += job_dates.count()
            done_dates += job_dates.filter(status='Done').count()
    
    completion_percent = 0
    if total_dates > 0:
        completion_percent = int((done_dates / total_dates) * 100)
    
    in_progress_count = 0
    for project_item in project_data:
        for job in project_item['jobs']:
            if job.tanggal_pelaksanaan.filter(status__in=['Open', 'Pending']).exists():
                in_progress_count += 1
    
    return {
        'total_projects': total_projects,
        'total_jobs': total_jobs,
        'completed_jobs': len([j for p in project_data for j in p['jobs'] if j.get_progress_percent() == 100]),
        'in_progress_jobs': in_progress_count,
        'total_dates': total_dates,
        'done_dates': done_dates,
        'completion_percent': completion_percent,
    }


def generate_pdf_filename(report_type, year, month):
    """
    Generate nama file PDF yang deskriptif
    report_type: 'daily' atau 'project'
    """
    month_name = get_month_name_id(month)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if report_type == 'daily':
        filename = f"LAPORAN_DAILY_JOBS_{month_name}_{year}_{timestamp}.pdf"
    else:
        filename = f"LAPORAN_PROJECT_JOBS_{month_name}_{year}_{timestamp}.pdf"
    
    return filename
