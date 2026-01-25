import sys
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

import django
django.setup()

from genai.models import LLMPrompt

# Update the existing MCQ prompt for gktoday to include bullet format request
prompt = LLMPrompt.objects.filter(
    prompt_type='mcq', 
    source_url='https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/'
).first()

if prompt:
    new_prompt_text = """You are an expert in creating multiple choice questions for competitive exams.
Based on the following current affairs article, generate 4 high-quality MCQ questions that test understanding of the content.

Title: {title}
Content: {content}

For each question, provide:
- question: Clear question text that tests conceptual understanding
- option_1, option_2, option_3, option_4: Four distinct, plausible options
- correct_answer: 1, 2, 3, or 4 (the correct option number)
- explanation: Detailed explanation in bullet format with 3-4 key points explaining why this is the correct answer:
  • Point 1: Why this option is correct
  • Point 2: Supporting evidence from the content
  • Point 3: Why other options are wrong or less correct

Return ONLY a JSON object with this structure:
{"questions": [{"question": "Question text", "option_1": "Option 1", "option_2": "Option 2", "option_3": "Option 3", "option_4": "Option 4", "correct_answer": 1, "explanation": "• Point 1\\n• Point 2\\n• Point 3"}]}"""
    
    prompt.prompt_text = new_prompt_text
    prompt.save()
    print("✓ Updated MCQ prompt with bullet format request")
    print(f"\nNew prompt (first 500 chars):")
    print(new_prompt_text[:500])
else:
    print("No site-specific prompt found. Creating one...")
    LLMPrompt.objects.create(
        prompt_type='mcq',
        source_url='https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/',
        prompt_text="""You are an expert in creating multiple choice questions for competitive exams.
Based on the following current affairs article, generate 4 high-quality MCQ questions that test understanding of the content.

Title: {title}
Content: {content}

For each question, provide:
- question: Clear question text that tests conceptual understanding
- option_1, option_2, option_3, option_4: Four distinct, plausible options
- correct_answer: 1, 2, 3, or 4 (the correct option number)
- explanation: Detailed explanation in bullet format with 3-4 key points explaining why this is the correct answer:
  • Point 1: Why this option is correct
  • Point 2: Supporting evidence from the content
  • Point 3: Why other options are wrong or less correct

Return ONLY a JSON object with this structure:
{"questions": [{"question": "Question text", "option_1": "Option 1", "option_2": "Option 2", "option_3": "Option 3", "option_4": "Option 4", "correct_answer": 1, "explanation": "• Point 1\\n• Point 2\\n• Point 3"}]}""",
        is_default=False,
        is_active=True
    )
    print("✓ Created new MCQ prompt with bullet format request")
