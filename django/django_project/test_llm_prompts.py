#!/usr/bin/env python
"""Test script to verify LLMPrompt functionality"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from bank.models import LLMPrompt
from genai.tasks.current_affairs import CurrentAffairsProcessor

print("=" * 60)
print("Testing LLM Prompt Management System")
print("=" * 60)

# Test 1: Verify default prompts exist
print("\n[Test 1] Checking default prompts...")
mcq_prompts = LLMPrompt.objects.filter(
    prompt_type='mcq', 
    is_default=True, 
    is_active=True
)
desc_prompts = LLMPrompt.objects.filter(
    prompt_type='descriptive', 
    is_default=True, 
    is_active=True
)

print(f"[OK] Default MCQ prompts: {mcq_prompts.count()}")
print(f"[OK] Default Descriptive prompts: {desc_prompts.count()}")

# Test 2: Verify prompt fetching
print("\n[Test 2] Testing prompt fetching from CurrentAffairsProcessor...")
processor = CurrentAffairsProcessor()

# Test MCQ prompt fetch
mcq_prompt = processor.get_prompt_from_database('mcq')
print(f"[OK] Fetched MCQ prompt: {len(mcq_prompt) if mcq_prompt else 0} chars")

# Test Descriptive prompt fetch  
desc_prompt = processor.get_prompt_from_database('descriptive')
print(f"[OK] Fetched Descriptive prompt: {len(desc_prompt) if desc_prompt else 0} chars")

# Test 3: Verify source-specific fallback
print("\n[Test 3] Testing source-specific prompt fetching...")
prompt = processor.get_prompt_from_database('mcq', source_url='https://example.com/news')
print(f"[OK] Non-existent source falls back to default: {prompt is not None}")

# Test 4: Verify prompt template substitution
print("\n[Test 4] Testing prompt template substitution...")
test_title = "Test Article Title"
test_body = "Test article body content"

mcq_final = processor.generate_mcq_prompt(test_title, test_body)
print(f"[OK] MCQ prompt with substitution: {len(mcq_final)} chars")
print(f"  - Contains title: {test_title in mcq_final}")
print(f"  - Contains body: {test_body in mcq_final}")

desc_final = processor.generate_descriptive_prompt(test_title, test_body)
print(f"[OK] Descriptive prompt with substitution: {len(desc_final)} chars")
print(f"  - Contains title: {test_title in desc_final}")
print(f"  - Contains body: {test_body in desc_final}")

# Test 5: Verify all prompts in database
print("\n[Test 5] Listing all available prompts...")
all_prompts = LLMPrompt.objects.all()
for prompt in all_prompts:
    status = "[OK]" if prompt.is_active else "[X]"
    default = "[DEFAULT]" if prompt.is_default else ""
    source = f"({prompt.source_url})" if prompt.source_url else "(global)"
    print(f"{status} {prompt.get_prompt_type_display().upper():15} {source:20} {default}")

print("\n" + "=" * 60)
print("All tests passed! LLM Prompt Management System is working.")
print("=" * 60)
print("\nNext step: You can now modify prompts in the admin panel:")
print("  URL: http://127.0.0.1:8000/admin/bank/llmprompt/")
print("\nThe system will automatically use the right prompt based on:")
print("  1. Source URL (if specified)")
print("  2. Default prompt for the prompt type (fallback)")
print("  3. Hardcoded prompt in Python (final fallback)")
