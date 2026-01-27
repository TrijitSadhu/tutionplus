from genai.models import LLMPrompt

# Check existing prompt structure
p = LLMPrompt.objects.get(source_url='pdf_to_mcq_polity')
print("Current MCQ Polity Prompt:")
print("="*80)
print(p.prompt_text[:1000])
print("\n" + "="*80)
print(f"Total length: {len(p.prompt_text)} characters")
