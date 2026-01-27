import os
import sys
import django
import datetime

# Setup Django
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import ContentSource

# Check current IndiaBIX source
source = ContentSource.objects.filter(url__contains='indiabix').first()
if source:
    print(f"Current IndiaBIX URL: {source.url}")
    print(f"Source Type: {source.source_type}")
    print(f"Active: {source.is_active}")
    
    # IndiaBIX website structure issue: The page likely doesn't have proper quiz content
    # in the regular current-affairs section. Let's try the MCQ section
    source.url = "https://www.indiabix.com/current-affairs-mcq/"
    source.source_type = "currentaffairs_mcq"
    source.content_date = datetime.date.today()
    source.save()
    print(f"\nUpdated URL to: {source.url}")
    print(f"Updated content_date to: {source.content_date}")
else:
    print("No IndiaBIX source found")
    # Create one
    source = ContentSource.objects.create(
        url="https://www.indiabix.com/current-affairs-mcq/",
        source_type="currentaffairs_mcq",
        content_date=datetime.date.today(),
        is_active=True,
        created_by="system"
    )
    print(f"Created new IndiaBIX source: {source.url}")
