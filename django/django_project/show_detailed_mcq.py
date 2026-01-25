#!/usr/bin/env python
"""Show detailed MCQ with all fields and categories"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from bank.models import currentaffairs_mcq

# Get the latest MCQ
mcq = currentaffairs_mcq.objects.all().order_by('-id').first()

if not mcq:
    print("No MCQs found")
else:
    print("\n" + "="*90)
    print(f"📋 DETAILED MCQ DISPLAY - ID: {mcq.id}")
    print("="*90)
    
    print(f"\n❓ QUESTION:")
    print(f"   {mcq.question}")
    
    print(f"\n🔤 OPTIONS:")
    print(f"   1️⃣  {mcq.option_1}")
    print(f"   2️⃣  {mcq.option_2}")
    print(f"   3️⃣  {mcq.option_3}")
    print(f"   4️⃣  {mcq.option_4}")
    
    print(f"\n✅ CORRECT ANSWER: Option {mcq.ans}")
    
    print(f"\n📚 EXPLANATION:")
    if mcq.extra:
        # Print explanation with proper formatting
        explanation_lines = mcq.extra.split('\n')
        for line in explanation_lines:
            if line.strip():
                print(f"   {line}")
    else:
        print("   (No explanation provided)")
    
    print(f"\n🏷️  CATEGORIES:")
    
    categories = []
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
            print(f"   ✓ {cat}")
    else:
        print("   (No categories assigned)")
    
    print(f"\n📅 METADATA:")
    print(f"   Date: {mcq.day}")
    print(f"   Time: {mcq.creation_time}")
    print(f"   Status: {'Live' if mcq.is_live else 'Hidden'}")
    
    print("\n" + "="*90)
