#!/usr/bin/env python
"""Verify categories are correctly applied to MCQs"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from bank.models import currentaffairs_mcq

# Get the latest MCQs
mcqs = currentaffairs_mcq.objects.all().order_by('-id')[:4]

print("\n" + "="*80)
print("📊 MCQ CATEGORY VERIFICATION")
print("="*80)

for mcq in mcqs:
    print(f"\n📌 MCQ ID: {mcq.id}")
    print(f"   Question: {mcq.question[:70]}...")
    print(f"\n   ✓ Categories Applied:")
    
    categories = []
    # Check all boolean category fields
    if mcq.Science_Techonlogy:
        categories.append("Science_Techonlogy")
    if mcq.National:
        categories.append("National")
    if mcq.International:
        categories.append("International")
    if mcq.Business_Economy_Banking:
        categories.append("Business_Economy_Banking")
    if mcq.Environment:
        categories.append("Environment")
    if mcq.Defence:
        categories.append("Defence")
    if mcq.Sports:
        categories.append("Sports")
    if mcq.Art_Culture:
        categories.append("Art_Culture")
    if mcq.Awards_Honours:
        categories.append("Awards_Honours")
    if mcq.Persons_in_News:
        categories.append("Persons_in_News")
    if mcq.Government_Schemes:
        categories.append("Government_Schemes")
    if mcq.State:
        categories.append("State")
    if mcq.appointment:
        categories.append("appointment")
    if mcq.obituary:
        categories.append("obituary")
    if mcq.important_day:
        categories.append("important_day")
    if mcq.rank:
        categories.append("rank")
    if mcq.mythology:
        categories.append("mythology")
    if mcq.agreement:
        categories.append("agreement")
    if mcq.medical:
        categories.append("medical")
    if mcq.static_gk:
        categories.append("static_gk")
    
    if categories:
        for cat in categories:
            print(f"      • {cat}")
    else:
        print(f"      (No categories applied)")

print("\n" + "="*80)
