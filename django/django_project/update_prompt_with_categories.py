#!/usr/bin/env python
"""Update LLMPrompt with category classification instructions"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import LLMPrompt

# The updated prompt with category classification
updated_prompt = """You are an expert in creating multiple choice questions for competitive exams based on current affairs.
Based on the provided current affairs article, generate 4 high-quality MCQ questions.

Title: {title}
Content: {content}

CATEGORY CLASSIFICATION - IMPORTANT:
After analyzing the article content, classify which of these categories the MCQ belongs to. 
Select ALL that apply (can be multiple categories). Use your judgment based on the content:
- Science_Techonlogy: For technology, innovation, research, engineering, scientific discoveries
- National: For India-specific news, policies, government, national events, Indian politics
- International: For global news, international relations, foreign countries, UN, world events
- Business_Economy_Banking: For economy, business, markets, finance, banking, commerce, trade
- Environment: For environmental issues, climate, pollution, conservation, wildlife
- Defence: For military, defence, security, armed forces, wars, defense policy
- Sports: For sports events, athletes, tournaments, sports organizations
- Art_Culture: For arts, culture, heritage, literature, music, cultural events
- Awards_Honours: For awards, honors, recognitions, achievements, competitions
- Persons_in_News: For notable personalities, appointments, resignations, important people
- Government_Schemes: For government programs, policies, schemes, initiatives, welfare
- State: For state-specific news (mention which state it concerns)
- appointment: For new appointments, positions, leadership changes, transfers
- obituary: For death announcements, obituaries, notable deaths
- important_day: For special days, commemorations, anniversaries, observances
- rank: For rankings, ratings, positions, surveys, statistics
- mythology: For historical or mythological references, historical events
- agreement: For treaties, agreements, MOUs, international pacts
- medical: For medical discoveries, health issues, medicine, healthcare
- static_gk: For general knowledge facts, historical information, basic facts

For each question, return in JSON format:
- question: Clear question text based on article content
- option_1, option_2, option_3, option_4: Four distinct options
- correct_answer: 1, 2, 3, or 4 (the correct option number)
- explanation: Detailed bullet-point explanation (3-4 key points with • bullet format)
- categories: ARRAY of 1-3 most relevant category names (MUST be exact names from list above)

IMPORTANT: The "categories" field MUST be an array, and category names MUST match exactly from the list above.

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question about article topic?",
            "option_1": "First option",
            "option_2": "Second option",
            "option_3": "Third option",
            "option_4": "Fourth option",
            "correct_answer": 1,
            "explanation": "• Why this is correct\\n• Supporting point from article\\n• Additional context",
            "categories": ["National", "Art_Culture"]
        }}
    ]
}}"""

try:
    # Find and update the existing MCQ prompt for gktoday
    llm_prompt = LLMPrompt.objects.filter(
        prompt_type='mcq',
        source_url__icontains='gktoday.in'
    ).first()
    
    if llm_prompt:
        print(f"✓ Found existing prompt (ID: {llm_prompt.id})")
        print(f"  Old length: {len(llm_prompt.prompt_text)} chars")
        
        llm_prompt.prompt_text = updated_prompt
        llm_prompt.save()
        
        print(f"  New length: {len(llm_prompt.prompt_text)} chars")
        print("✓ Prompt updated successfully with category classification!")
    else:
        print("❌ No MCQ prompt found for gktoday.in")
        print("Available prompts:")
        for prompt in LLMPrompt.objects.all():
            print(f"  - {prompt.source_url} ({prompt.prompt_type})")
            
except Exception as e:
    print(f"❌ Error: {str(e)}")
