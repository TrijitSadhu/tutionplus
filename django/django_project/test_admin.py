#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

# Import admin explicitly
import django.contrib.admin as admin_module
from genai.admin import LLMPromptAdmin
from genai.models import LLMPrompt

print("✓ LLMPromptAdmin imported successfully")
print("✓ LLMPrompt model imported successfully")

# Try to register manually
try:
    # Check if already registered
    if LLMPrompt in admin_module.site._registry:
        print("✓ LLMPrompt already registered")
        print(f"  Admin: {admin_module.site._registry[LLMPrompt].__class__.__name__}")
    else:
        print("✗ LLMPrompt NOT registered, registering now...")
        admin_module.site.register(LLMPrompt, LLMPromptAdmin)
        print("✓ LLMPrompt registered successfully")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

# List all models in genai admin
print("\n" + "="*60)
print("Models registered in genai admin:")
print("="*60)
from genai.models import (PDFUpload, CurrentAffairsGeneration, MathProblemGeneration, 
                           ProcessingTask, ProcessingLog, ContentSource)

models = [PDFUpload, CurrentAffairsGeneration, MathProblemGeneration, 
          ProcessingTask, ProcessingLog, ContentSource, LLMPrompt]

for model in models:
    is_registered = model in admin_module.site._registry
    status = "✓" if is_registered else "✗"
    print(f"{status} {model.__name__}")
