import os
import sys
import django

sys.path.insert(0, os.path.join(os.getcwd(), 'django', 'django_project'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import LLMPrompt

# Update the skip-scraping prompt
new_prompt_text = """You are an expert in creating multiple choice questions for competitive exams.

The following is current affairs content that has already been extracted from a webpage. Please:
1. Carefully read and analyze the provided content: {content}
2. Extract key information and facts from the content
3. Generate 3-4 high-quality MCQ questions based on ONLY the provided content

Return ONLY a JSON object with this structure:
{"questions": [{"question": "Question text", "option_a": "Option A", "option_b": "Option B", "option_c": "Option C", "option_d": "Option D", "correct_answer": "A", "explanation": "Why this answer is correct"}]}

Important Guidelines:
- Use ONLY the information provided in the content - do NOT fetch or look up external information
- Each MCQ should test understanding of the provided content
- Options should be plausible but clearly distinct
- Correct answer must be one of: A, B, C, or D
- Explanations should reference specific details from the provided content
- Return ONLY valid JSON, no additional text or explanations
- If content is insufficient or irrelevant for MCQ generation, return: {"questions": []}
"""

prompt = LLMPrompt.objects.get(source_url='skip_scraping_mode')
prompt.prompt_text = new_prompt_text
prompt.save()

print('='*80)
print('✅ SKIP-SCRAPING PROMPT UPDATED')
print('='*80)
print('New prompt tells LLM to use PROVIDED content, not fetch URLs')
print(f'Updated prompt length: {len(new_prompt_text)} characters')
print('\nFirst 400 chars of updated prompt:')
print('-'*80)
print(new_prompt_text[:400])
print('-'*80)
print('\n✅ This change will allow skip-scraping to work for both sources')
