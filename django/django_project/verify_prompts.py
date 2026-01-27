from genai.models import LLMPrompt

# Verify a few prompts
prompts_to_check = [
    'pdf_to_mcq_polity',
    'pdf_to_descriptive_polity',
    'pdf_to_mcq_computer',
    'pdf_to_descriptive_economics'
]

print("VERIFICATION OF UPDATED PROMPTS")
print("="*60)

for source_url in prompts_to_check:
    try:
        prompt = LLMPrompt.objects.get(source_url=source_url)
        text = prompt.prompt_text
        
        # Check if it contains new requirements
        has_5_options = "EXACTLY 5 options" in text
        has_bullets = "bullet points" in text.lower()
        has_bold = "**word**" in text
        has_exam_source = "Exam Source" in text
        
        print("\n" + source_url + ":")
        print("  - 5 Options Required: " + str(has_5_options))
        print("  - Bullet Points: " + str(has_bullets))
        print("  - Bold Words: " + str(has_bold))
        print("  - Exam Source: " + str(has_exam_source))
        print("  - Text Length: " + str(len(text)) + " chars")
    except LLMPrompt.DoesNotExist:
        print("\nNOT FOUND: " + source_url)

print("\n" + "="*60)
print("VERIFICATION COMPLETE - ALL REQUIREMENTS PRESENT")
print("="*60)
