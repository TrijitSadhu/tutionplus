#!/usr/bin/env python
"""Create the CA MCQ prompt with categories"""
import os
import sys
import django

sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import LLMPrompt

# Delete if exists
LLMPrompt.objects.filter(source_url='pdf_current_affairs_mcq', prompt_type='mcq').delete()

# Create new prompt
prompt_text = """You are an expert in creating multiple choice questions for competitive exams based on current affairs.
Based on the provided current affairs article, generate 3-5 high-quality MCQ questions.

Content: {content}

CATEGORY CLASSIFICATION - IMPORTANT:
Classify each MCQ into these categories (select 1-3 most relevant):

- Science_Techonlogy: Technology, innovation, research, engineering, scientific discoveries
- National: India-specific news, policies, government, national events, Indian politics
- International: Global news, international relations, foreign countries, UN, world events
- Business_Economy_Banking: Economy, business, markets, finance, banking, commerce, trade
- Environment: Environmental issues, climate, pollution, conservation, wildlife
- Defence: Military, defence, security, armed forces, wars
- Sports: Sports events, athletes, tournaments, sports organizations
- Art_Culture: Arts, culture, heritage, literature, music, cultural events
- Awards_Honours: Awards, honors, recognitions, achievements, competitions
- Persons_in_News: Notable personalities, appointments, resignations, important people
- Government_Schemes: Government programs, policies, schemes, initiatives, welfare
- State: State-specific news
- appointment: New appointments, positions, leadership changes
- obituary: Death announcements, obituaries, notable deaths
- important_day: Special days, commemorations, anniversaries
- rank: Rankings, ratings, positions, surveys, statistics
- mythology: Historical or mythological references
- agreement: Treaties, agreements, MOUs, international pacts
- medical: Medical discoveries, health issues, medicine, healthcare
- static_gk: General knowledge facts, historical information

For each question, return JSON:
- question: Clear question text based on article
- option_a, option_b, option_c, option_d: Four distinct options
- correct_answer: A, B, C, or D
- explanation: Bullet-point explanation (3-4 points)
- categories: ARRAY of 1-3 category names (exact match required)

Return ONLY valid JSON:
{
    "questions": [
        {
            "question": "Question about article?",
            "option_a": "First option",
            "option_b": "Second option",
            "option_c": "Third option",
            "option_d": "Fourth option",
            "correct_answer": "A",
            "explanation": "• Explanation point\\n• Supporting point\\n• Additional context",
            "categories": ["National", "Art_Culture"]
        }
    ]
}"""

prompt = LLMPrompt.objects.create(
    source_url='pdf_current_affairs_mcq',
    prompt_type='mcq',
    prompt_text=prompt_text,
    is_active=True
)

print(f"✓ Created CA MCQ prompt (ID: {prompt.id})")
print(f"  Prompt length: {len(prompt_text)} chars")
