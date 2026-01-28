#!/usr/bin/env python
"""Test bulk import with all available tables"""
import os
import django
import json
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.bulk_import import BulkImporter
from genai.models import JsonImport

print("\n" + "="*80)
print("🧪 TESTING BULK IMPORTER WITH ALL TABLE TYPES")
print("="*80)

# Get test record ID 17 (physics)
try:
    test_record = JsonImport.objects.get(id=17)
    print(f"\n✅ Test Record Found: ID {test_record.id}")
    print(f"   Table: {test_record.to_table}")
    print(f"   JSON Data: {test_record.json_data[:100]}...")
except JsonImport.DoesNotExist:
    print(f"\n❌ Test record ID 17 not found!")
    exit(1)

# Test the importer directly
print(f"\n" + "-"*80)
print(f"Testing BulkImporter.get_model_class() for '{test_record.to_table}'")
print("-"*80)

try:
    importer = BulkImporter(
        table_name=test_record.to_table,
        json_data=test_record.json_data,
        form_date=date.today(),
        form_time=None
    )
    print(f"✅ BulkImporter created")
    
    model_class = importer.get_model_class()
    print(f"✅ Model class retrieved: {model_class}")
    print(f"   Model name: {model_class._meta.model_name}")
    print(f"   App label: {model_class._meta.app_label}")
    
except ValueError as e:
    print(f"❌ Error: {e}")
    exit(1)

# Now test the full import
print(f"\n" + "-"*80)
print(f"Testing full import_data()")
print("-"*80)

try:
    result = importer.import_data()
    print(f"\n✅ Import completed!")
    print(f"   Success: {result['success']}")
    print(f"   Created: {result['created']}")
    print(f"   Updated: {result['updated']}")
    print(f"   Errors: {len(result['errors'])}")
    
    if result['errors']:
        print(f"\n❌ Errors occurred:")
        for err in result['errors']:
            print(f"   - {err}")
    else:
        print(f"\n✅ NO ERRORS - Import successful!")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print(f"\n" + "="*80)
print(f"✅ TEST COMPLETE")
print(f"="*80)
