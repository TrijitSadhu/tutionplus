#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection
from genai.models import LLMPrompt

# Check if table exists
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='genai_llmprompt';
    """)
    table_exists = cursor.fetchone()

if table_exists:
    print("✓ Table 'genai_llmprompt' exists in database")
else:
    print("✗ Table 'genai_llmprompt' does NOT exist")
    print("Running migrations...")
    from django.core.management import call_command
    call_command('migrate', 'genai')
    print("✓ Migrations completed")

# Check for records
count = LLMPrompt.objects.count()
print(f"\n✓ Total LLMPrompt records: {count}")

if count == 0:
    print("\n→ No prompts found. Creating sample prompts...")
    
    # Create default MCQ prompt
    LLMPrompt.objects.create(
        source_url='',  # Empty for default
        prompt_type='mcq',
        prompt_text="""You are an expert in creating multiple choice questions for competitive exams.
Based on the following current affairs article, generate 3 high-quality MCQ questions.

Title: {title}
Content: {content}

Return ONLY a JSON object with this structure:
{"questions": [{"question": "Question text", "option_a": "Option A", "option_b": "Option B", "option_c": "Option C", "option_d": "Option D", "correct_answer": "A", "explanation": "Why this answer is correct"}]}""",
        is_default=True,
        is_active=True,
        created_by=None
    )
    print("✓ Created default MCQ prompt")
    
    # Create default descriptive prompt
    LLMPrompt.objects.create(
        source_url='',  # Empty for default
        prompt_type='descriptive',
        prompt_text="""You are an expert in summarizing current affairs for educational purposes.
Summarize the following article in a clear, structured way suitable for study notes.

Title: {title}
Content: {content}

Return ONLY a JSON object with this structure:
{"title": "Article Title", "summary": "Detailed summary", "key_points": ["Point 1", "Point 2", "Point 3"], "importance": "Why this is important for competitive exams"}""",
        is_default=True,
        is_active=True,
        created_by=None
    )
    print("✓ Created default descriptive prompt")
    
    print("\n✓ Sample prompts created successfully!")

# List all prompts
print("\n" + "="*60)
print("All LLMPrompt records:")
print("="*60)
for prompt in LLMPrompt.objects.all():
    source = prompt.source_url if prompt.source_url else "(Default)"
    print(f"\nID: {prompt.id}")
    print(f"Type: {prompt.prompt_type}")
    print(f"Source: {source}")
    print(f"Is Default: {prompt.is_default}")
    print(f"Is Active: {prompt.is_active}")
    print(f"Preview: {prompt.prompt_text[:80]}...")
