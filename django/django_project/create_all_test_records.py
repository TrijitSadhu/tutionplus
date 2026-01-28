#!/usr/bin/env python
"""Create comprehensive dummy test records for ALL tables"""
import os
import django
import json
from datetime import datetime, date, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import JsonImport
from django.contrib.auth.models import User

print("\n" + "="*100)
print("🧪 COMPREHENSIVE TEST DATA GENERATION FOR ALL 34 TABLES")
print("="*100)

# Get or create a test user
user, created = User.objects.get_or_create(
    username='test_importer_all',
    defaults={'first_name': 'Test', 'last_name': 'AllTables'}
)
print(f"\n👤 Using User: {user.username}")

# Comprehensive test data for ALL 34 tables
test_data = {
    # Subject MCQ Tables (10 tables)
    'polity': {
        'description': 'Polity MCQ Questions',
        'json': [
            {
                "question": "How many Articles are in the Indian Constitution?",
                "option_1": "390",
                "option_2": "395",
                "option_3": "400",
                "option_4": "405",
                "option_5": "",
                "ans": 2,
                "explanation": "The Indian Constitution has 395 Articles divided into 22 Parts.",
                "categories": ["National"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'history': {
        'description': 'History MCQ Questions',
        'json': [
            {
                "question": "In which year did the Indian Independence Act become effective?",
                "option_1": "1945",
                "option_2": "1946",
                "option_3": "1947",
                "option_4": "1948",
                "option_5": "",
                "ans": 3,
                "explanation": "August 15, 1947 is when India became independent from British rule.",
                "categories": ["National"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'geography': {
        'description': 'Geography MCQ Questions',
        'json': [
            {
                "question": "Which is the largest ocean in the world?",
                "option_1": "Atlantic Ocean",
                "option_2": "Indian Ocean",
                "option_3": "Pacific Ocean",
                "option_4": "Arctic Ocean",
                "option_5": "",
                "ans": 3,
                "explanation": "The Pacific Ocean is the largest and deepest ocean on Earth.",
                "categories": ["National"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'economics': {
        'description': 'Economics MCQ Questions',
        'json': [
            {
                "question": "What does GDP stand for?",
                "option_1": "General Domestic Product",
                "option_2": "Gross Domestic Product",
                "option_3": "Global Development Program",
                "option_4": "Government Development Plan",
                "option_5": "",
                "ans": 2,
                "explanation": "GDP stands for Gross Domestic Product, the total economic output of a country.",
                "categories": ["Business_Economy_Banking"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'physics': {
        'description': 'Physics MCQ Questions',
        'json': [
            {
                "question": "What is the speed of light in vacuum?",
                "option_1": "2 × 10^8 m/s",
                "option_2": "3 × 10^8 m/s",
                "option_3": "4 × 10^8 m/s",
                "option_4": "5 × 10^8 m/s",
                "option_5": "",
                "ans": 2,
                "explanation": "The speed of light (c) = 3 × 10^8 meters per second in vacuum.",
                "categories": ["Science_Techonlogy"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'chemistry': {
        'description': 'Chemistry MCQ Questions',
        'json': [
            {
                "question": "What is the atomic number of Carbon?",
                "option_1": "4",
                "option_2": "5",
                "option_3": "6",
                "option_4": "7",
                "option_5": "",
                "ans": 3,
                "explanation": "Carbon has atomic number 6, with 6 protons in its nucleus.",
                "categories": ["Science_Techonlogy"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'biology': {
        'description': 'Biology MCQ Questions',
        'json': [
            {
                "question": "What is the powerhouse of the cell?",
                "option_1": "Nucleus",
                "option_2": "Mitochondria",
                "option_3": "Ribosome",
                "option_4": "Chloroplast",
                "option_5": "",
                "ans": 2,
                "explanation": "Mitochondria is called the powerhouse of the cell as it produces ATP energy.",
                "categories": ["Science_Techonlogy"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'reasoning': {
        'description': 'Reasoning MCQ Questions',
        'json': [
            {
                "question": "If all men are mortal and Socrates is a man, then Socrates is mortal. This is an example of?",
                "option_1": "Inductive reasoning",
                "option_2": "Deductive reasoning",
                "option_3": "Abductive reasoning",
                "option_4": "Analogical reasoning",
                "option_5": "",
                "ans": 2,
                "explanation": "This is a classic example of deductive reasoning - general truth applied to specific case.",
                "categories": ["National"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'error': {
        'description': 'Error Finding MCQ Questions',
        'json': [
            {
                "question": "Find the error: 'He go to school everyday.'",
                "option_1": "He",
                "option_2": "go",
                "option_3": "to",
                "option_4": "everyday",
                "option_5": "",
                "ans": 2,
                "explanation": "Should be 'goes' not 'go' - subject-verb agreement error.",
                "categories": ["National"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'mcq': {
        'description': 'General MCQ Questions',
        'json': [
            {
                "question": "What is the capital of France?",
                "option_1": "London",
                "option_2": "Paris",
                "option_3": "Berlin",
                "option_4": "Madrid",
                "option_5": "",
                "ans": 2,
                "explanation": "Paris is the capital and largest city of France.",
                "categories": ["International"],
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    
    # Current Affairs Tables (3 tables)
    'currentaffairs_mcq': {
        'description': 'Current Affairs MCQ',
        'json': [
            {
                "question": "Which country hosted the G20 summit in 2025?",
                "option_1": "Japan",
                "option_2": "Brazil",
                "option_3": "India",
                "option_4": "USA",
                "option_5": "",
                "ans": 2,
                "explanation": "Brazil is hosting the G20 summit for 2025.",
                "categories": ["International"],
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
                "upper_heading": "Global Economic Trends 2026",
                "yellow_heading": "Market Performance Overview",
                "key_1": "Stock markets show mixed performance",
                "key_2": "Cryptocurrency market recovery continuing",
                "key_3": "Gold prices increase due to geopolitical tensions",
                "key_4": "Real estate market stabilizes",
                "all_key_points": "Economic outlook shows cautious optimism",
                "categories": ["Business_Economy_Banking"],
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
                "upper_heading": "Climate Action Report 2026",
                "yellow_heading": "Progress on Net-Zero Targets",
                "key_1": "150 countries meet renewable energy goals",
                "key_2": "Carbon emissions decline by 8% YoY",
                "key_3": "Green technology investments reach $2 trillion",
                "key_4": "New climate treaties signed by 180 nations",
                "creation_time": "10:00:00"
            }
        ]
    },
    
    # Other Tables (21 tables)
    'total': {
        'description': 'Total - General Purpose',
        'json': [
            {
                "name": "Test Record 1",
                "title": "General Test Data",
                "content": "This is a general purpose test record",
                "year_now": "2026",
                "month": "January",
                "creation_time": "10:00:00"
            }
        ]
    },
    'total_english': {
        'description': 'Total English',
        'json': [
            {
                "question": "Choose the correct spelling:",
                "option_1": "Occured",
                "option_2": "Occurred",
                "option_3": "Occured",
                "option_4": "Occoured",
                "option_5": "",
                "ans": 2,
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'total_math': {
        'description': 'Total Math',
        'json': [
            {
                "question": "What is 15 × 8?",
                "option_1": "100",
                "option_2": "110",
                "option_3": "120",
                "option_4": "130",
                "option_5": "",
                "ans": 3,
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'total_job': {
        'description': 'Total Job',
        'json': [
            {
                "job_title": "Software Engineer",
                "company": "Tech Corp",
                "salary": "10-15 LPA",
                "location": "Bangalore",
                "experience": "2-3 years",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'total_job_category': {
        'description': 'Total Job Category',
        'json': [
            {
                "category": "IT",
                "description": "Information Technology Jobs",
                "count": 1500,
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'total_job_state': {
        'description': 'Total Job State',
        'json': [
            {
                "state": "Karnataka",
                "jobs_available": 500,
                "avg_salary": "12 LPA",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'home': {
        'description': 'Home Page Content',
        'json': [
            {
                "title": "Welcome to Learning Platform",
                "content": "Start your learning journey today",
                "featured_courses": 5,
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'topic': {
        'description': 'Topic',
        'json': [
            {
                "topic_name": "Machine Learning",
                "description": "ML fundamentals and applications",
                "difficulty": "Intermediate",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'math': {
        'description': 'Math Questions',
        'json': [
            {
                "question": "What is the area of a circle with radius 5?",
                "option_1": "25π",
                "option_2": "50π",
                "option_3": "75π",
                "option_4": "100π",
                "option_5": "",
                "ans": 1,
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'job': {
        'description': 'Job Listings',
        'json': [
            {
                "position": "Data Scientist",
                "company": "Analytics Inc",
                "salary_min": 800000,
                "salary_max": 1500000,
                "location": "Mumbai",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'the_hindu_word_Header1': {
        'description': 'The Hindu Word Header 1',
        'json': [
            {
                "word": "Ubiquitous",
                "meaning": "Present everywhere",
                "example": "Mobile phones are ubiquitous in modern society",
                "part_of_speech": "Adjective",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'the_hindu_word_Header2': {
        'description': 'The Hindu Word Header 2',
        'json': [
            {
                "word": "Ephemeral",
                "meaning": "Lasting for a very short time",
                "example": "The beauty of flowers is ephemeral",
                "part_of_speech": "Adjective",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'the_hindu_word_list1': {
        'description': 'The Hindu Word List 1',
        'json': [
            {
                "word": "Ameliorate",
                "meaning": "To make better",
                "example": "Education can ameliorate poverty",
                "part_of_speech": "Verb",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'the_hindu_word_list2': {
        'description': 'The Hindu Word List 2',
        'json': [
            {
                "word": "Benevolent",
                "meaning": "Kind and generous",
                "example": "The benevolent organization helps the poor",
                "part_of_speech": "Adjective",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'the_economy_word_Header1': {
        'description': 'The Economy Word Header 1',
        'json': [
            {
                "word": "Inflation",
                "meaning": "General increase in prices",
                "example": "High inflation reduces purchasing power",
                "part_of_speech": "Noun",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'the_economy_word_Header2': {
        'description': 'The Economy Word Header 2',
        'json': [
            {
                "word": "Recession",
                "meaning": "Period of economic decline",
                "example": "The economy faces recession pressures",
                "part_of_speech": "Noun",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'the_economy_word_list1': {
        'description': 'The Economy Word List 1',
        'json': [
            {
                "word": "Deflation",
                "meaning": "Decrease in general price level",
                "example": "Deflation can increase unemployment",
                "part_of_speech": "Noun",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
    'the_economy_word_list2': {
        'description': 'The Economy Word List 2',
        'json': [
            {
                "word": "Equity",
                "meaning": "Ownership stake in a company",
                "example": "Investors buy equity in startups",
                "part_of_speech": "Noun",
                "year_now": "2026",
                "month": "January"
            }
        ]
    },
}

# Print all JSON data being used
print(f"\n{'='*100}")
print("📋 DUMMY JSON DATA FOR ALL TABLES")
print(f"{'='*100}\n")

for idx, (table_name, test_info) in enumerate(test_data.items(), 1):
    print(f"\n{idx:2d}. TABLE: {table_name:30s} | {test_info['description']}")
    print(f"    {'─'*90}")
    print(f"    JSON Data:")
    print(json.dumps(test_info['json'], indent=6))

# Create JsonImport records
print(f"\n{'='*100}")
print("📥 CREATING JSONIMPORT RECORDS")
print(f"{'='*100}\n")

created_records = []

for table_name, test_info in test_data.items():
    try:
        json_import = JsonImport.objects.create(
            to_table=table_name,
            json_data=json.dumps(test_info['json'], indent=2),
            created_by=user
        )
        
        created_records.append({
            'id': json_import.id,
            'table': table_name,
            'description': test_info['description'],
            'record_count': len(test_info['json'])
        })
        
        print(f"✅ [{json_import.id:3d}] {table_name:30s} | Items: {len(test_info['json'])} | {test_info['description']}")
        
    except Exception as e:
        print(f"❌ {table_name:30s} | ERROR: {str(e)}")

# Print summary
print(f"\n{'='*100}")
print(f"🎯 TEST RECORDS CREATED - SUMMARY")
print(f"{'='*100}\n")

print(f"Total Records Created: {len(created_records)}\n")

# Group by category
categories = {
    'Subject MCQ': [],
    'Current Affairs': [],
    'Other Tables': []
}

for record in created_records:
    if record['table'] in ['polity', 'history', 'geography', 'economics', 'physics', 'chemistry', 'biology', 'reasoning', 'error', 'mcq']:
        categories['Subject MCQ'].append(record)
    elif record['table'] in ['currentaffairs_mcq', 'currentaffairs_descriptive', 'current_affairs_slide']:
        categories['Current Affairs'].append(record)
    else:
        categories['Other Tables'].append(record)

for category, records in categories.items():
    print(f"\n📌 {category} ({len(records)} tables)")
    print(f"   {'─'*90}")
    for record in records:
        print(f"   ID: {record['id']:3d} | {record['table']:30s} | Items: {record['record_count']} | {record['description']}")

print(f"\n{'='*100}")
print(f"✅ ALL TEST DATA READY FOR TESTING")
print(f"{'='*100}\n")
