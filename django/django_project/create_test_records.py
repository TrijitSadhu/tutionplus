#!/usr/bin/env python
"""Create dummy JsonImport records for testing bulk import"""
import os
import django
import json
from datetime import datetime, date, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import JsonImport
from django.contrib.auth.models import User

print("\n" + "="*80)
print("🧪 CREATING DUMMY TEST RECORDS FOR BULK IMPORT")
print("="*80)

# Get or create a test user
user, created = User.objects.get_or_create(
    username='test_importer',
    defaults={'first_name': 'Test', 'last_name': 'User'}
)
print(f"\n👤 User: {user.username} (Created: {created})")

# Define test data for each table type
test_data = {
    'currentaffairs_mcq': {
        'description': 'Current Affairs MCQ',
        'json': [
            {
                "question": "Which country has the highest GDP in 2025?",
                "option_1": "United States",
                "option_2": "China",
                "option_3": "Japan",
                "option_4": "Germany",
                "option_5": "",
                "ans": 1,
                "correct_answer": "A",
                "explanation": "The USA has the largest GDP globally. It remains the world's largest economy with a GDP of over 27 trillion USD.",
                "categories": ["International", "Business_Economy_Banking"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            },
            {
                "question": "What is the capital of India?",
                "option_1": "Mumbai",
                "option_2": "Delhi",
                "option_3": "Bangalore",
                "option_4": "Kolkata",
                "option_5": "",
                "ans": 2,
                "correct_answer": "B",
                "explanation": "New Delhi is the capital of India. It serves as the seat of the national government.",
                "categories": ["National"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'currentaffairs_descriptive': {
        'description': 'Current Affairs Descriptive',
        'json': [
            {
                "upper_heading": "Global Climate Summit 2026",
                "yellow_heading": "Key Outcomes and Decisions",
                "key_1": "195 countries committed to net-zero emissions by 2050",
                "key_2": "New climate finance fund established with $100 billion",
                "key_3": "Enhanced carbon trading mechanisms agreed upon",
                "key_4": "Renewable energy targets increased by 50%",
                "all_key_points": "Major environmental agreement reached; Climate action accelerated",
                "categories": ["Environment", "International"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'current_affairs_slide': {
        'description': 'Current Affairs Slide',
        'json': [
            {
                "upper_heading": "Space Exploration Milestone",
                "yellow_heading": "First Manned Mars Mission Launched",
                "key_1": "12 astronauts selected for the mission",
                "key_2": "Expected landing: December 2026",
                "key_3": "6-month mission duration planned",
                "key_4": "International collaboration with 15 countries",
                "creation_time": "10:00:00"
            }
        ]
    },
    'total': {
        'description': 'Total - Generic Table',
        'json': [
            {
                "name": "Test Record 1",
                "title": "Sample Data",
                "content": "This is a test record for the total table",
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'topic': {
        'description': 'Topic Table',
        'json': [
            {
                "topic_name": "Artificial Intelligence",
                "description": "AI and Machine Learning",
                "content": "Overview of AI developments",
                "year_now": "2026",
                "month": "January"
            }
        ]
    }
}

# Create JsonImport records for each table
created_records = []

for table_name, test_info in test_data.items():
    print(f"\n{'='*80}")
    print(f"📝 Creating test record for: {test_info['description']}")
    print(f"   Table: {table_name}")
    print(f"{'='*80}")
    
    try:
        # Create JSON import record
        json_import = JsonImport.objects.create(
            to_table=table_name,
            json_data=json.dumps(test_info['json'], indent=2),
            created_by=user
        )
        
        print(f"   ✅ Created JsonImport record:")
        print(f"      ID: {json_import.id}")
        print(f"      Table: {json_import.to_table}")
        print(f"      JSON Size: {len(json_import.json_data)} chars")
        print(f"      Records in JSON: {len(test_info['json'])}")
        print(f"      Created At: {json_import.created_at}")
        
        created_records.append({
            'id': json_import.id,
            'table': table_name,
            'description': test_info['description'],
            'record_count': len(test_info['json'])
        })
        
        print(f"   ✅ SUCCESS")
        
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")

# Print summary
print(f"\n{'='*80}")
print(f"🎯 TEST RECORDS CREATED SUMMARY")
print(f"{'='*80}")
print(f"\nTotal records created: {len(created_records)}\n")

for idx, record in enumerate(created_records, 1):
    print(f"{idx}. ID: {record['id']:3d} | Table: {record['table']:30s} | Items: {record['record_count']} | {record['description']}")

print(f"\n{'='*80}")
print(f"✅ TEST DATA CREATION COMPLETE")
print(f"{'='*80}")
print(f"""
📋 NEXT STEPS - TEST ONE BY ONE:

1. Open Django Admin: http://localhost:8000/admin/genai/jsonimport/

2. For each record created above:
   a. Select the record
   b. Choose action: "📥 Bulk Import (Select records & proceed)"
   c. Click "Go"
   d. The date should auto-fill with today's date
   e. Click "Proceed with Import"
   f. Watch:
      - Django terminal for logging
      - Browser console for JavaScript logging (F12)
   g. Check if success message appears
   h. Verify data in the respective admin table

3. Testing order (easiest to hardest):
   - Test currentaffairs_mcq first (simple model)
   - Test currentaffairs_descriptive
   - Test current_affairs_slide
   - Test total (generic model)
   - Test topic

4. Report findings for each test:
   ✅ Success / ❌ Failed
   Details of any errors

""")
