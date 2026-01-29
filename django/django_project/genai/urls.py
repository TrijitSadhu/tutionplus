"""
GenAI URL Configuration
"""

from django.urls import path, re_path
from . import views
from . import admin as admin_views

app_name = 'genai'

urlpatterns = [
    # Current Affairs endpoints
    path('api/current-affairs/mcq/', views.process_current_affairs_mcq, name='ca_mcq'),
    path('api/current-affairs/descriptive/', views.process_current_affairs_descriptive, name='ca_descriptive'),
    
    # Subject PDF processing
    path('api/pdf/process/', views.process_subject_pdf_view, name='process_pdf'),
    
    # Math processing
    path('api/math/process/', views.process_math_problem_view, name='process_math'),
    path('api/math/batch/', views.batch_process_math_view, name='batch_math'),
    
    # Status endpoint
    path('api/status/', views.genai_status, name='status'),
    
    # Admin Dashboard - Processing Management
    path('admin/dashboard/', views.processing_dashboard, name='processing_dashboard'),
    path('admin/trigger-fetch/', views.trigger_fetch, name='trigger_fetch'),
    path('admin/task-status/<int:task_id>/', views.task_status, name='task_status'),
    
    # PDF Processing Form (with chapter and difficulty selection)
    path('process-pdf-form/', admin_views.process_pdf_with_options, name='process_pdf_form'),
    
    # Math PDF Processing Form (GO button handler)
    path('admin/math-pdf-processing/<int:pk>/', views.math_pdf_processing_form, name='math_pdf_processing_form'),
]