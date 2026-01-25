#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib import admin
from django.apps import apps
from genai.models import LLMPrompt

print("=" * 70)
print("ADMIN REGISTRATION DIAGNOSIS")
print("=" * 70)

# Check if registered
if LLMPrompt in admin.site._registry:
    admin_class = admin.site._registry[LLMPrompt]
    print(f"\n✓ LLMPrompt IS registered")
    print(f"  Admin Class: {admin_class.__class__.__name__}")
    print(f"  Model: {admin_class.model.__name__}")
    print(f"  App Label: {admin_class.model._meta.app_label}")
else:
    print(f"\n✗ LLMPrompt NOT registered!")

# Check app registry
print("\n" + "=" * 70)
print("ALL MODELS REGISTERED IN ADMIN")
print("=" * 70)

for model, admin_class in admin.site._registry.items():
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    verbose_name = model._meta.verbose_name_plural
    print(f"{app_label:15} {model_name:25} {verbose_name}")

# Check database
print("\n" + "=" * 70)
print("DATABASE TABLE STATUS")
print("=" * 70)

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM genai_llmprompt")
        count = cursor.fetchone()[0]
        print(f"✓ Table 'genai_llmprompt' exists")
        print(f"  Records: {count}")
except Exception as e:
    print(f"✗ Error: {e}")

# List records
print("\n" + "=" * 70)
print("LLMPrompt RECORDS")
print("=" * 70)

for prompt in LLMPrompt.objects.all():
    print(f"\nID: {prompt.id}")
    print(f"  Type: {prompt.prompt_type}")
    print(f"  Source: {prompt.source_url or '(Default)'}")
    print(f"  Active: {prompt.is_active}")
    print(f"  Default: {prompt.is_default}")
