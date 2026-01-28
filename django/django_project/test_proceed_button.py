#!/usr/bin/env python
"""Test the Proceed button form submission"""
import os
import django
import json
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.test import Client
from genai.models import JsonImport

print("\n" + "="*80)
print("🧪 TESTING PROCEED BUTTON FORM SUBMISSION")
print("="*80)

# Get test record ID 13 (polity)
try:
    test_record = JsonImport.objects.get(id=13)
    print(f"\n✅ Found test record ID 13: {test_record.to_table}")
except JsonImport.DoesNotExist:
    print(f"\n❌ Test record ID 13 not found!")
    print("Available records:")
    for rec in JsonImport.objects.all()[:5]:
        print(f"  - ID {rec.id}: {rec.to_table}")
    exit(1)

# Create a test client
client = Client()

print("\n" + "-"*80)
print("📋 STEP 1: GET the bulk import form")
print("-"*80)

# First, we need to visit the changelist and perform the initial action
changelist_url = '/admin/genai/jsonimport/'

# Simulate selecting record and clicking "Go" to show the form
response = client.post(
    changelist_url,
    {
        'action': 'bulk_import_action',
        'select_across': '0',
        'index': '0',
        '_selected_action': '13',
    },
    follow=False
)

print(f"Status Code: {response.status_code}")
print(f"Content Length: {len(response.content)} bytes")

if response.status_code == 200:
    print("✅ Form page received")
    # Check if the form is in the response
    if 'bulk-import-form' in response.content.decode():
        print("✅ bulk-import-form found in response")
    else:
        print("❌ bulk-import-form NOT found in response")
else:
    print(f"❌ Unexpected status code: {response.status_code}")
    print(f"Content: {response.content[:500]}")

print("\n" + "-"*80)
print("📋 STEP 2: POST the form with import_date (Proceed button)")
print("-"*80)

# Now submit the form with import_date
response = client.post(
    changelist_url,
    {
        'action': 'bulk_import_action',
        'select_across': '0',
        'index': '0',
        '_selected_action': '13',
        'import_date': str(date.today()),  # Add the import_date!
    },
    follow=False
)

print(f"\nStatus Code: {response.status_code}")
print(f"Content Length: {len(response.content)} bytes")

if response.status_code == 302:
    print("✅ Got redirect (302) - form was processed!")
    print(f"Redirect Location: {response.get('Location', 'N/A')}")
elif response.status_code == 200:
    print("⚠️  Got 200 - form might not have been processed")
    if 'bulk-import-form' in response.content.decode():
        print("   Form is still showing - might be re-rendered")
    if 'success' in response.content.decode().lower():
        print("   Success message found!")
    if 'error' in response.content.decode().lower():
        print("   Error message found!")
else:
    print(f"❌ Unexpected status code: {response.status_code}")

print("\n" + "="*80)
print("✅ TEST COMPLETE")
print("="*80)
print("\nNow try in browser:")
print("1. Go to http://localhost:8000/admin/genai/jsonimport/")
print("2. Select record ID 13")
print("3. Action: Bulk Import → Go")
print("4. Open Browser Console (F12)")
print("5. Click 'Proceed with Import'")
print("6. Watch for logs and check if import succeeds")
print("="*80 + "\n")
