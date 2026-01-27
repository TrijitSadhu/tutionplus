"""
Setup script to add subject-specific LLM prompts to database
Run: python manage.py shell < setup_subject_prompts.py
"""

from genai.models import LLMPrompt

# Define subjects
subjects = [
    ('polity', 'Polity'),
    ('economics', 'Economics'),
    ('math', 'Mathematics'),
    ('physics', 'Physics'),
    ('chemistry', 'Chemistry'),
    ('history', 'History'),
    ('geography', 'Geography'),
    ('biology', 'Biology'),
]

print("\n" + "="*60)
print("  ADDING SUBJECT-SPECIFIC LLM PROMPTS")
print("="*60 + "\n")

count = 0

for slug, name in subjects:
    # Create MCQ prompt
    mcq_prompt, created = LLMPrompt.objects.get_or_create(
        source_url=f'pdf_{slug}_mcq',
        prompt_type='mcq',
        defaults={
            'prompt_text': f"""You are an expert {name} teacher. Create 5 multiple choice questions based on the provided content from the PDF.

IMPORTANT INSTRUCTIONS:
- Generate ONLY from the provided content
- Do NOT add external information or knowledge
- Each question must have 4 options (A, B, C, D)
- Clearly indicate the correct answer

Format output as JSON:
[
    {{"question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "correct": "A"}},
    {{"question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "correct": "B"}},
    ...
]""",
            'is_active': True,
            'is_default': False
        }
    )
    if created:
        print(f"✓ Created MCQ prompt for {name} ({slug})")
        count += 1
    else:
        print(f"  MCQ prompt for {name} already exists")
    
    # Create Descriptive prompt
    desc_prompt, created = LLMPrompt.objects.get_or_create(
        source_url=f'pdf_{slug}_descriptive',
        prompt_type='descriptive',
        defaults={
            'prompt_text': f"""You are an expert {name} teacher. Create 3 detailed descriptive answers based on the provided content from the PDF.

IMPORTANT INSTRUCTIONS:
- Generate ONLY from the provided content
- Do NOT add external information or knowledge
- Each answer should be 150-250 words
- Be clear and well-structured

Format as Markdown with clear headings:

## Question 1: [Question text]
Answer: [Detailed explanation]

## Question 2: [Question text]
Answer: [Detailed explanation]

## Question 3: [Question text]
Answer: [Detailed explanation]""",
            'is_active': True,
            'is_default': False
        }
    )
    if created:
        print(f"✓ Created Descriptive prompt for {name} ({slug})")
        count += 1
    else:
        print(f"  Descriptive prompt for {name} already exists")

print(f"\n{'='*60}")
print(f"  TOTAL PROMPTS CREATED/UPDATED: {count}")
print(f"{'='*60}\n")

# Verify all prompts
total = LLMPrompt.objects.filter(source_url__startswith='pdf_').count()
print(f"Total subject-specific prompts in database: {total}")
print("\nSubject-specific prompts summary:")
for slug, name in subjects:
    mcq_count = LLMPrompt.objects.filter(source_url=f'pdf_{slug}_mcq').count()
    desc_count = LLMPrompt.objects.filter(source_url=f'pdf_{slug}_descriptive').count()
    print(f"  {name:15} → MCQ: {'✓' if mcq_count else '✗'}, Descriptive: {'✓' if desc_count else '✗'}")

print("\n" + "="*60)
print("  SETUP COMPLETE!")
print("="*60 + "\n")
