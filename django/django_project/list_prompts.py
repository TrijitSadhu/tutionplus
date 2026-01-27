from genai.models import LLMPrompt

print("\n" + "="*80)
print("ALL PROMPTS IN DATABASE")
print("="*80 + "\n")

prompts = LLMPrompt.objects.all().order_by('source_url')

for p in prompts:
    status = "✓" if p.is_active else "✗"
    source = p.source_url or "DEFAULT"
    print(f"  {status} {source:<45} | {p.prompt_type:<12}")

print(f"\nTotal: {prompts.count()} prompts\n")
print("="*80 + "\n")
