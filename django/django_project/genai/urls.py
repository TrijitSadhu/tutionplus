"""
GenAI URL Configuration
"""

from django.urls import path, re_path
from . import views

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
]
