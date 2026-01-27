#!/usr/bin/env python
"""
Script to create default LLMPrompt records for Current Affairs MCQ and Descriptive processing
Run this after migrations: python manage.py shell < create_ca_llm_prompts.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.contrib.auth.models import User
from genai.models import LLMPrompt

print("\n" + "="*80)
print("Creating Current Affairs LLM Prompts")
print("="*80)

# Get admin user or create if needed
try:
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print(f"✓ Created admin user: {admin_user.username}\n")
    else:
        print(f"✓ Using existing admin user: {admin_user.username}\n")
except Exception as e:
    print(f"✗ Error getting admin user: {e}")
    admin_user = None

# ==================== CURRENT AFFAIRS MCQ PROMPT ====================
ca_mcq_prompt_text = """You are an expert Current Affairs analyst and MCQ creator. Analyze the provided content and create high-quality multiple-choice questions (MCQs) suitable for competitive exams.

CONTENT TO ANALYZE:
{title}

{content}

REQUIREMENTS:
1. Generate exactly {num_questions} MCQs from the content
2. Each question should test understanding of key facts and concepts
3. Options should be plausible but clearly have one correct answer
4. Include relevant categories from: Science and Technology, National, International, Business, Sports, Environment, Defence, Politics, Law and Justice, Health, Economy, Agriculture, Culture, Social, Scheme, Report, Awards, Person

RESPONSE FORMAT (Valid JSON only):
{{
    "questions": [
        {{
            "question": "Question text here?",
            "option_1": "Option A text",
            "option_2": "Option B text",
            "option_3": "Option C text",
            "option_4": "Option D text",
            "correct_answer": "1",
            "explanation": "Why this is the correct answer...",
            "categories": ["National", "Politics"]
        }}
    ]
}}

IMPORTANT:
- Return ONLY valid JSON, no markdown or extra text
- correct_answer: Use numeric values (1, 2, 3, or 4)
- categories: Array of applicable categories
- explanation: 1-2 sentence explanation of the correct answer
"""

ca_mcq_prompt, created = LLMPrompt.objects.get_or_create(
    source_url='pdf_to_currentaffairs_mcq',
    prompt_type='mcq',
    defaults={
        'prompt_text': ca_mcq_prompt_text,
        'is_default': True,
        'is_active': True,
        'created_by': admin_user
    }
)

if created:
    print("✓ Created CA MCQ Prompt")
    print(f"  - source_url: {ca_mcq_prompt.source_url}")
    print(f"  - prompt_type: {ca_mcq_prompt.prompt_type}")
    print(f"  - is_default: {ca_mcq_prompt.is_default}")
    print(f"  - length: {len(ca_mcq_prompt_text)} characters\n")
else:
    print("⚠ CA MCQ Prompt already exists, skipping...")
    print(f"  - ID: {ca_mcq_prompt.id}\n")

# ==================== CURRENT AFFAIRS DESCRIPTIVE PROMPT ====================
ca_desc_prompt_text = """You are an expert Current Affairs analyst and content creator. Analyze the provided content and create a comprehensive descriptive piece suitable for competitive exam answer writing.

CONTENT TO ANALYZE:
{title}

{content}

REQUIREMENTS:
1. Provide detailed analysis and explanation of the current affairs topic
2. Cover key aspects, implications, and contextual information
3. Include relevant categories from: Science and Technology, National, International, Business, Sports, Environment, Defence, Politics, Law and Justice, Health, Economy, Agriculture, Culture, Social, Scheme, Report, Awards, Person
4. Structure with clear headings and key points

RESPONSE FORMAT (Valid JSON only):
{{
    "upper_heading": "Main topic title",
    "yellow_heading": "Sub-topic or focus area",
    "key_1": "First key point heading",
    "key_2": "Second key point heading",
    "key_3": "Third key point heading",
    "key_4": "Fourth key point heading",
    "all_key_points": "Point 1: Detailed explanation///Point 2: Detailed explanation///Point 3: Detailed explanation///Point 4: Detailed explanation",
    "categories": ["National", "Politics", "Law and Justice"]
}}

IMPORTANT:
- Return ONLY valid JSON, no markdown or extra text
- all_key_points: Use /// to separate different points
- categories: Array of applicable categories
- Keep explanations concise but comprehensive
- Ensure content is factually accurate
"""

ca_desc_prompt, created = LLMPrompt.objects.get_or_create(
    source_url='pdf_to_currentaffairs_descriptive',
    prompt_type='descriptive',
    defaults={
        'prompt_text': ca_desc_prompt_text,
        'is_default': True,
        'is_active': True,
        'created_by': admin_user
    }
)

if created:
    print("✓ Created CA Descriptive Prompt")
    print(f"  - source_url: {ca_desc_prompt.source_url}")
    print(f"  - prompt_type: {ca_desc_prompt.prompt_type}")
    print(f"  - is_default: {ca_desc_prompt.is_default}")
    print(f"  - length: {len(ca_desc_prompt_text)} characters\n")
else:
    print("⚠ CA Descriptive Prompt already exists, skipping...")
    print(f"  - ID: {ca_desc_prompt.id}\n")

print("="*80)
print("Current Affairs LLM Prompts Setup Complete!")
print("="*80 + "\n")

# Show summary
print("Summary:")
print("-" * 80)
mcq_count = LLMPrompt.objects.filter(prompt_type='mcq').count()
desc_count = LLMPrompt.objects.filter(prompt_type='descriptive').count()
print(f"Total MCQ Prompts: {mcq_count}")
print(f"Total Descriptive Prompts: {desc_count}")
print(f"Total LLM Prompts: {LLMPrompt.objects.count()}")
print("-" * 80 + "\n")
