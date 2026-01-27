import os
import sys
import django

sys.path.insert(0, r'c:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import LLMPrompt

print("="*80)
print("ALL MCQ PROMPTS IN DATABASE")
print("="*80)

prompts = LLMPrompt.objects.filter(prompt_type='mcq')
for p in prompts:
    print(f"\n📋 ID: {p.id}")
    print(f"   Type: {p.prompt_type}")
    print(f"   Source: {p.source_url}")
    print(f"   Default: {p.is_default}")
    print(f"   Active: {p.is_active}")
    print(f"   Text (first 150 chars): {p.prompt_text[:150]}...")

print("\n" + "="*80)
print("SKIP-SCRAPING SPECIFIC PROMPT:")
print("="*80)

skip_prompt = LLMPrompt.objects.filter(source_url='skip_scraping_mode').first()
if skip_prompt:
    print(f"✅ FOUND - ID: {skip_prompt.id}")
    print(f"Full prompt text:\n{skip_prompt.prompt_text}")
else:
    print("❌ NOT FOUND")
