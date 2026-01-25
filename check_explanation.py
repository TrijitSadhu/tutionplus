import sys
sys.path.insert(0, r'C:\Users\newwe\Desktop\tution\tutionplus\django\django_project')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

import django
django.setup()

from genai.models import LLMPrompt
import requests
from bs4 import BeautifulSoup

# Check current prompt
prompt = LLMPrompt.objects.filter(prompt_type='mcq', is_active=True).first()
if prompt:
    print("Current MCQ Prompt:")
    print(prompt.prompt_text)
    print("\n" + "="*80 + "\n")

# Check website for explanation
print("Checking website for explanation field...")
url = 'https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/'
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(resp.text, 'html.parser')

# Find correct answer sections with explanations
main = soup.find('main')
if main:
    # Look for ques_answer divs (which contain correct answer and explanation)
    answer_divs = main.find_all('div', class_='ques_answer')
    print(f"\nFound {len(answer_divs)} answer divs")
    
    for i, div in enumerate(answer_divs[:2]):  # Show first 2
        print(f"\nAnswer Section {i+1}:")
        print(div.get_text(strip=True)[:200])
        print("...")
