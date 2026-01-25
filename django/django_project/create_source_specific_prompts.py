#!/usr/bin/env python
"""
Example: How to create source-specific prompts for different news sources
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from bank.models import LLMPrompt

print("=" * 70)
print("Example: Creating Source-Specific Prompts")
print("=" * 70)

# Example 1: Create MCQ prompt for Times of India news
print("\n[Example 1] Creating MCQ prompt for Times of India...")
toi_mcq_prompt, created = LLMPrompt.objects.get_or_create(
    source_url='https://timesofindia.indiatimes.com/news',
    prompt_type='mcq',
    defaults={
        'prompt_text': """You are creating MCQs for Indian competitive exams based on Times of India articles.
Focus on current affairs and Indian politics from this article:

Title: {title}
Content: {content}

Create 3 challenging MCQ questions in JSON format with:
- Focus on Indian current affairs
- Banking/Finance relevant when possible
- Clear explanations

{
    "questions": [
        {
            "question": "...",
            "option_a": "...",
            "option_b": "...",
            "option_c": "...",
            "option_d": "...",
            "correct_answer": "A",
            "explanation": "..."
        }
    ]
}""",
        'is_default': False,  # This is specific to one source
        'is_active': True
    }
)
print(f"[{'CREATED' if created else 'EXISTS'}] MCQ prompt for Times of India")

# Example 2: Create Descriptive prompt for NDTV
print("\n[Example 2] Creating Descriptive prompt for NDTV...")
ndtv_desc_prompt, created = LLMPrompt.objects.get_or_create(
    source_url='https://www.ndtv.com/news',
    prompt_type='descriptive',
    defaults={
        'prompt_text': """Summarize this NDTV news article for bank exam study notes.
Create a concise summary with clear sections.

Title: {title}
Content: {content}

Format as JSON with:
- Clear title
- Concise 2-3 line summary
- 3-4 important points for exam preparation
- Why this matters for competitive exams

{
    "title": "...",
    "summary": "...",
    "key_points": ["point1", "point2", "point3"],
    "importance": "..."
}""",
        'is_default': False,
        'is_active': True
    }
)
print(f"[{'CREATED' if created else 'EXISTS'}] Descriptive prompt for NDTV")

# Example 3: Create MCQ prompt for BBC (International news)
print("\n[Example 3] Creating MCQ prompt for BBC News...")
bbc_mcq_prompt, created = LLMPrompt.objects.get_or_create(
    source_url='https://www.bbc.com/news',
    prompt_type='mcq',
    defaults={
        'prompt_text': """Create MCQ questions from BBC international news for competitive exams.
Focus on global affairs and their impact on India.

Title: {title}
Content: {content}

Generate 3 MCQs suitable for international relations section of exams.

{
    "questions": [
        {
            "question": "...",
            "option_a": "...",
            "option_b": "...",
            "option_c": "...",
            "option_d": "...",
            "correct_answer": "A",
            "explanation": "..."
        }
    ]
}""",
        'is_default': False,
        'is_active': True
    }
)
print(f"[{'CREATED' if created else 'EXISTS'}] MCQ prompt for BBC")

# Show all prompts
print("\n" + "=" * 70)
print("All Available Prompts:")
print("=" * 70)
all_prompts = LLMPrompt.objects.all().order_by('source_url', 'prompt_type')
for prompt in all_prompts:
    status = "[ACTIVE]" if prompt.is_active else "[INACTIVE]"
    default = "[DEFAULT]" if prompt.is_default else ""
    source = prompt.source_url if prompt.source_url else "(Global Default)"
    ptype = prompt.get_prompt_type_display()
    print(f"{status} {ptype:12} {source:40} {default}")

print("\n" + "=" * 70)
print("How the system will use these prompts:")
print("=" * 70)
print("""
When processing articles from:
1. Times of India   -> Uses ToI-specific MCQ prompt (if available)
2. NDTV            -> Uses NDTV-specific Descriptive prompt (if available)  
3. BBC             -> Uses BBC-specific MCQ prompt (if available)
4. Any other URL   -> Falls back to default prompt

Example processing flow:
- Article from 'https://timesofindia.indiatimes.com/news/politics'
  -> Matches source_url 'https://timesofindia.indiatimes.com/news'
  -> Uses Times of India MCQ prompt
  -> Falls back to default if that specific URL not found
  
This allows you to:
- Customize questions for each news source
- Have different styles for different outlets
- Use regional-specific prompts for Indian news
- Have standard prompts for international news
- Create specialized prompts for finance/banking news
""")

print("\nYou can manage these in admin panel: /admin/bank/llmprompt/")
