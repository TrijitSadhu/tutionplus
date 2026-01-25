#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib import admin
from genai.models import LLMPrompt

print("=" * 60)
print("CHECKING ADMIN REGISTRATION")
print("=" * 60)

# Check if LLMPrompt is registered
llmprompt_admin = admin.site._registry.get(LLMPrompt)

if llmprompt_admin:
    print(f"✓ LLMPrompt is registered in admin")
    print(f"  Admin Class: {llmprompt_admin.__class__.__name__}")
    print(f"  Model: {llmprompt_admin.model.__name__}")
else:
    print("✗ LLMPrompt is NOT registered in admin")

print("\n" + "=" * 60)
print("ALL REGISTERED MODELS IN GENAI")
print("=" * 60)

from genai import models as genai_models

# Get all models from genai app
for name in dir(genai_models):
    obj = getattr(genai_models, name)
    if isinstance(obj, type) and issubclass(obj, django.db.models.Model) and obj.__module__ == 'genai.models':
        is_registered = obj in admin.site._registry
        status = "✓ REGISTERED" if is_registered else "✗ NOT REGISTERED"
        print(f"{status:20} {name}")

print("\n" + "=" * 60)
print("LLMPROMPT MODEL INFO")
print("=" * 60)

print(f"Model: {LLMPrompt}")
print(f"Database table: {LLMPrompt._meta.db_table}")
print(f"App label: {LLMPrompt._meta.app_label}")

# Check database
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM genai_llmprompt")
        count = cursor.fetchone()[0]
        print(f"Records in DB: {count}")
except Exception as e:
    print(f"Error checking database: {e}")
