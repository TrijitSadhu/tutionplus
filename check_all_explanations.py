import sys
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

import django
django.setup()

from bank.models import currentaffairs_mcq

print("Checking all new MCQs (46-50) for explanations:\n")

for mcq_id in [46, 47, 48, 49, 50]:
    mcq = currentaffairs_mcq.objects.get(id=mcq_id)
    print(f"MCQ ID {mcq_id}:")
    print(f"  Question: {mcq.question[:60]}...")
    print(f"  Extra Field Explanation:")
    print(f"  {mcq.extra}")
    print()
