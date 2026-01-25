import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from bank.models import currentaffairs_mcq

print("Checking ans field for newly saved MCQs:\n")
for mcq_id in [36, 37, 38, 39, 40]:
    mcq = currentaffairs_mcq.objects.get(id=mcq_id)
    print(f"MCQ ID {mcq_id}:")
    print(f"  Question: {mcq.question[:50]}...")
    print(f"  ans field value: {mcq.ans}")
    opt_text = getattr(mcq, f'option_{mcq.ans}', '')
    print(f"  Option {mcq.ans} text: {opt_text[:50]}...")
    print()
