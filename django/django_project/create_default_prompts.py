#!/usr/bin/env python
"""Create default LLM prompts in database"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from bank.models import LLMPrompt

# Create default MCQ prompt
mcq_prompt, created = LLMPrompt.objects.get_or_create(
    source_url='',
    prompt_type='mcq',
    defaults={
        'prompt_text': """You are an expert in creating multiple choice questions for competitive exams.
Based on the following current affairs article, generate 3 high-quality MCQ questions.

Title: {title}
Content: {content}

Return ONLY a JSON object with this structure:
{
    "questions": [
        {
            "question": "Question text",
            "option_a": "Option A",
            "option_b": "Option B", 
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_answer": "A",
            "explanation": "Why this answer is correct"
        }
    ]
}""",
        'is_default': True,
        'is_active': True
    }
)
print(f"MCQ prompt {'created' if created else 'already exists'}: {mcq_prompt.id}")

# Create default Descriptive prompt
desc_prompt, created = LLMPrompt.objects.get_or_create(
    source_url='',
    prompt_type='descriptive',
    defaults={
        'prompt_text': """You are an expert in summarizing current affairs for educational purposes.
Summarize the following article in a clear, structured way suitable for study notes.

Title: {title}
Content: {content}

Return ONLY a JSON object with this structure:
{
    "title": "Article Title",
    "summary": "Detailed summary",
    "key_points": ["Point 1", "Point 2", "Point 3"],
    "importance": "Why this is important for competitive exams"
}""",
        'is_default': True,
        'is_active': True
    }
)
print(f"Descriptive prompt {'created' if created else 'already exists'}: {desc_prompt.id}")

print("\nDefault prompts are now available in the database!")
print("You can view and modify them at: /admin/bank/llmprompt/")
