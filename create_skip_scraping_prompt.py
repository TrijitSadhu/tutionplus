import os
import sys
import django

# Setup Django
sys.path.insert(0, r'c:\Users\newwe\Desktop\tution\tutionplus\django\django_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from genai.models import LLMPrompt

# Create a special prompt for skip-scraping mode (direct URL to LLM)
skip_scraping_prompt = LLMPrompt.objects.create(
    prompt_type='mcq',
    prompt_text="""You are an expert in creating multiple choice questions for competitive exams.

The following URL contains current affairs content. Please:
1. Fetch and read the content from this URL: {content}
2. Extract key information from the page
3. Generate 3 high-quality MCQ questions based on the content

Return ONLY a JSON object with this structure:
{"questions": [{"question": "Question text", "option_a": "Option A", "option_b": "Option B", "option_c": "Option C", "option_d": "Option D", "correct_answer": "A", "explanation": "Why this answer is correct"}]}

Important:
- Each MCQ should be based on actual information from the URL
- Options should be plausible but distinct
- Explanations should reference the source content
- Return ONLY valid JSON, no additional text""",
    is_default=False,
    is_active=True,
    source_url='skip_scraping_mode'
)

print("="*80)
print("✅ CREATED SKIP-SCRAPING MODE PROMPT")
print("="*80)
print(f"ID: {skip_scraping_prompt.id}")
print(f"Type: {skip_scraping_prompt.prompt_type}")
print(f"Source: {skip_scraping_prompt.source_url}")
print(f"Active: {skip_scraping_prompt.is_active}")
print("\n" + "="*80)
print("Prompt Text (First 400 chars):")
print("="*80)
print(skip_scraping_prompt.prompt_text[:400])
print("\n" + "="*80)
print("✅ Now update the pipeline to use this prompt in skip-scraping mode")
print("="*80)
