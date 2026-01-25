import sys
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

import django
django.setup()

from bank.models import currentaffairs_mcq

print("Checking latest MCQs (51-54) with updated bullet format prompt:\n")

for mcq_id in [51, 52, 53, 54]:
    mcq = currentaffairs_mcq.objects.get(id=mcq_id)
    print(f"MCQ ID {mcq_id}:")
    print(f"  Question: {mcq.question[:60]}...")
    print(f"  Ans: {mcq.ans}")
    print(f"  Extra Field (Explanation):")
    explanation_lines = mcq.extra.split('\n')
    for line in explanation_lines:
        if line.strip():
            print(f"    {line}")
    print()
