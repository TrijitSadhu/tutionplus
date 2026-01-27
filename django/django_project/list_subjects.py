from genai.models import PDFUpload

subjects = sorted(list(set(PDFUpload.objects.values_list('subject', flat=True).distinct())))

print("\nSubjects in database:")
for s in subjects:
    print(f"  • {s}")
print()
