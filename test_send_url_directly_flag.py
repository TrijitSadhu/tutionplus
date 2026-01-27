#!/usr/bin/env python
"""Test that send_url_directly flag is properly passed"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import ProcessingLog
from django.utils import timezone

# Create a test ProcessingLog entry with send_url_directly=True
print("\n" + "="*70)
print("TEST: Verify send_url_directly flag is passed to function")
print("="*70)

test_log = ProcessingLog.objects.create(
    task_type='currentaffairs_mcq_fetch',
    status='pending',
    skip_scraping=False,
    send_url_directly=True,  # ← This should be passed to the function
    is_scheduled=False
)

print(f"\n✅ Created ProcessingLog entry:")
print(f"   ID: {test_log.id}")
print(f"   skip_scraping: {test_log.skip_scraping}")
print(f"   send_url_directly: {test_log.send_url_directly}")

print(f"\nNow run this command to test:")
print(f"   python manage.py fetch_all_content --type=currentaffairs_mcq --log-id={test_log.id}")

print(f"\nYou should see in the output:")
print(f"   ✓ 'Send URL Directly: True' in the fetch_and_process_current_affairs() call")
print(f"   ✓ '🔗 URL-ONLY MODE' in the processing output")

print("\n" + "="*70)
