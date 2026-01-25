#!/usr/bin/env python
"""Test script to verify ContentSource content_date field and MCQ date extraction"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import ContentSource
from bank.models import currentaffairs_mcq
from datetime import date

# Check existing ContentSource
print("\n" + "="*80)
print("🔍 TESTING ContentSource with content_date field")
print("="*80)

try:
    # Get the gktoday source
    source = ContentSource.objects.filter(url__icontains='gktoday.in').first()
    
    if source:
        print(f"\n✓ Found ContentSource: {source.name}")
        print(f"  URL: {source.url}")
        
        if hasattr(source, 'content_date'):
            print(f"  📅 Content Date: {source.content_date}")
            print(f"     Year: {source.content_date.year}")
            print(f"     Month: {source.content_date.month}")
            print(f"     Day: {source.content_date.day}")
        else:
            print(f"  ⚠️  content_date field not available")
    else:
        print("\n❌ No ContentSource found with gktoday.in URL")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

# Check if MCQs have the date fields
print(f"\n" + "="*80)
print("📊 CHECKING MCQ Records")
print("="*80)

mcqs = currentaffairs_mcq.objects.all().order_by('-id')[:3]

for mcq in mcqs:
    print(f"\n📌 MCQ ID: {mcq.id}")
    print(f"   Question: {mcq.question[:60]}...")
    print(f"   Year: {mcq.year_now}")
    print(f"   Month: {mcq.month}")
    print(f"   Day: {mcq.day if isinstance(mcq.day, int) else mcq.day.strftime('%Y-%m-%d')}")

print("\n" + "="*80)
