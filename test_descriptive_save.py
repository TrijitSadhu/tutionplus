#!/usr/bin/env python
"""Test script to run fetch_all_content for descriptive"""
import os
import sys
import django

sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.core.management import call_command

print("\n" + "="*80)
print("RUNNING: fetch_all_content for descriptive")
print("="*80 + "\n")

try:
    call_command('fetch_all_content', type='currentaffairs_descriptive', log_id=73, verbosity=2)
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

# Check what was saved
print("\n" + "="*80)
print("CHECKING DATABASE")
print("="*80 + "\n")

from bank.models import currentaffairs_descriptive
total = currentaffairs_descriptive.objects.count()
latest = currentaffairs_descriptive.objects.all().order_by('-id').first()

print(f"Total descriptive entries in DB: {total}")
if latest:
    print(f"\nLatest Entry:")
    print(f"  ID: {latest.id}")
    print(f"  Heading: {latest.upper_heading[:70]}")
    print(f"  Date: {latest.day}")
    print(f"  Defence: {latest.Defence}, National: {latest.National}")
