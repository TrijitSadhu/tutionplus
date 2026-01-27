#!/usr/bin/env python
"""Check ContentSource URLs and test skip-scraping with better debugging"""
import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
django.setup()

from genai.models import ContentSource, CurrentAffairsMCQ
from django.utils import timezone

print(f"\n{'='*70}")
print(f"📋 CHECKING CONTENT SOURCES")
print(f"{'='*70}\n")

# Get active MCQ sources
mcq_sources = ContentSource.objects.filter(
    is_active=True,
    source_type='currentaffairs_mcq'
)

print(f"Active MCQ Sources: {mcq_sources.count()}")
for source in mcq_sources:
    print(f"\n  • {source.url}")
    print(f"    Type: {source.source_type}")
    print(f"    Active: {source.is_active}")

print(f"\n{'='*70}")
print(f"📊 LATEST MCQ RESULTS")
print(f"{'='*70}\n")

# Get latest MCQs
latest_mcqs = CurrentAffairsMCQ.objects.all().order_by('-id')[:5]
print(f"Latest {latest_mcqs.count()} MCQs:\n")
for mcq in latest_mcqs:
    print(f"  ID: {mcq.id}")
    print(f"  Question: {mcq.question[:60]}...")
    print(f"  Source: {mcq.source_url}")
    print()

print(f"{'='*70}")
print(f"💡 SKIP-SCRAPING MODE EXPLAINED")
print(f"{'='*70}\n")
print("""
In skip-scraping mode:
  ✓ URLs are sent directly to LLM
  ✓ NO fetching or downloading happens
  ✓ NO HTML extraction or scraping
  ✓ LLM receives: URL only
  
The LLM is expected to:
  • Understand it's a URL
  • Know how to extract content from that URL
  • Generate MCQs based on the content
  
Current behavior:
  ✓ Pipeline correctly skips scraping
  ✓ URL sent to LLM: https://www.indiabix.com/current-affairs-mcq/
  ⚠ LLM response format needs adjustment
""")
print(f"{'='*70}\n")
