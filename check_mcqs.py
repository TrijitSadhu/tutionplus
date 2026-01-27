import os
import sys
import django

sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from bank.models import currentaffairs_mcq

mcqs = currentaffairs_mcq.objects.filter(id__gte=79).order_by('id')
print("=== LATEST MCQs GENERATED ===\n")
for mcq in mcqs:
    print(f"MCQ ID: {mcq.id}")
    print(f"Question: {mcq.question[:120]}")
    print(f"Option 1: {mcq.option_1[:80]}")
    print()
