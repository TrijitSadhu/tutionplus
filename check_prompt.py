import sys
import os

# Add django project to path
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

import django
django.setup()

from genai.models import LLMPrompt

prompt = LLMPrompt.objects.filter(prompt_type='mcq', is_active=True).first()
if prompt:
    print('MCQ Prompt Template:')
    print(prompt.prompt_text)
    print("\n" + "="*80)
    print("\nChecking for 'correct_answer' format...")
    if 'correct_answer' in prompt.prompt_text.lower():
        idx = prompt.prompt_text.lower().find('correct_answer')
        print(f"Found at position {idx}:")
        print(prompt.prompt_text[idx-50:idx+100])
else:
    print("No MCQ prompt found")
