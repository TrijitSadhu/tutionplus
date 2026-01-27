"""
Update all MCQ prompts to support DUAL-MODE MCQ generation:
1. MCQ to MCQ: Extract existing Q/A, use/create options based on content
2. Descriptive to MCQ: Create Q&A&Options from scratch
"""

from genai.models import LLMPrompt

# Template for all MCQ subjects with dual-mode support
def get_dual_mode_mcq_prompt(subject_name: str, subject_keywords: str = ""):
    """Generate dual-mode MCQ prompt for any subject"""
    keywords = f" - {subject_keywords}" if subject_keywords else ""
    
    prompt = f"""You are an expert MCQ creator for government exams (UPSC, State PSC, Railway, Bank exams) specializing in {subject_name}{keywords}.

CRITICAL: ANALYZE CONTENT FIRST
- If content contains "Q." or "Ans" or "Question" or "Answer" with actual questions visible: Use MODE 1
- Otherwise: Use MODE 2

MODE 1: MCQ to MCQ (Content has EXISTING QUESTIONS)
- Extract the question and answer directly from the PDF content
- CHECK FOR OPTIONS in content:
  * If you find option_1, option_2, option_3, option_4 or A), B), C), D), E) in content:
    - Use these options EXACTLY as they appear
    - Simplify the language to VERY EASY level (suitable for beginners)
    - Keep the meaning exactly same but use simpler words
  * If options are NOT in content:
    - CREATE 5 new options (A, B, C, D, E)
    - Make them appropriate difficulty based on {{difficulty}}
    - Ensure one is clearly correct
    - Other options should be plausible but incorrect
- Use the answer from content if available
- Explanation should be SIMPLE and CLEAR

MODE 2: Descriptive to MCQ (Content is PURELY DESCRIPTIVE, no existing questions)
- You must CREATE questions based on the descriptive content
- Create EXACTLY {{num_questions}} questions
- Create corresponding answers
- Create options (A, B, C, D, E) for each question
- Difficulty level MUST match: {{difficulty}}
  * Easy: Simple questions about basic facts/concepts - suitable for beginners
  * Medium: Standard difficulty - requires understanding of concepts
  * Hard: Complex questions requiring deep analysis and understanding (UPSC Civil Services level)

MANDATORY REQUIREMENTS (BOTH MODES):

1. **EXACTLY 5 OPTIONS per question (A, B, C, D, E)**
   - Mode 1: Extract from content or create as needed
   - Mode 2: Create all 5 options
   - One option MUST be the correct answer
   - Make options close to each other - test REAL understanding not guessing
   - All options should be roughly similar in length

2. **LANGUAGE QUALITY**
   - LUCID and EASILY UNDERSTANDABLE
   - Simple vocabulary, no unnecessary jargon
   - Questions must be CRYSTAL CLEAR
   - What is being asked should be obvious

3. **EXPLANATION (ALWAYS IN BULLET FORMAT)**
   - Each bullet = ONE key point
   - If explanation exists in content: Rewrite in EASY language
   - If explanation doesn't exist: Create clear explanation
   - Explain WHY correct answer is right
   - Explain WHY other answers are wrong (when helpful)
   - Make 3-5 bullet points total

4. **BOLD IMPORTANT EXAM WORDS**
   - Use **word** for words important for exam
   - Bold: key terms, concepts, important dates, names
   - But don't over-bold - only really important words

5. **EXAM SOURCE ATTRIBUTION**
   - If content mentions exam source (e.g., "Railway Group D 2016", "UPSC 2019", "SBI Bank 2021")
   - Include after explanation: "Exam Source: [Exam Name, Year]"

MANDATORY OUTPUT FORMAT - VALID JSON ONLY:
{{
  "questions": [
    {{
      "question": "question text here",
      "options": {{
        "A": "option A text",
        "B": "option B text",
        "C": "option C text",
        "D": "option D text",
        "E": "option E text"
      }},
      "correct_answer": "A",
      "explanation": "• First bullet point\\n• Second bullet point\\n• Third bullet point"
    }}
  ]
}}

CONTENT PROVIDED:
{{content}}

PARAMETERS:
- Number of Questions to Generate: {{num_questions}}
- Difficulty Level: {{difficulty}}
- Chapter: {{chapter}}

NOW GENERATE THE MCQs:
"""
    return prompt

# Update all MCQ prompts with dual-mode support
prompts_to_update = {
    'pdf_to_mcq_polity': ('Polity', 'Government and Constitution - includes Articles, Amendments, Rights, Duties'),
    'pdf_to_mcq_economics': ('Economics', 'Economic concepts, policies, indicators, trade, finance'),
    'pdf_to_mcq_history': ('History', 'Historical events, dates, movements, important personalities'),
    'pdf_to_mcq_geography': ('Geography', 'Physical geography, maps, climate, natural resources'),
    'pdf_to_mcq_computer': ('Computer Science & IT', 'Programming, databases, networks, technology concepts'),
    'pdf_to_mcq_mathematics': ('Mathematics', 'Algebra, geometry, trigonometry, statistics, formulas'),
    'pdf_to_mcq_physics': ('Physics', 'Laws of motion, energy, waves, mechanics, electricity'),
    'pdf_to_mcq_chemistry': ('Chemistry', 'Elements, chemical reactions, bonds, valency, periodic table'),
    'pdf_to_mcq_biology': ('Biology', 'Cells, photosynthesis, evolution, genetics, organisms, ecosystems'),
    'pdf_to_mcq_science': ('Science', 'Physics, Chemistry, and Biology combined topics'),
    'pdf_to_mcq_english': ('English', 'Grammar, vocabulary, comprehension, literature'),
    'pdf_to_mcq_other': ('General Knowledge', 'Various topics across different domains'),
}

print("Updating all MCQ prompts with DUAL-MODE support...")
print("="*80)

updated_count = 0
error_count = 0

for source_url, (subject_name, keywords) in prompts_to_update.items():
    try:
        prompt_obj = LLMPrompt.objects.get(source_url=source_url)
        new_prompt_text = get_dual_mode_mcq_prompt(subject_name, keywords)
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
print(f"SUMMARY: Updated {updated_count} prompts")
if error_count > 0:
    print(f"         Errors: {error_count}")
print("="*80)

print("\nAll MCQ prompts now support:")
print("  1. MODE DETECTION: Automatically detects Q&A vs Descriptive content")
print("  2. MCQ TO MCQ: Extracts existing questions, uses/creates options")
print("  3. DESCRIPTIVE TO MCQ: Creates questions from scratch")
print("  4. DIFFICULTY MAPPING: Applies easy/medium/hard to question creation")
print("  5. UNLIMITED MCQs: Can generate any number of questions")
print("  6. IMPROVED PROMPTS: Clearer instructions with bullet formatting")
