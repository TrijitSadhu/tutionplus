#!/usr/bin/env python
"""
Script to check existing prompts and create missing ones for all subjects
Run with: python manage.py shell < check_and_create_prompts.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import LLMPrompt
from bank.models import PDFUpload

# Get all unique subjects from PDFUpload
subjects = PDFUpload.objects.values_list('subject', flat=True).distinct()
subjects = sorted(list(set(subjects)))

print("\n" + "="*80)
print("CHECKING EXISTING PROMPTS")
print("="*80)

# Check existing prompts
existing_prompts = LLMPrompt.objects.all().values_list('source_url', 'prompt_type')
existing_prompts = list(existing_prompts)

print(f"\nTotal existing prompts: {len(existing_prompts)}\n")
for source_url, prompt_type in existing_prompts:
    print(f"  ✓ {source_url or 'DEFAULT'} ({prompt_type})")

print("\n" + "="*80)
print(f"SUBJECTS IN DATABASE: {subjects}")
print("="*80)

# Define prompts for each subject
PROMPTS = {
    'polity': {
        'mcq': """You are an expert Indian Politics and Constitution specialist. Generate high-quality multiple choice questions for competitive exams like UPSC.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} MCQ questions based on the content. The questions should test understanding and application of concepts in Indian Politics and Constitution.

Difficulty: {difficulty}

Return ONLY valid JSON (no markdown):
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Question text",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "correct_answer": 1,
            "explanation": "Detailed explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert Indian Politics and Constitution specialist. Generate high-quality descriptive answers for competitive exams.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} descriptive questions and comprehensive answers based on the content.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Descriptive question text",
            "answer": "Comprehensive answer with key points",
            "key_points": ["point1", "point2", "point3"],
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'economics': {
        'mcq': """You are an expert Economics specialist. Generate high-quality multiple choice questions for competitive exams.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} MCQ questions based on economic concepts. Questions should test understanding of micro/macro economics, policies, and theories.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Question text",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "correct_answer": 1,
            "explanation": "Detailed explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert Economics specialist. Generate descriptive questions and answers.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} descriptive economics questions with comprehensive answers.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Descriptive question text",
            "answer": "Comprehensive answer with examples",
            "key_points": ["point1", "point2", "point3"],
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'history': {
        'mcq': """You are an expert History specialist. Generate high-quality multiple choice questions for competitive exams.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} MCQ questions based on historical events, dates, figures, and facts.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Question text",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "correct_answer": 1,
            "explanation": "Detailed explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert History specialist. Generate descriptive questions and answers.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} descriptive history questions with comprehensive answers.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Descriptive question text",
            "answer": "Comprehensive historical answer",
            "key_points": ["point1", "point2", "point3"],
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'geography': {
        'mcq': """You are an expert Geography specialist. Generate high-quality multiple choice questions for competitive exams.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} MCQ questions based on geography concepts, locations, and facts.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Question text",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "correct_answer": 1,
            "explanation": "Detailed explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert Geography specialist. Generate descriptive questions and answers.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} descriptive geography questions with comprehensive answers.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Descriptive question text",
            "answer": "Comprehensive geographical answer",
            "key_points": ["point1", "point2", "point3"],
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'other': {
        'mcq': """You are an expert content creator. Generate high-quality multiple choice questions.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} MCQ questions based on the content provided.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Question text",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "correct_answer": 1,
            "explanation": "Detailed explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert content creator. Generate descriptive questions and answers.

Chapter: {chapter}
Topic: {topic}
Content: {content}

Generate {num_questions} descriptive questions with comprehensive answers.

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "chapter": "{chapter}",
    "topic": "{topic}",
    "questions": [
        {{
            "question": "Descriptive question text",
            "answer": "Comprehensive answer",
            "key_points": ["point1", "point2", "point3"],
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    }
}

print("\n" + "="*80)
print("CREATING MISSING PROMPTS")
print("="*80 + "\n")

created_count = 0
skipped_count = 0

for subject in subjects:
    for prompt_type in ['mcq', 'descriptive']:
        source_url = f'pdf_to_{prompt_type}_{subject}'
        
        # Check if prompt exists
        exists = LLMPrompt.objects.filter(
            source_url=source_url,
            prompt_type=prompt_type
        ).exists()
        
        if exists:
            print(f"  ✓ SKIP: {source_url} (already exists)")
            skipped_count += 1
        else:
            # Get prompt text from PROMPTS dict
            prompt_text = PROMPTS.get(subject, PROMPTS['other']).get(prompt_type, "")
            
            # Create the prompt
            prompt = LLMPrompt.objects.create(
                source_url=source_url,
                prompt_type=prompt_type,
                prompt_text=prompt_text,
                is_default=False,
                is_active=True
            )
            print(f"  ✓ CREATED: {source_url}")
            created_count += 1

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Created: {created_count} prompts")
print(f"Skipped: {skipped_count} prompts (already exist)")
print(f"Total: {created_count + skipped_count} prompts")

print("\n" + "="*80)
print("ALL PROMPTS IN DATABASE")
print("="*80 + "\n")

all_prompts = LLMPrompt.objects.all().values_list('source_url', 'prompt_type', 'is_active')
for source_url, prompt_type, is_active in all_prompts:
    status = "✓ Active" if is_active else "✗ Inactive"
    print(f"  {status} | {source_url or 'DEFAULT'} ({prompt_type})")

print("\n" + "="*80)
