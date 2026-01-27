"""
Update Descriptive Prompts with enhanced instructions
Descriptive prompts are used for creating descriptive/long-answer questions
"""

from genai.models import LLMPrompt

def get_descriptive_prompt(subject_name: str, keywords: str = ""):
    """Generate enhanced descriptive prompt for any subject"""
    keywords_text = f" - {keywords}" if keywords else ""
    
    prompt = f"""You are an expert descriptive question creator for government exams (UPSC Mains, State PSC, Railway exams) specializing in {subject_name}{keywords_text}.

TASK: Create long-answer/descriptive questions from the provided content.

These are for descriptive/essay-type answers (150-300 words expected).

IMPORTANT REQUIREMENTS:

1. **QUESTION DESIGN:**
   - Create clear, comprehensive questions
   - Questions should require detailed, thoughtful answers
   - Should test understanding and analysis, not just memorization
   - Difficulty level: {{difficulty}}
     * Easy: Straightforward descriptive questions about basic concepts
     * Medium: Standard difficulty requiring good understanding
     * Hard: Complex questions requiring deep analysis (UPSC Mains level)
   - Create exactly {{num_questions}} questions

2. **LANGUAGE QUALITY:**
   - Use LUCID, EASILY UNDERSTANDABLE language
   - Simple words and structure
   - Questions should be CRYSTAL CLEAR
   - What is being asked should be obvious

3. **ANSWER FORMAT (Always Bullet Points):**
   - Provide complete answer outline in bullet points
   - Each bullet = ONE key point
   - If answer exists in content: Rewrite in SIMPLE, EASY language
   - If answer doesn't exist: Create comprehensive answer
   - Make 5-8 bullet points covering all aspects
   - Answers should be suitable for 150-300 word response

4. **BOLD IMPORTANT WORDS:**
   - Use **word** for words important for exam
   - Bold: key terms, important concepts, names, dates
   - Don't over-bold - be selective

5. **EXAM SOURCE ATTRIBUTION:**
   - If content mentions exam source (e.g., "UPSC 2019 Mains", "State PSC 2020")
   - Include after explanation: "Exam Source: [Exam Name, Year]"

MANDATORY OUTPUT FORMAT - VALID JSON ONLY:
{{
  "questions": [
    {{
      "question": "Full question text here",
      "answer": "• First bullet point\\n• Second bullet point\\n• Third bullet point\\n• Fourth bullet point\\n• Fifth bullet point",
      "explanation": "Any additional explanation or context if needed"
    }}
  ]
}}

CONTENT PROVIDED:
{{content}}

PARAMETERS:
- Number of Questions: {{num_questions}}
- Difficulty: {{difficulty}}
- Chapter: {{chapter}}

CREATE THE DESCRIPTIVE QUESTIONS NOW:
"""
    return prompt

# Update all descriptive prompts
descriptive_prompts = {
    'pdf_to_descriptive_polity': ('Polity', 'Government and Constitution'),
    'pdf_to_descriptive_economics': ('Economics', 'Economic concepts and policies'),
    'pdf_to_descriptive_history': ('History', 'Historical events and analysis'),
    'pdf_to_descriptive_geography': ('Geography', 'Physical and human geography'),
    'pdf_to_descriptive_computer': ('Computer Science', 'IT and programming concepts'),
    'pdf_to_descriptive_mathematics': ('Mathematics', 'Mathematical concepts and proofs'),
    'pdf_to_descriptive_physics': ('Physics', 'Physical laws and phenomena'),
    'pdf_to_descriptive_chemistry': ('Chemistry', 'Chemical reactions and theory'),
    'pdf_to_descriptive_biology': ('Biology', 'Biological processes and systems'),
    'pdf_to_descriptive_science': ('Science', 'General science concepts'),
    'pdf_to_descriptive_english': ('English', 'Literature and grammar'),
    'pdf_to_descriptive_other': ('General Knowledge', 'Various topics'),
}

print("Updating all Descriptive prompts with enhanced instructions...")
print("="*80)

updated_count = 0
error_count = 0

for source_url, (subject_name, keywords) in descriptive_prompts.items():
    try:
        prompt_obj = LLMPrompt.objects.get(source_url=source_url)
        new_prompt_text = get_descriptive_prompt(subject_name, keywords)
        prompt_obj.prompt_text = new_prompt_text
        prompt_obj.save()
        print(f"UPDATED: {source_url}")
        updated_count += 1
    except LLMPrompt.DoesNotExist:
        print(f"NOT FOUND: {source_url}")
        error_count += 1
    except Exception as e:
        print(f"ERROR updating {source_url}: {str(e)}")
        error_count += 1

print("\n" + "="*80)
print(f"SUMMARY: Updated {updated_count} Descriptive prompts")
if error_count > 0:
    print(f"         Errors: {error_count}")
print("="*80)

print("\nAll Descriptive prompts now include:")
print("  - Difficulty-based question creation (Easy/Medium/Hard)")
print("  - Bullet-point answer formatting")
print("  - Unlimited question generation")
print("  - Clear exam-focused instructions")
print("  - Exam source attribution")
