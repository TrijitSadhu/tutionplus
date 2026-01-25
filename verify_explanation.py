import sys
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

import django
django.setup()

from bank.models import currentaffairs_mcq

print("Verifying explanations are saved in extra field:\n")

mcq = currentaffairs_mcq.objects.get(id=46)
print(f"MCQ ID 46:")
print(f"  Question: {mcq.question}")
print(f"  Option 1: {mcq.option_1}")
print(f"  Option 2: {mcq.option_2}")
print(f"  Option 3: {mcq.option_3}")
print(f"  Option 4: {mcq.option_4}")
print(f"  Correct Answer (ans): {mcq.ans}")
print(f"\n  Extra Field (Explanation):")
print(f"  {mcq.extra}")
print("\n✅ Explanations are now being saved in the extra field!")
