import os
import sys
import django

# Setup Django
sys.path.insert(0, r'c:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import LLMPrompt

# Get default MCQ prompt
prompt = LLMPrompt.objects.filter(prompt_type='mcq', is_default=True).first()

if prompt:
    print("="*80)
    print("DEFAULT MCQ PROMPT (First 800 chars):")
    print("="*80)
    print(prompt.prompt_text[:800])
    print("\n" + "="*80)
    print(f"Full length: {len(prompt.prompt_text)} characters")
    print("="*80)
else:
    print("NO DEFAULT MCQ PROMPT FOUND")
    print("\nLet's check what prompts exist:")
    prompts = LLMPrompt.objects.filter(prompt_type='mcq')
    for p in prompts:
        print(f"  - ID: {p.id}, Type: {p.prompt_type}, Default: {p.is_default}, Source: {p.source_url}")
