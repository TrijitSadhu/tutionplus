#!/usr/bin/env python
"""
Script to add news sources to the database via Django admin.
Run this once to populate initial sources.

Usage:
    python manage.py shell < genai/scripts/add_news_sources.py
    
    OR
    
    from django.core.management import execute_from_command_line
    import sys
    sys.path.insert(0, 'django/django_project')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
    django.setup()
    exec(open('genai/scripts/add_news_sources.py').read())
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from bank.models import NewsSource

# Define news sources
NEWS_SOURCES = [
    {
        'name': 'GK Today',
        'url': 'https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/',
        'content_type': 'mcq',
        'description': 'Daily current affairs quiz from GK Today website'
    },
    # Add more sources here
    # {
    #     'name': 'Example Descriptive',
    #     'url': 'https://example-descriptive-site.com',
    #     'content_type': 'descriptive',
    #     'description': 'Example descriptive content source'
    # },
]

def add_sources():
    """Add news sources to database"""
    print("Adding news sources to database...\n")
    
    for source_data in NEWS_SOURCES:
        # Check if source already exists
        existing = NewsSource.objects.filter(url=source_data['url']).first()
        
        if existing:
            print(f"✓ Source already exists: {source_data['name']}")
            continue
        
        # Create new source
        source = NewsSource.objects.create(**source_data)
        print(f"✓ Added: {source.name} ({source.get_content_type_display()})")
    
    print("\n✓ All sources added successfully!")
    print("\nTo manage sources, go to: /admin/bank/newssource/")

if __name__ == '__main__':
    add_sources()
