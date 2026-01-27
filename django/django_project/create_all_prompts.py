from genai.models import LLMPrompt

# Define prompts for each subject
PROMPTS = {
    'polity': {
        'mcq': """You are an expert Indian Politics and Constitution specialist creating MCQs for government competitive exams (UPSC, Banking, Railway, SSC).

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly (you can rephrase for clarity)
3. If options DON'T exist in content → Create 4 plausible alternatives that are:
   - Close to the correct answer (to confuse students)
   - Logically relevant to the topic
   - Different from the correct answer

LANGUAGE RULES:
- Use lucid, easy-to-understand language
- Avoid complex jargon
- Make each option distinct and clear

EXPLANATION RULES:
- ALWAYS provide explanation in bullet points (•)
- If explanation exists in content → Simplify it to easy language
- If explanation doesn't exist → Create one yourself
- Make important exam words BOLD using **word**
- If exam source mentioned (e.g., "Railway 2016", "SSC CGL 2018") → Include it after explanation
- Format: • Key point 1
         • Key point 2
         • Source: Railway Group D 2016 (if mentioned)

DIFFICULTY: {difficulty}

Return ONLY valid JSON (no markdown):
{{
    "questions": [
        {{
            "question": "Clear, unambiguous question",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• First point\\n• Second point\\n• Third point\\n• Source: Exam name if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert Indian Politics and Constitution specialist creating descriptive answers for government competitive exams.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed answers following THESE RULES:

LANGUAGE RULES:
- Use lucid, easy-to-understand language
- Avoid complex jargon
- Make content accessible to all students

ANSWER FORMAT:
- Structure answers with clear points (use bullet format)
- Make important exam words BOLD using **word**
- If source information available (e.g., "As per Constitution Article X") → Include it
- Keep explanations detailed but simple

ANSWER RULES:
- If explanation exists in content → Use and simplify to easy language
- If explanation doesn't exist → Create comprehensive one yourself
- Include real examples where relevant
- Reference exam sources if mentioned in content

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive question",
            "answer": "Comprehensive answer with bullet points\\n• Key point 1\\n• Key point 2\\n• Example or reference if applicable",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'economics': {
        'mcq': """You are an expert Economics specialist creating MCQs for government competitive exams (UPSC, Banking, Railway, SSC).

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly (you can rephrase for clarity)
3. If options DON'T exist in content → Create 4 plausible alternatives that are:
   - Close to the correct answer (to confuse students)
   - Logically relevant to economic concepts
   - Different from the correct answer

LANGUAGE RULES:
- Use lucid, easy-to-understand language
- Avoid complex economic jargon without explanation
- Make each option distinct and clear

EXPLANATION RULES:
- ALWAYS provide explanation in bullet points (•)
- If explanation exists in content → Simplify it to easy language
- If explanation doesn't exist → Create one yourself
- Make important exam words BOLD using **word**
- If exam source mentioned → Include it after explanation
- Format: • Key point
         • Source: Exam name if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Clear economic question",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• Point 1\\n• Point 2\\n• Source: Exam if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert Economics specialist creating descriptive answers for government competitive exams.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed answers following THESE RULES:

LANGUAGE RULES:
- Use lucid, easy-to-understand language
- Simplify economic concepts
- Make content accessible

ANSWER FORMAT:
- Use bullet points for clarity
- Make important words BOLD using **word**
- Include real examples and statistics
- Reference sources if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive economics question",
            "answer": "Detailed answer with bullet points\\n• Key point\\n• Example\\n• Statistics if relevant",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'history': {
        'mcq': """You are a history expert creating MCQs for government competitive exams (UPSC, Railway, SSC).

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly
3. If options DON'T exist → Create 4 plausible alternatives that are:
   - Close/confusing (similar dates, similar figures, similar events)
   - Logically relevant to history
   - Different from correct answer

LANGUAGE RULES:
- Use clear, simple language
- Avoid overly complex historical terminology
- Make all options distinct

EXPLANATION RULES:
- ALWAYS use bullet points (•)
- If explanation in content → Simplify it
- If not → Create one yourself
- Bold important historical figures, dates, events using **word**
- Include exam source if mentioned
- Format: • Historical fact
         • Key detail
         • Source: Exam name if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Historical question",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• Historical fact\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a history expert creating descriptive answers for government competitive exams.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed answers:

LANGUAGE RULES:
- Use simple, engaging language
- Make history easy to understand
- Avoid unnecessary jargon

ANSWER FORMAT:
- Use bullet points
- Bold important figures, dates, events using **word**
- Include timeline if relevant
- Reference sources

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive history question",
            "answer": "Answer with bullet points\\n• Event/Date\\n• Significance\\n• Impact\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'geography': {
        'mcq': """You are a geography expert creating MCQs for government competitive exams (UPSC, Railway, SSC).

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly
3. If options DON'T exist → Create 4 plausible alternatives that are:
   - Close/confusing (similar locations, similar climates, similar features)
   - Geographically relevant
   - Different from correct answer

LANGUAGE RULES:
- Use clear, simple language
- Make geographical concepts easy to understand
- Make all options distinct and clear

EXPLANATION RULES:
- ALWAYS use bullet points (•)
- If explanation in content → Simplify it
- If not → Create one yourself
- Bold important geographical terms using **word**
- Include exam source if mentioned
- Format: • Geographical fact
         • Key detail
         • Source if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Geographical question",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• Geographical fact\\n• Key detail\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a geography expert creating descriptive answers for government competitive exams.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed answers:

LANGUAGE RULES:
- Use simple, clear language
- Make geography concepts accessible
- Include maps/directions where relevant

ANSWER FORMAT:
- Use bullet points
- Bold important terms using **word**
- Include location details
- Reference sources

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive geography question",
            "answer": "Answer with bullet points\\n• Location\\n• Features\\n• Significance\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'computer': {
        'mcq': """You are a computer science expert creating MCQs for government competitive exams (UPSC, SSC, Railway).

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly
3. If options DON'T exist → Create 4 plausible alternatives that are:
   - Close/similar-sounding (similar concepts, similar commands)
   - Logically relevant to CS
   - Different from correct answer

LANGUAGE RULES:
- Use clear, simple language
- Explain technical terms when needed
- Make all options distinct

EXPLANATION RULES:
- ALWAYS use bullet points (•)
- If explanation in content → Simplify it
- If not → Create one yourself
- Bold important CS terms using **word**
- Include code examples if relevant
- Include exam source if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "CS question",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• Concept explanation\\n• Code/Example if relevant\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a computer science expert creating descriptive answers for government competitive exams.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed answers:

LANGUAGE RULES:
- Use simple, clear language
- Explain technical terms
- Include code examples where helpful

ANSWER FORMAT:
- Use bullet points
- Bold important terms using **word**
- Include examples/code snippets
- Reference sources

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive CS question",
            "answer": "Answer with bullet points\\n• Definition\\n• Example/Code\\n• Use case\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'mathematics': {
        'mcq': """You are a mathematics expert creating MCQs for government competitive exams (UPSC, SSC, Railway, Banking).

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly
3. If options DON'T exist → Create 4 plausible alternatives that are:
   - Close/confusing (common calculation mistakes)
   - Logically relevant
   - Different from correct answer

LANGUAGE RULES:
- Use clear, simple language
- Clearly state what is given and what is asked
- Make all options distinct

EXPLANATION RULES:
- ALWAYS use bullet points (•)
- If explanation in content → Simplify it
- If not → Create step-by-step solution
- Bold important formulas/concepts using **word**
- Include formula used
- Include exam source if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Math question with given values",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• Step 1\\n• Step 2\\n• Formula: **formula here**\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a mathematics expert creating descriptive answers for government competitive exams.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed solutions:

LANGUAGE RULES:
- Use clear, step-by-step language
- Make solutions easy to follow
- Include formulas clearly

SOLUTION FORMAT:
- Use bullet points for steps
- Bold formulas using **word**
- Show working/calculations
- Reference sources

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive math question",
            "answer": "Step-by-step solution\\n• Given\\n• Formula: **formula**\\n• Calculation\\n• Answer\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'science': {
        'mcq': """You are a science expert creating MCQs for government competitive exams (UPSC, Railway, SSC).

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly
3. If options DON'T exist → Create 4 plausible alternatives that are:
   - Close/confusing (similar scientific concepts)
   - Logically relevant
   - Different from correct answer

LANGUAGE RULES:
- Use clear, simple language
- Explain scientific terms when needed
- Make all options distinct

EXPLANATION RULES:
- ALWAYS use bullet points (•)
- If explanation in content → Simplify it
- If not → Create one yourself
- Bold important scientific terms using **word**
- Include real-world example if relevant
- Include exam source if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Science question",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• Scientific fact\\n• Example\\n• Key concept\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a science expert creating descriptive answers for government competitive exams.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed answers:

LANGUAGE RULES:
- Use simple, clear language
- Explain all scientific terms
- Include real-world examples

ANSWER FORMAT:
- Use bullet points
- Bold important terms using **word**
- Include examples/diagrams description
- Reference sources

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive science question",
            "answer": "Answer with bullet points\\n• Definition\\n• How it works\\n• Example\\n• Real-world application\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'english': {
        'mcq': """You are an English language expert creating MCQs for government competitive exams (UPSC, Banking, Railway, SSC).

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly
3. If options DON'T exist → Create 4 plausible alternatives that are:
   - Close/confusing (similar meanings, similar grammar patterns)
   - Logically relevant
   - Different from correct answer

LANGUAGE RULES:
- Use clear, simple language
- Make all options distinct and grammatically correct
- Avoid ambiguity

EXPLANATION RULES:
- ALWAYS use bullet points (•)
- If explanation in content → Simplify it
- If not → Create one yourself
- Bold important grammar/vocabulary using **word**
- Include usage example if relevant
- Include exam source if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "English question (grammar/vocabulary)",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• Grammar rule or word meaning\\n• Usage example\\n• Why others are wrong\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an English language expert creating descriptive answers for government competitive exams.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed answers:

LANGUAGE RULES:
- Use clear, correct English
- Provide detailed explanations
- Include examples

ANSWER FORMAT:
- Use bullet points for clarity
- Bold important grammar/words using **word**
- Include examples/sentences
- Reference sources

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive English question",
            "answer": "Answer with bullet points\\n• Rule/Definition\\n• Example sentence\\n• Exception if any\\n• Common mistakes\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'other': {
        'mcq': """You are creating MCQs for government competitive exams for general content.

Content to analyze:
{content}

Generate {num_questions} MCQ questions following THESE RULES STRICTLY:

RULES FOR OPTIONS:
1. Create 5 options (A, B, C, D, E) for EVERY question
2. If options exist in content → Use them directly
3. If options DON'T exist → Create 4 plausible alternatives that are:
   - Close/confusing (similar to correct answer)
   - Logically relevant
   - Different from correct answer

LANGUAGE RULES:
- Use clear, simple, lucid language
- Make all options distinct and clear
- Avoid ambiguity

EXPLANATION RULES:
- ALWAYS use bullet points (•)
- If explanation in content → Simplify it
- If not → Create one yourself
- Bold important terms using **word**
- Include relevant details
- Include exam source if mentioned

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Clear question",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "option_5": "Option E",
            "correct_answer": 1,
            "explanation": "• Key point\\n• Detail\\n• Why correct\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are creating descriptive answers for government competitive exams for general content.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with detailed answers:

LANGUAGE RULES:
- Use simple, clear, lucid language
- Make content easy to understand
- Be comprehensive yet simple

ANSWER FORMAT:
- Use bullet points
- Bold important terms using **word**
- Include relevant details and examples
- Reference sources

DIFFICULTY: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive question",
            "answer": "Answer with bullet points\\n• Main point\\n• Details\\n• Example\\n• Conclusion\\n• Source if mentioned",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    }
}

print("\n" + "="*80)
print("CREATING PROMPTS FOR ALL SUBJECTS")
print("="*80 + "\n")

created_count = 0
skipped_count = 0

for subject in PROMPTS.keys():
    for prompt_type in ['mcq', 'descriptive']:
        source_url = f'pdf_to_{prompt_type}_{subject}'
        
        exists = LLMPrompt.objects.filter(source_url=source_url, prompt_type=prompt_type).exists()
        
        if exists:
            print(f"  ✓ SKIP: {source_url}")
            skipped_count += 1
        else:
            prompt_text = PROMPTS[subject][prompt_type]
            LLMPrompt.objects.create(
                source_url=source_url,
                prompt_type=prompt_type,
                prompt_text=prompt_text,
                is_default=False,
                is_active=True
            )
            print(f"  ✅ CREATED: {source_url}")
            created_count += 1

print("\n" + "="*80)
print(f"SUMMARY: Created {created_count} | Skipped {skipped_count}")
print("="*80 + "\n")

# List all created prompts
print("All subject-specific prompts:")
all_prompts = LLMPrompt.objects.filter(source_url__startswith='pdf_to_').order_by('source_url')
for p in all_prompts:
    print(f"  ✓ {p.source_url}")
print()
