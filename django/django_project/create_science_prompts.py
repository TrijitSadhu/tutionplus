from genai.models import LLMPrompt

# Create Physics-specific prompts
mcq_physics = """You are an expert MCQ creator for government exams specializing in Physics.

TASK: Create Physics MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant physics options
   - Make options appropriately challenging
   - Test physics understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain physics concepts clearly
   - Questions should be crystal clear
   - Make physics accessible

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Include practical examples
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: physics laws, formulas, concepts
   - Examples: **Newton's Laws**, **Force**, **Velocity**, **Gravity**

5. EXAM SOURCE:
   - If exam name mentioned, add after explanation
   - Format: "Exam Source: [exam name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT AS VALID JSON:
{{
  "questions": [
    {{
      "question": "question text",
      "options": {{"A": "a", "B": "b", "C": "c", "D": "d", "E": "e"}},
      "correct_answer": "A",
      "explanation": "explanation text"
    }}
  ]
}}
"""

descriptive_physics = """You are an expert descriptive question creator for government exams specializing in Physics.

TASK: Create descriptive Physics questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test physics understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain physics concepts clearly
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include practical examples and applications
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: physics laws, formulas, principles

5. EXAM SOURCE:
   - If exam mentioned, add: "Exam Source: [name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT AS VALID JSON:
{{
  "questions": [
    {{
      "question": "question",
      "answer": "bullet answer",
      "explanation": "explanation"
    }}
  ]
}}
"""

# Create Chemistry-specific prompts
mcq_chemistry = """You are an expert MCQ creator for government exams specializing in Chemistry.

TASK: Create Chemistry MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant chemistry options
   - Make options appropriately challenging
   - Test chemistry understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain chemistry concepts clearly
   - Questions should be crystal clear
   - Make chemistry accessible

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Include reactions and properties
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: chemical elements, compounds, reactions
   - Examples: **Valency**, **Oxidation**, **pH**, **Catalyst**

5. EXAM SOURCE:
   - If exam name mentioned, add after explanation
   - Format: "Exam Source: [exam name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT AS VALID JSON:
{{
  "questions": [
    {{
      "question": "question text",
      "options": {{"A": "a", "B": "b", "C": "c", "D": "d", "E": "e"}},
      "correct_answer": "A",
      "explanation": "explanation text"
    }}
  ]
}}
"""

descriptive_chemistry = """You are an expert descriptive question creator for government exams specializing in Chemistry.

TASK: Create descriptive Chemistry questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test chemistry understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain chemistry concepts clearly
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include reactions and chemical principles
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: chemical concepts, reactions, elements

5. EXAM SOURCE:
   - If exam mentioned, add: "Exam Source: [name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT AS VALID JSON:
{{
  "questions": [
    {{
      "question": "question",
      "answer": "bullet answer",
      "explanation": "explanation"
    }}
  ]
}}
"""

# Create Biology-specific prompts
mcq_biology = """You are an expert MCQ creator for government exams specializing in Biology.

TASK: Create Biology MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant biology options
   - Make options appropriately challenging
   - Test biology understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain biology concepts clearly
   - Questions should be crystal clear
   - Make biology accessible

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Include biological processes and systems
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: biological terms, processes, organisms
   - Examples: **Photosynthesis**, **Respiration**, **DNA**, **Ecosystem**

5. EXAM SOURCE:
   - If exam name mentioned, add after explanation
   - Format: "Exam Source: [exam name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT AS VALID JSON:
{{
  "questions": [
    {{
      "question": "question text",
      "options": {{"A": "a", "B": "b", "C": "c", "D": "d", "E": "e"}},
      "correct_answer": "A",
      "explanation": "explanation text"
    }}
  ]
}}
"""

descriptive_biology = """You are an expert descriptive question creator for government exams specializing in Biology.

TASK: Create descriptive Biology questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test biology understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain biology concepts clearly
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include biological structures and processes
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: biological terms, organisms, systems

5. EXAM SOURCE:
   - If exam mentioned, add: "Exam Source: [name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT AS VALID JSON:
{{
  "questions": [
    {{
      "question": "question",
      "answer": "bullet answer",
      "explanation": "explanation"
    }}
  ]
}}
"""

# Dictionary of new prompts
new_prompts = {
    'pdf_to_mcq_physics': mcq_physics,
    'pdf_to_descriptive_physics': descriptive_physics,
    'pdf_to_mcq_chemistry': mcq_chemistry,
    'pdf_to_descriptive_chemistry': descriptive_chemistry,
    'pdf_to_mcq_biology': mcq_biology,
    'pdf_to_descriptive_biology': descriptive_biology,
}

print("Creating Physics, Chemistry, and Biology specific prompts...")
print("="*60)

created_count = 0
for source_url, prompt_content in new_prompts.items():
    try:
        # Check if prompt already exists
        existing = LLMPrompt.objects.filter(source_url=source_url).first()
        if existing:
            print("Already exists: " + source_url)
        else:
            # Determine prompt type
            prompt_type = 'mcq' if 'mcq' in source_url else 'descriptive'
            
            # Create new prompt
            prompt_obj = LLMPrompt(
                source_url=source_url,
                prompt_type=prompt_type,
                prompt_text=prompt_content,
                is_active=True
            )
            prompt_obj.save()
            print("CREATED: " + source_url)
            created_count += 1
    except Exception as e:
        print("ERROR creating " + source_url + ": " + str(e))

print("\n" + "="*60)
print("CREATED: " + str(created_count) + " new prompts")
print("="*60)
print("\nNew Science-Specific Prompts:")
print("- pdf_to_mcq_physics")
print("- pdf_to_descriptive_physics")
print("- pdf_to_mcq_chemistry")
print("- pdf_to_descriptive_chemistry")
print("- pdf_to_mcq_biology")
print("- pdf_to_descriptive_biology")
