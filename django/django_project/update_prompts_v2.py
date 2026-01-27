"""
Update all LLM prompts with enhanced requirements
"""

from genai.models import LLMPrompt

# MCQ Prompt for Polity
mcq_polity = """You are an expert MCQ creator for government exams (UPSC, State PSC, Railway, Bank exams).

TASK: Create MCQs from the provided content on Government and Constitution topics.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly (can rephrase for clarity)
   - If content has NO options, CREATE relevant options yourself
   - Make created options close enough to test understanding
   - Avoid options that are too obviously wrong

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Avoid difficult jargon where possible
   - Questions should be crystal clear
   - Everyone should understand what is being asked

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point (one point per line)
   - If explanation exists in content: rewrite it in simple language
   - If explanation does not exist: create a complete explanation
   - Explain WHY the correct answer is right
   - Explain WHY wrong options are wrong
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** to make important words bold in explanation
   - Bold: constitutional terms, articles, important dates, key names
   - Examples: **Constitution**, **Article 15**, **1950**, **Ambedkar**

5. EXAM SOURCE:
   - If content mentions exam name (Railway Group D 2016, UPSC 2019, etc)
   - Add after explanation: "Exam Source: [exam name and year]"

CONTENT: {content}

NUMBER OF QUESTIONS: {num_questions}
DIFFICULTY LEVEL: {difficulty}
CHAPTER: {chapter}

OUTPUT AS VALID JSON:
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
      "explanation": "Bullet explanation text"
    }}
  ]
}}
"""

# MCQ Prompt for Economics
mcq_economics = """You are an expert MCQ creator for government exams specializing in Economics.

TASK: Create Economics MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly (can rephrase for clarity)
   - If content has NO options, CREATE relevant options yourself
   - Make created options similar in style and length
   - Options should test real understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain economic concepts in simple terms
   - Questions should be crystal clear
   - Avoid unnecessary economic jargon

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point (one point per line)
   - If explanation exists: rewrite it in simple language
   - If explanation does not exist: create a complete explanation
   - Include real-world examples where helpful
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** to make important words bold in explanation
   - Bold: economic terms, policies, important concepts
   - Examples: **Inflation**, **GDP**, **Monetary Policy**

5. EXAM SOURCE:
   - If content mentions exam name, add after explanation
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
      "options": {{
        "A": "option A",
        "B": "option B",
        "C": "option C",
        "D": "option D",
        "E": "option E"
      }},
      "correct_answer": "A",
      "explanation": "Bullet points explanation"
    }}
  ]
}}
"""

# MCQ Prompt for History
mcq_history = """You are an expert MCQ creator for government exams specializing in History.

TASK: Create History MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant and plausible options
   - Make options close enough to test understanding
   - Avoid obviously wrong options

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain historical context clearly
   - Questions should be crystal clear
   - Make history concepts accessible

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation with historical context
   - Include significance and importance
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words in explanation
   - Bold: historical events, dates, important names, movements
   - Examples: **1857 Revolt**, **Ashoka**, **Mughal Empire**

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

# MCQ Prompt for Geography
mcq_geography = """You are an expert MCQ creator for government exams specializing in Geography.

TASK: Create Geography MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant geographic options
   - Make options appropriately challenging
   - Test real geographical understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain geographic concepts clearly
   - Questions should be crystal clear
   - Avoid unnecessary technical jargon

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Include geographical significance
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: locations, geographic terms, climate concepts
   - Examples: **Himalayas**, **Monsoon**, **Western Ghats**

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

# MCQ Prompt for Computer
mcq_computer = """You are an expert MCQ creator for government exams specializing in Computer Science and IT.

TASK: Create Computer Science MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant IT options
   - Make options challenging but fair
   - Test understanding of concepts

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain technical concepts in simple terms
   - Questions should be crystal clear
   - Make technology accessible

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Include practical examples
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: technical terms, programming concepts, technologies
   - Examples: **Algorithm**, **Database**, **Cloud Computing**

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

# MCQ Prompt for Mathematics
mcq_mathematics = """You are an expert MCQ creator for government exams specializing in Mathematics.

TASK: Create Mathematics MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant math options
   - Make options include common mistakes
   - Test mathematical understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain math concepts clearly
   - Questions should be crystal clear
   - Make math accessible

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Show step-by-step approach
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: formulas, theorems, key concepts
   - Examples: **Pythagorean Theorem**, **Quadratic Equation**

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

# MCQ Prompt for Science
mcq_science = """You are an expert MCQ creator for government exams specializing in Science (Physics, Chemistry, Biology).

TASK: Create Science MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant science options
   - Make options appropriately challenging
   - Test scientific understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Explain science concepts in simple terms
   - Questions should be crystal clear
   - Make science accessible

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Include real-world applications
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: scientific terms, laws, principles
   - Examples: **Photosynthesis**, **Osmosis**, **Ecosystem**

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

# MCQ Prompt for English
mcq_english = """You are an expert MCQ creator for government exams specializing in English.

TASK: Create English MCQs from the provided content.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant English options
   - Make options challenging but fair
   - Test English understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Questions should be crystal clear
   - Everyone should understand the question

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Explain grammar or literary concepts
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: grammar terms, literary devices
   - Examples: **Adjective**, **Simile**, **Metaphor**

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

# MCQ Prompt for Other
mcq_other = """You are an expert MCQ creator for government exams.

TASK: Create MCQs from the provided content on various topics.

IMPORTANT REQUIREMENTS:

1. OPTIONS REQUIREMENT:
   - Create EXACTLY 5 options (A, B, C, D, E)
   - One option MUST be the correct answer
   - If content has options, USE them directly
   - If no options, CREATE relevant options
   - Make options appropriately challenging
   - Test real understanding

2. LANGUAGE QUALITY:
   - Use simple, easy to understand language
   - Questions should be crystal clear
   - Everyone should understand what is asked

3. EXPLANATION FORMAT:
   - Use bullet points for EVERY point
   - If explanation exists: rewrite in simple language
   - If not: create complete explanation
   - Make 3-5 bullet points per explanation

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words in explanation
   - Bold: key terms, important concepts

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

# Descriptive prompts
descriptive_polity = """You are an expert descriptive question creator for government exams.

TASK: Create descriptive questions about Government and Constitution topics.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test understanding, not just memorization
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Avoid difficult jargon
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: constitutional terms, articles, key concepts
   - Examples: **Preamble**, **Article 15**, **Rights**

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
      "question": "question text",
      "answer": "bullet point answer",
      "explanation": "explanation text"
    }}
  ]
}}
"""

descriptive_economics = """You are an expert descriptive question creator for government exams specializing in Economics.

TASK: Create descriptive Economics questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test understanding of economic concepts
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain concepts simply
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include real-world examples
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: economic terms, policies, concepts
   - Examples: **Inflation**, **GDP**, **Policy**

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

descriptive_history = """You are an expert descriptive question creator for government exams specializing in History.

TASK: Create descriptive History questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test historical understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain historical context clearly
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include historical significance
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: events, dates, names, movements
   - Examples: **1857 Revolt**, **Ashoka**, **Empire**

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

descriptive_geography = """You are an expert descriptive question creator for government exams specializing in Geography.

TASK: Create descriptive Geography questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test geographical understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain geographic concepts clearly
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include geographical significance
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: locations, geographic terms, climate concepts

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

descriptive_computer = """You are an expert descriptive question creator for government exams specializing in Computer Science and IT.

TASK: Create descriptive Computer Science questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test understanding of computing concepts
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain technical concepts simply
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include practical examples
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: technical terms, programming concepts, technologies

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

descriptive_mathematics = """You are an expert descriptive question creator for government exams specializing in Mathematics.

TASK: Create descriptive Mathematics questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test mathematical understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain math concepts clearly
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Show step-by-step approach
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: formulas, theorems, key concepts

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

descriptive_science = """You are an expert descriptive question creator for government exams specializing in Science (Physics, Chemistry, Biology).

TASK: Create descriptive Science questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test scientific understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Explain science concepts simply
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include real-world applications
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: scientific terms, laws, principles

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

descriptive_english = """You are an expert descriptive question creator for government exams specializing in English.

TASK: Create descriptive English questions.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test English understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Include examples
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words
   - Bold: grammar terms, literary devices

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

descriptive_other = """You are an expert descriptive question creator for government exams.

TASK: Create descriptive questions on various topics.

REQUIREMENTS:

1. QUESTION DESIGN:
   - Clear comprehensive questions needing detailed answers
   - Test understanding
   - Should be answerable in 150-250 words

2. LANGUAGE:
   - Use simple, easy to understand language
   - Questions should be crystal clear

3. ANSWER FORMAT:
   - Provide complete answer in bullet points
   - One key point per bullet line
   - If explanation exists: rewrite in simple language
   - If not: create complete answer
   - Make 5-8 bullet points

4. BOLD IMPORTANT WORDS:
   - Use **word** for important words

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

# MCQ Prompts dictionary
mcq_prompts = {
    'pdf_to_mcq_polity': mcq_polity,
    'pdf_to_mcq_economics': mcq_economics,
    'pdf_to_mcq_history': mcq_history,
    'pdf_to_mcq_geography': mcq_geography,
    'pdf_to_mcq_computer': mcq_computer,
    'pdf_to_mcq_mathematics': mcq_mathematics,
    'pdf_to_mcq_science': mcq_science,
    'pdf_to_mcq_english': mcq_english,
    'pdf_to_mcq_other': mcq_other,
}

# Descriptive Prompts dictionary
descriptive_prompts = {
    'pdf_to_descriptive_polity': descriptive_polity,
    'pdf_to_descriptive_economics': descriptive_economics,
    'pdf_to_descriptive_history': descriptive_history,
    'pdf_to_descriptive_geography': descriptive_geography,
    'pdf_to_descriptive_computer': descriptive_computer,
    'pdf_to_descriptive_mathematics': descriptive_mathematics,
    'pdf_to_descriptive_science': descriptive_science,
    'pdf_to_descriptive_english': descriptive_english,
    'pdf_to_descriptive_other': descriptive_other,
}

# Update all MCQ prompts
print("Updating MCQ prompts...")
for source_url, prompt_content in mcq_prompts.items():
    try:
        prompt_obj = LLMPrompt.objects.get(source_url=source_url)
        prompt_obj.prompt_text = prompt_content
        prompt_obj.save()
        print("OK: " + source_url)
    except LLMPrompt.DoesNotExist:
        print("NOT FOUND: " + source_url)

# Update all Descriptive prompts
print("\nUpdating Descriptive prompts...")
for source_url, prompt_content in descriptive_prompts.items():
    try:
        prompt_obj = LLMPrompt.objects.get(source_url=source_url)
        prompt_obj.prompt_text = prompt_content
        prompt_obj.save()
        print("OK: " + source_url)
    except LLMPrompt.DoesNotExist:
        print("NOT FOUND: " + source_url)

print("\n========================================")
print("ALL PROMPTS UPDATED")
print("========================================")
