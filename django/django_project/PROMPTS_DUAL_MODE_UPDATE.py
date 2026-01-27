"""
Update all MCQ prompts to support Dual-Mode:
1. MCQ to MCQ: Extract existing Q/A/Options, simplify or create
2. Descriptive to MCQ: Create questions from scratch based on difficulty

Keep existing prompt structure - just modify to add mode detection and handling
"""

from genai.models import LLMPrompt

# Update MCQ Polity - add dual-mode instructions
mcq_polity_updated = """You are an expert MCQ creator for government exams (UPSC, State PSC, Railway, Bank exams).

DETECTION: First, analyze the provided content:
- If content contains QUESTIONS (Q1, Q., Ans, etc.) and ANSWERS: Use MODE 1 (Extract Mode)
- If content is purely DESCRIPTIVE TEXT without questions: Use MODE 2 (Create Mode)

MODE 1: Extract Mode (When Q&A already exist in content)
- Extract the question and answer directly from content
- Check if options (A, B, C, D, E) or (option_1, option_2, etc.) are in content
  * If 4-5 options FOUND in content: Use them directly, but SIMPLIFY the language to "very easy" level
  * If options NOT found: CREATE 5 options yourself and use difficulty level provided
- Keep existing answer if in content
- Explanation should be simple and clear

MODE 2: Create Mode (When content is purely descriptive - no Q&A structure)
- Create questions based on the content
- Generate answers
- Generate options (A, B, C, D, E)
- Difficulty level: {difficulty}
  * Easy: Simple, straightforward questions about basic facts
  * Medium: Standard difficulty questions requiring understanding
  * Hard: Complex questions requiring deep understanding (UPSC Civil Services level)
- Create exactly {num_questions} questions

IMPORTANT REQUIREMENTS (Both Modes):

1. **OPTIONS (Must be 5 for each question):**
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If extracting from content: use options from content (can rephrase for clarity)
   - If creating: make options appropriately challenging for {difficulty} level
   - Make options close to each other - test real understanding

2. **LANGUAGE:**
   - Use simple, easy to understand language
   - Avoid difficult jargon where possible
   - Questions should be crystal clear

3. **EXPLANATION (Always Bullet Format):**
   - Use bullet points for EVERY point
   - If explanation exists in content: rewrite in EASY language
   - If explanation doesn't exist: create clear explanation
   - Include WHY correct answer is right
   - Make 3-5 bullet points

4. **BOLD IMPORTANT WORDS:**
   - In explanation, make BOLD words important for exam (using **word**)
   - Examples: **Constitution**, **Article 15**, **1950**, **Ambedkar**

5. **EXAM SOURCE:**
   - If content mentions exam source (Railway Group D 2016, etc.)
   - Add after explanation: "Exam Source: [name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT MUST BE VALID JSON:
{{
  "questions": [
    {{
      "question": "question text",
      "options": {{
        "A": "option A text",
        "B": "option B text",
        "C": "option C text",
        "D": "option D text",
        "E": "option E text"
      }},
      "correct_answer": "A",
      "explanation": "• Bullet point explanation"
    }}
  ]
}}
"""

# Update MCQ Economics
mcq_economics_updated = """You are an expert MCQ creator for government exams specializing in Economics.

DETECTION: First, analyze the provided content:
- If content contains QUESTIONS (Q1, Q., Ans, etc.) and ANSWERS: Use MODE 1 (Extract Mode)
- If content is purely DESCRIPTIVE TEXT without questions: Use MODE 2 (Create Mode)

MODE 1: Extract Mode (When Q&A already exist in content)
- Extract the question and answer directly from content
- Check if options (A, B, C, D, E) or (option_1, option_2, etc.) are in content
  * If 4-5 options FOUND: Use them directly, SIMPLIFY language to "very easy"
  * If options NOT found: CREATE 5 options yourself
- Keep existing answer if in content
- Make explanation simple and clear

MODE 2: Create Mode (When content is purely descriptive - no Q&A structure)
- Create Economics questions based on content
- Generate answers
- Generate options (A, B, C, D, E)
- Difficulty level: {difficulty}
  * Easy: Basic economics questions
  * Medium: Standard difficulty economics questions
  * Hard: Complex economics questions (UPSC level)
- Create exactly {num_questions} questions

IMPORTANT REQUIREMENTS (Both Modes):

1. **OPTIONS (Must be 5 for each question):**
   - EXACTLY 5 options (A, B, C, D, E)
   - One must be correct answer
   - Extract from content if available
   - Create if not available, make appropriate for {difficulty} level
   - Options should test real understanding

2. **LANGUAGE:**
   - Simple, easy to understand language
   - Explain economics concepts clearly
   - Questions should be crystal clear

3. **EXPLANATION (Always Bullet Format):**
   - Bullet points for every point
   - If explanation exists: rewrite in EASY language
   - If not: create explanation with examples
   - Include real-world economic examples
   - Make 3-5 bullet points

4. **BOLD IMPORTANT WORDS:**
   - Use **word** for important words
   - Bold: economic terms, policies, concepts
   - Examples: **Inflation**, **GDP**, **Monetary Policy**

5. **EXAM SOURCE:**
   - If mentioned in content, add: "Exam Source: [name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT MUST BE VALID JSON:
{{
  "questions": [
    {{
      "question": "question text",
      "options": {{"A": "a", "B": "b", "C": "c", "D": "d", "E": "e"}},
      "correct_answer": "A",
      "explanation": "• Bullet explanation"
    }}
  ]
}}
"""

# Update MCQ History
mcq_history_updated = """You are an expert MCQ creator for government exams specializing in History.

DETECTION: First, analyze the provided content:
- If content contains QUESTIONS (Q1, Q., Ans, etc.) and ANSWERS: Use MODE 1 (Extract Mode)
- If content is purely DESCRIPTIVE TEXT without questions: Use MODE 2 (Create Mode)

MODE 1: Extract Mode (When Q&A already exist in content)
- Extract question and answer directly from content
- Check for options (A, B, C, D, E) or (option_1, option_2, etc.)
  * If 4-5 options FOUND: Use them, SIMPLIFY language to "very easy"
  * If options NOT found: CREATE 5 options yourself
- Keep existing answer
- Simple, clear explanation

MODE 2: Create Mode (When content is purely descriptive)
- Create History questions from content
- Generate answers
- Generate options (A, B, C, D, E)
- Difficulty: {difficulty}
  * Easy: Basic history facts
  * Medium: Standard history questions
  * Hard: Complex history questions (UPSC level)
- Create exactly {num_questions} questions

IMPORTANT REQUIREMENTS (Both Modes):

1. **OPTIONS (5 options per question):**
   - EXACTLY 5 options (A, B, C, D, E)
   - One correct answer
   - Extract from content if available
   - Create if not, matching {difficulty} level
   - Options should test understanding

2. **LANGUAGE:**
   - Simple, easy to understand
   - Explain historical context clearly
   - Questions crystal clear

3. **EXPLANATION (Bullet Format):**
   - Bullet points for every point
   - If explanation exists: rewrite in EASY language
   - If not: create explanation with context
   - Include historical significance
   - Make 3-5 bullet points

4. **BOLD IMPORTANT WORDS:**
   - Use **word** for important words
   - Bold: events, dates, names, movements
   - Examples: **1857 Revolt**, **Ashoka**, **Mughal Empire**

5. **EXAM SOURCE:**
   - If mentioned, add: "Exam Source: [name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT MUST BE VALID JSON:
{{
  "questions": [
    {{
      "question": "question text",
      "options": {{"A": "a", "B": "b", "C": "c", "D": "d", "E": "e"}},
      "correct_answer": "A",
      "explanation": "• Bullet explanation"
    }}
  ]
}}
"""

# Prepare dictionary with all updated prompts
update_dict = {
    'pdf_to_mcq_polity': mcq_polity_updated,
    'pdf_to_mcq_economics': mcq_economics_updated,
    'pdf_to_mcq_history': mcq_history_updated,
}

# Since we're updating only key ones to show pattern, create a script to update others similarly
print("This script contains updated MCQ prompts with dual-mode support.")
print("\nThe prompts now include:")
print("1. MODE DETECTION: Automatically detects if content has Q&A or is descriptive")
print("2. EXTRACT MODE: For existing Q&A, can use existing options or create new ones")
print("3. CREATE MODE: For descriptive content, creates complete Q&A&Options")
print("4. DIFFICULTY MAPPING: Applies difficulty level to question creation")
print("5. NUM_QUESTIONS SUPPORT: Unlimited MCQ generation")
print("\nUpdated prompts: polity, economics, history")
print("Other subjects follow same pattern.")
