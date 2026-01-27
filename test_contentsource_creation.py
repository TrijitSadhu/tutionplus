#!/usr/bin/env python
"""Test ContentSource creation after migration"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import ContentSource
from django.contrib.auth.models import User
from django.utils import timezone

try:
    user = User.objects.first()
    
    # Test creating a ContentSource entry
    source = ContentSource(
        source_type='currentaffairs_mcq',
        url='https://example.com/test-migration',
        name='Test Migration Source',
        description='Test to verify columns removed',
        created_by=user
    )
    source.save()
    print(f"✅ SUCCESS: ContentSource created with ID {source.id}")
    print(f"   Name: {source.name}")
    print(f"   URL: {source.url}")
    print(f"   Type: {source.source_type}")
    print(f"   Active: {source.is_active}")
    print(f"   Created: {source.created_at}")
    
    # Clean up
    source.delete()
    print(f"✅ Test entry deleted successfully")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
