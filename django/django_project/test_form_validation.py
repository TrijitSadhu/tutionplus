#!/usr/bin/env python
"""Test BulkImportForm validation"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.admin import BulkImportForm
from datetime import date

print("\n" + "="*80)
print("🧪 TESTING BulkImportForm VALIDATION")
print("="*80)

# Test 1: Empty form
print("\n[TEST 1] Empty form (no data)")
form1 = BulkImportForm()
print(f"  is_bound: {form1.is_bound}")
print(f"  is_valid: {form1.is_valid()}")

# Test 2: Form with valid date string
print("\n[TEST 2] Form with valid date string '2026-01-28'")
form2 = BulkImportForm({'import_date': '2026-01-28'})
print(f"  is_bound: {form2.is_bound}")
print(f"  is_valid: {form2.is_valid()}")
if form2.is_valid():
    print(f"  cleaned_data: {form2.cleaned_data}")
else:
    print(f"  errors: {form2.errors}")

# Test 3: Form with empty date
print("\n[TEST 3] Form with empty date ''")
form3 = BulkImportForm({'import_date': ''})
print(f"  is_bound: {form3.is_bound}")
print(f"  is_valid: {form3.is_valid()}")
if not form3.is_valid():
    print(f"  errors: {form3.errors}")

# Test 4: Form with today's date
print("\n[TEST 4] Form with today's date")
today = date.today().isoformat()
form4 = BulkImportForm({'import_date': today})
print(f"  Date string: {today}")
print(f"  is_bound: {form4.is_bound}")
print(f"  is_valid: {form4.is_valid()}")
if form4.is_valid():
    print(f"  cleaned_data: {form4.cleaned_data}")
else:
    print(f"  errors: {form4.errors}")

print("\n" + "="*80)
print("✅ FORM VALIDATION TEST COMPLETE")
print("="*80 + "\n")
