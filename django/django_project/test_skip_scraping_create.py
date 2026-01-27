#!/usr/bin/env python
"""Test skip-scraping mode with MCQs from both sites"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
django.setup()

from genai.models import ProcessingLog
from django.utils import timezone

# Create ProcessingLog with skip_scraping=True
log = ProcessingLog.objects.create(
    task_type='currentaffairs_mcq_fetch',
    status='running',
    started_at=timezone.now(),
    skip_scraping=True,  # Enable skip-scraping mode
    is_scheduled=False
)

print(f"\n{'='*70}")
print(f"✅ Created ProcessingLog for Skip-Scraping Test")
print(f"{'='*70}")
print(f"  ID: {log.id}")
print(f"  Task Type: {log.task_type}")
print(f"  Skip Scraping: {log.skip_scraping}")
print(f"  Status: {log.status}")
print(f"{'='*70}\n")
print(f"Run this command to test:")
print(f"  python manage.py fetch_all_content --type=currentaffairs_mcq --log-id={log.id}")
print()
