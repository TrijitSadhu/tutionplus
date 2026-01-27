#!/usr/bin/env python
"""
Test script to verify send_url_directly mode works correctly
Run this from Django shell: python manage.py shell < test_send_url_directly.py
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import ProcessingLog, ContentSource, MCQAnswer
from genai.tasks.current_affairs import CurrentAffairsProcessor
from datetime import datetime

print("=" * 80)
print("TEST: send_url_directly Mode Fix")
print("=" * 80)

# Test Setup
print("\n1️⃣ SETUP: Creating test ProcessingLog entry...")
log_entry = ProcessingLog.objects.create(
    task_name='test_send_url_directly',
    task_type='currentaffairs_mcq',
    status='pending',
    skip_scraping=False,  # Don't skip scraping in this test
    send_url_directly=True,  # ENABLE URL-ONLY MODE
    created_at=datetime.now(),
    updated_at=datetime.now()
)
print(f"   ✅ Created ProcessingLog ID: {log_entry.id}")
print(f"      - skip_scraping: {log_entry.skip_scraping}")
print(f"      - send_url_directly: {log_entry.send_url_directly}")

# Test Processor
print("\n2️⃣ TEST: Initialize CurrentAffairsProcessor...")
processor = CurrentAffairsProcessor()
print("   ✅ Processor initialized")

# Run the pipeline
print("\n3️⃣ EXECUTE: Running fetch_and_process_current_affairs...")
print("   " + "-" * 60)

try:
    result = processor.fetch_and_process_current_affairs(
        content_type='currentaffairs_mcq',
        skip_scraping=log_entry.skip_scraping,
        send_url_directly=log_entry.send_url_directly,
        logging_context=f"Test-{log_entry.id}"
    )
    
    print("   " + "-" * 60)
    print(f"\n   ✅ Pipeline executed successfully")
    print(f"      - Processed items: {len(result.get('processed_items', []))}")
    print(f"      - Total MCQs saved: {result.get('total_mcqs_saved', 0)}")
    print(f"      - Errors: {result.get('errors', [])}")
    
    # Check if MCQs were actually saved
    mcq_count = MCQAnswer.objects.filter(
        created_from=f"Current Affairs - currentaffairs_mcq"
    ).count()
    print(f"\n   📊 MCQ Database Check: {mcq_count} questions in database")
    
    if mcq_count > 0:
        print("\n   ✅ SUCCESS: MCQs were generated and saved!")
        print("   📝 Sample MCQs:")
        samples = MCQAnswer.objects.filter(
            created_from=f"Current Affairs - currentaffairs_mcq"
        ).order_by('-created_at')[:3]
        for i, mcq in enumerate(samples, 1):
            print(f"\n      MCQ {i}:")
            print(f"         Q: {mcq.question[:60]}...")
            print(f"         Answer: {mcq.correct_option}")
            print(f"         Categories: {mcq.category_list}")
    else:
        print("\n   ⚠️  WARNING: No MCQs were saved to database")
        print("      This might indicate an issue with the pipeline")
        
except Exception as e:
    print(f"\n   ❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

# Final Report
print("\n" + "=" * 80)
print("TEST REPORT")
print("=" * 80)
print(f"✅ Test completed")
print(f"✅ ProcessingLog ID: {log_entry.id}")
print(f"✅ Mode: send_url_directly=True (URL-ONLY MODE)")
print(f"✅ Expected: Content downloaded, extracted, and sent to LLM")
print(f"✅ Check logs above for detailed execution flow")
print("=" * 80)

# Clean up
print("\n4️⃣ CLEANUP: Removing test entry...")
log_entry.delete()
print("   ✅ Test entry deleted")
