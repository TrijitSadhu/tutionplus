"""
Django Management Command to Create Missing Prompts for All Subjects
Run with: python manage.py shell < create_missing_prompts.py
"""

from genai.models import LLMPrompt, PDFUpload

# Get all unique subjects
subjects = list(PDFUpload.objects.values_list('subject', flat=True).distinct())
subjects = sorted(list(set(subjects)))

print("\n" + "="*80)
print("CREATING MISSING PROMPTS FOR ALL SUBJECTS")
print("="*80)

# Define prompts for each subject
PROMPTS = {
    'polity': {
        'mcq': """You are an expert Indian Politics and Constitution specialist. Generate high-quality multiple choice questions for competitive exams like UPSC.

Content to analyze:
{content}

Generate {num_questions} MCQ questions. Questions should test understanding of Indian politics, constitution, and governance.
Difficulty: {difficulty}

Return ONLY valid JSON (no markdown, no explanations):
{{
    "questions": [
        {{
            "question": "Question text",
            "option_1": "Option A",
            "option_2": "Option B",
            "option_3": "Option C",
            "option_4": "Option D",
            "correct_answer": 1,
            "explanation": "Why this answer is correct",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert Indian Politics and Constitution specialist.

Content to analyze:
{content}

Generate {num_questions} descriptive questions with comprehensive answers on Indian politics and constitution.
Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Descriptive question",
            "answer": "Comprehensive answer with key points",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'economics': {
        'mcq': """You are an expert Economics specialist. Generate {num_questions} MCQ questions based on:
{content}

Questions should test understanding of economic concepts, policies, and theories.
Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "correct_answer": 1,
            "explanation": "Explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an expert Economics specialist. Generate {num_questions} descriptive questions with detailed answers based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "answer": "Answer with examples and analysis",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'history': {
        'mcq': """You are a history expert. Generate {num_questions} MCQ questions based on:
{content}

Questions should test knowledge of historical events, dates, figures, and facts.
Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "correct_answer": 1,
            "explanation": "Explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a history expert. Generate {num_questions} descriptive questions with detailed answers based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "answer": "Answer with historical context and details",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'geography': {
        'mcq': """You are a geography expert. Generate {num_questions} MCQ questions based on:
{content}

Questions should test knowledge of geography, locations, climates, and geographical features.
Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "correct_answer": 1,
            "explanation": "Explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a geography expert. Generate {num_questions} descriptive questions with detailed answers based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "answer": "Answer with geographical details and facts",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'computer': {
        'mcq': """You are a computer science expert. Generate {num_questions} MCQ questions based on:
{content}

Questions should test understanding of programming, algorithms, data structures, and computer science concepts.
Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "correct_answer": 1,
            "explanation": "Explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a computer science expert. Generate {num_questions} descriptive questions with detailed answers based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "answer": "Answer with code examples or detailed explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'mathematics': {
        'mcq': """You are a mathematics expert. Generate {num_questions} MCQ questions based on:
{content}

Questions should test mathematical problem-solving and concept understanding.
Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "correct_answer": 1,
            "explanation": "Solution with steps",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a mathematics expert. Generate {num_questions} descriptive questions with detailed solutions based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "answer": "Answer with step-by-step solution",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'science': {
        'mcq': """You are a science expert. Generate {num_questions} MCQ questions based on:
{content}

Questions should test understanding of scientific concepts, laws, and phenomena.
Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "correct_answer": 1,
            "explanation": "Scientific explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are a science expert. Generate {num_questions} descriptive questions with detailed answers based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "answer": "Answer with scientific details and examples",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'english': {
        'mcq': """You are an English language expert. Generate {num_questions} MCQ questions based on:
{content}

Questions should test understanding of grammar, vocabulary, reading comprehension, and language skills.
Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "correct_answer": 1,
            "explanation": "Explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """You are an English language expert. Generate {num_questions} descriptive questions with detailed answers based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "answer": "Answer with detailed explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    },
    'other': {
        'mcq': """Generate {num_questions} MCQ questions based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "option_1": "A",
            "option_2": "B",
            "option_3": "C",
            "option_4": "D",
            "correct_answer": 1,
            "explanation": "Explanation",
            "difficulty": "{difficulty}"
        }}
    ]
}}""",
        'descriptive': """Generate {num_questions} descriptive questions with detailed answers based on:
{content}

Difficulty: {difficulty}

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Question",
            "answer": "Answer",
            "difficulty": "{difficulty}"
        }}
    ]
}}"""
    }
}

created_count = 0
skipped_count = 0

for subject in subjects:
    for prompt_type in ['mcq', 'descriptive']:
        source_url = f'pdf_to_{prompt_type}_{subject}'
        
        # Check if exists
        exists = LLMPrompt.objects.filter(source_url=source_url, prompt_type=prompt_type).exists()
        
        if exists:
            print(f"  ✓ SKIP: {source_url}")
            skipped_count += 1
        else:
            prompt_text = PROMPTS.get(subject, PROMPTS['other']).get(prompt_type, "")
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
