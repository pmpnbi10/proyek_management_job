from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # URL Halaman Utama/Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # URL Job Per Day (BARU - untuk export Google Apps Script)
    path('job-per-day/', views.job_per_day_view, name='job_per_day'),
    
    # URL Halaman Login & Logout
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='login.html',
             redirect_authenticated_user=True
         ), 
         name='login'),
    
    path('logout/', 
         auth_views.LogoutView.as_view(
             next_page='core:login'
         ), 
         name='logout'),

    # URL MANAJEMEN PERSONIL
    path('personil/', views.manajemen_personil, name='manajemen_personil'),
    path('personil/delete/<int:personil_id>/', 
         views.delete_personil, 
         name='delete_personil'),

    # URL MANAJEMEN PROJECT
    path('projects/', views.manajemen_project, name='manajemen_project'),
    path('projects/delete/<int:project_id>/', 
         views.delete_project, 
         name='delete_project'),
         
    # ==========================================================
    # URL BARU UNTUK DETAIL PROJECT (TAMBAHKAN KEMBALI)
    # ==========================================================
    path('project/<int:project_id>/', 
         views.project_detail_view, 
         name='project_detail'),
    
    # ==========================================================
    # URL BARU UNTUK "TAMBAH JOB DARI PROJECT" (TAMBAHKAN)
    # ==========================================================
    path('project/<int:project_id>/add-job/', 
         views.job_form_view, 
         name='job_add_to_project'),

    # URL MANAJEMEN JOB
    path('job/add/', views.job_form_view, name='job_add'),
    path('job/edit/<int:job_id>/', views.job_form_view, name='job_edit'),
    path('job/delete/<int:job_id>/', views.job_delete, name='job_delete'),

    # URL MODAL POP-UP
    path('job-date/update/<int:job_date_id>/', 
         views.update_job_date_status, 
         name='update_job_date_status'),

    # URL AJAX
    path('ajax/load-children/', views.load_children, name='load_children'),
    path('ajax/load-personil/', views.load_personil_by_assigned_to, name='load_personil'),
    
    # URL EXPORT KE GOOGLE APPS SCRIPT
    path('api/export-jobs/', views.export_jobs_to_gas, name='export_jobs_to_gas'),
    
    # URL EXPORT PDF (BARU)
    path('export/daily-jobs-pdf/', views.export_daily_jobs_pdf, name='export_daily_jobs_pdf'),
    path('export/project-jobs-pdf/', views.export_project_jobs_pdf, name='export_project_jobs_pdf'),
    
    # URL EXPORT EXCEL (BARU)
    path('export/daily-jobs-excel/', views.export_daily_jobs_excel, name='export_daily_jobs_excel'),
    path('export/project-jobs-excel/', views.export_project_jobs_excel, name='export_project_jobs_excel'),
]