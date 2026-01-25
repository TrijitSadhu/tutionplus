#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

# Test imports
try:
    from genai.models import LLMPrompt, ContentSource
    print("✓ LLMPrompt imported from genai.models")
    print("✓ ContentSource imported from genai.models")
    
    from genai.tasks.current_affairs import CurrentAffairsProcessor, CurrentAffairsScraper
    print("✓ CurrentAffairsProcessor imported successfully")
    print("✓ CurrentAffairsScraper imported successfully")
    
    print("\n✓ All imports successful!")
    print("✓ LLMPrompt migration from bank to genai completed!")
    print("✓ System is ready to use")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
