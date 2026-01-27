import os
import sys
import django

sys.path.insert(0, r'c:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import ProcessingLog

# Create new ProcessingLog for testing with STANDARD scraping mode (working mode)
test_log = ProcessingLog.objects.create(
    task_type='currentaffairs_mcq_fetch',
    skip_scraping=False,  # STANDARD MODE - This works!
    status='running'
)

print("="*80)
print("✅ CREATED TEST PROCESSINGLOG FOR STANDARD SCRAPING MODE")
print("="*80)
print(f"ID: {test_log.id}")
print(f"Task Type: {test_log.task_type}")
print(f"Skip Scraping: {test_log.skip_scraping} (Standard Mode - This Works!)")
print(f"Status: {test_log.status}")
print("\n" + "="*80)
print("Run this command to test (will work - generates MCQs):")
print(f"  python manage.py fetch_all_content --type=currentaffairs_mcq --log-id={test_log.id}")
print("="*80)
