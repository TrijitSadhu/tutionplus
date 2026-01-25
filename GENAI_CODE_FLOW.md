"""
GenAI System - Code Flow Visualization

This file shows exactly what happens when you use each GenAI feature
"""

# ============================================================================
# FLOW 1: PDF UPLOAD & PROCESSING
# ============================================================================

FLOW_1 = """
┌─────────────────────────────────────────────────────────────────┐
│ FLOW 1: PDF UPLOAD & MCQ GENERATION                             │
└─────────────────────────────────────────────────────────────────┘

USER ACTION:
─────────────
Admin Panel → PDFUpload → Add PDF Upload
  Title: "Biology_Chapter_5"
  Subject: "biology"
  File: biology_chapter_5.pdf (35 pages, 5MB)
  
                    ↓↓↓

WHAT HAPPENS BEHIND THE SCENES:
────────────────────────────────

1. DATABASE LEVEL
   └─ genai/models.py → PDFUpload model
      ├─ title = "Biology_Chapter_5"
      ├─ subject = "biology"
      ├─ pdf_file = Saved to genai/pdfs/2026/01/25/
      ├─ status = "uploaded" → "processing"
      ├─ uploaded_at = 2026-01-25 14:30:22
      └─ uploaded_by = <Current User>

2. FILE PROCESSING
   └─ genai/tasks/pdf_processor.py → process_subject_pdf()
      ├─ Load PDF file from disk
      ├─ Using PyPDF2 library:
      │   ├─ reader = PdfReader("biology_chapter_5.pdf")
      │   ├─ total_pages = len(reader.pages)  # 35
      │   └─ extracted_text = ""
      │
      ├─ For each page in PDF:
      │   └─ extracted_text += page.extract_text()
      │
      └─ Save to database:
         └─ pdf.extracted_text = "Cell structure is..."
            pdf.total_pages = 35
            pdf.save()

3. LLM PROCESSING
   └─ genai/utils/llm_provider.py → get_llm_provider()
      │
      ├─ TRY: GeminiProvider
      │   └─ import google.generativeai as genai
      │   └─ genai.configure(api_key=GEMINI_API_KEY)
      │   └─ client = genai.GenerativeModel('gemini-pro')
      │   └─ ✓ SUCCESS
      │
      └─ Generate MCQs:
         └─ prompt = """
              Extract key concepts from this biology text and generate
              10 multiple choice questions with 4 options each.
              Format as JSON.
              
              Text: [extracted_text from PDF]
            """
         └─ response = client.generate_content(prompt)
         └─ Parse response as JSON
         └─ Get 10 MCQs with options

4. TASK TRACKING
   └─ genai/models.py → ProcessingTask model
      ├─ task_type = "pdf_processing"
      ├─ input_data = {
      │     "pdf_id": 5,
      │     "subject": "biology",
      │     "pages": 35,
      │     "file_size": "5.2 MB"
      │  }
      ├─ status = "processing" → "completed"
      ├─ output_data = {
      │     "questions_generated": 10,
      │     "quality_score": 0.94,
      │     "extraction_time": 2.5,
      │     "llm_time": 8.3
      │  }
      └─ duration_seconds = 10.8

5. ADMIN DISPLAY
   └─ genai/admin.py → PDFUploadAdmin
      ├─ Displays status_badge = "✓ COMPLETED" (GREEN)
      ├─ Shows total_pages = 35
      ├─ Shows extracted_text in readonly field
      ├─ Allows export to CSV/JSON
      └─ Link to ProcessingTask details

RESULT:
───────
✓ 35-page PDF fully processed in ~10 seconds
✓ 10 quality MCQs generated
✓ All tracked and auditable
✓ Ready to export and use
"""

print(FLOW_1)


# ============================================================================
# FLOW 2: CURRENT AFFAIRS GENERATION
# ============================================================================

FLOW_2 = """
┌─────────────────────────────────────────────────────────────────┐
│ FLOW 2: CURRENT AFFAIRS MCQ GENERATION                          │
└─────────────────────────────────────────────────────────────────┘

USER ACTION:
─────────────
Admin Panel → CurrentAffairs → Add
  Topic: "Union Budget 2026"
  Source URL: https://news.example.com/budget-2026 (optional)

                    ↓↓↓

WHAT HAPPENS:
──────────────

1. CREATE DATABASE ENTRY
   └─ genai/models.py → CurrentAffairsGeneration
      ├─ topic = "Union Budget 2026"
      ├─ source_url = "https://news.example.com/budget-2026"
      ├─ status = "pending"
      ├─ created_at = 2026-01-25 14:35:00
      └─ generated_mcq = NULL (not yet)

2. FETCH SOURCE CONTENT (Optional)
   └─ genai/tasks/current_affairs.py
      ├─ If source_url provided:
      │   ├─ requests.get(source_url)
      │   ├─ BeautifulSoup parse HTML
      │   ├─ Extract main article content
      │   └─ content = "Union Budget 2026 allocates..."
      │
      └─ If no URL: Use topic as context

3. CALL LLM
   └─ genai/utils/llm_provider.py
      ├─ provider = get_llm_provider()  # Gemini or OpenAI
      │
      ├─ MCQ Generation:
      │   prompt = """
      │     Generate 5 multiple choice questions about:
      │     "Union Budget 2026"
      │     
      │     Requirements:
      │     - Suitable for competitive exams
      │     - 4 options per question
      │     - 1 correct answer
      │     - Format as JSON
      │     
      │     Return JSON with structure:
      │     {
      │       "mcqs": [
      │         {
      │           "id": 1,
      │           "question": "What was...",
      │           "option_a": "...",
      │           "option_b": "...",
      │           "option_c": "...",
      │           "option_d": "...",
      │           "correct_answer": "A"
      │         }
      │       ]
      │     }
      │   """
      │   └─ response = provider.generate_json(prompt)
      │
      └─ Descriptive Answer:
         prompt = """
           Write a detailed explanation of Union Budget 2026.
           Include:
           - Key allocations
           - Major announcements
           - Impact on economy
           - Suitable for students
         """
         └─ response = provider.generate(prompt)

4. SAVE RESULTS
   └─ Update database:
      ├─ generated_mcq = [JSON MCQ data]
      ├─ generated_descriptive = "Union Budget 2026 is..."
      ├─ status = "completed"
      ├─ processed_at = 2026-01-25 14:35:12
      └─ error_message = NULL

5. ADMIN DISPLAY
   └─ genai/admin.py → CurrentAffairsGenerationAdmin
      ├─ Topic badge showing status
      ├─ Collapsible section showing generated MCQs
      ├─ Collapsible section showing descriptive answer
      ├─ Copy buttons for easy export
      └─ Bulk action: "Generate MCQ" for multiple entries

RESULT:
───────
✓ 5 MCQs on "Union Budget 2026" auto-generated
✓ Full descriptive answer provided
✓ All content in JSON format (easy to parse)
✓ Ready to push to frontend or MCQ database
"""

print(FLOW_2)


# ============================================================================
# FLOW 3: MATH PROBLEM CONVERSION
# ============================================================================

FLOW_3 = """
┌─────────────────────────────────────────────────────────────────┐
│ FLOW 3: MATH PROBLEM LaTeX CONVERSION & MCQ GENERATION          │
└─────────────────────────────────────────────────────────────────┘

USER ACTION:
─────────────
Admin Panel → Math Problems → Add
  Problem: "Solve for x: 2x² + 5x - 3 = 0"
  Difficulty: "medium"

                    ↓↓↓

WHAT HAPPENS:
──────────────

1. STORE PROBLEM
   └─ genai/models.py → MathProblemGeneration
      ├─ problem_statement = "Solve for x: 2x² + 5x - 3 = 0"
      ├─ difficulty = "medium"
      ├─ status = "pending"
      └─ latex_formula = NULL (will be filled)

2. CONVERT TO LaTeX
   └─ genai/tasks/math_processor.py
      ├─ Extract mathematical expression
      ├─ Convert to LaTeX format:
      │   "2x² + 5x - 3 = 0"
      │   ↓
      │   "$2x^2 + 5x - 3 = 0$"
      │
      ├─ For complex expressions:
      │   prompt = """
      │     Convert this to proper LaTeX format:
      │     [expression]
      │     
      │     Return only the LaTeX, wrapped in $ symbols.
      │     Example: $\\frac{1}{2}x^2 + 3x - 5$
      │   """
      │
      └─ Save to database:
         └─ latex_formula = "$2x^2 + 5x - 3 = 0$"

3. GENERATE MCQ VERSION
   └─ genai/utils/llm_provider.py
      └─ prompt = """
           Create a multiple choice question from this math problem:
           
           Original: Solve for x: 2x² + 5x - 3 = 0
           
           Generate 4 plausible options (one correct, three distractors):
           
           Return JSON:
           {
             "question": "Find the roots of...",
             "option_a": "x = -3, x = 0.5",
             "option_b": "x = 1, x = -2",
             "option_c": "x = 3, x = -0.5",
             "option_d": "x = 2, x = -1",
             "correct": "A",
             "solution_steps": "Using quadratic formula..."
           }
         """
      └─ response = provider.generate_json(prompt)

4. SAVE ALL VERSIONS
   └─ Update database:
      ├─ latex_formula = "$2x^2 + 5x - 3 = 0$"
      ├─ generated_mcq_version = [MCQ JSON]
      ├─ status = "completed"
      └─ difficulty = "medium"

5. ADMIN DISPLAY
   └─ genai/admin.py → MathProblemGenerationAdmin
      ├─ Show original problem
      ├─ Display LaTeX formatted (renders properly)
      ├─ Show MCQ version with 4 options
      ├─ Difficulty color-coded
      └─ Export to test/worksheet

RESULT:
───────
✓ Mathematical expression properly formatted
✓ LaTeX version: $2x^2 + 5x - 3 = 0$ (renders beautifully)
✓ MCQ version with 4 options
✓ Difficulty level assigned
✓ Ready for use in tests/worksheets
"""

print(FLOW_3)


# ============================================================================
# FLOW 4: LLM PROVIDER FALLBACK
# ============================================================================

FLOW_4 = """
┌─────────────────────────────────────────────────────────────────┐
│ FLOW 4: LLM PROVIDER SELECTION & FALLBACK                       │
└─────────────────────────────────────────────────────────────────┘

WHEN YOU TRIGGER ANY GENAI OPERATION:
──────────────────────────────────────

User triggers task
    ↓
Load genai/config.py
    ├─ DEFAULT_LLM_PROVIDER = "gemini"
    ├─ GEMINI_API_KEY = "AIzaSy..."
    └─ OPENAI_API_KEY = "sk-..."
    ↓
Call get_llm_provider()
    ├─ Check DEFAULT_LLM_PROVIDER = "gemini"
    ├─ Try initialize GeminiProvider
    │   ├─ import google.generativeai as genai
    │   │   └─ Success? ✓ Continue
    │   │      Fail? (Python < 3.8) → Go to step 4
    │   │
    │   ├─ genai.configure(api_key=GEMINI_API_KEY)
    │   │   └─ Success? ✓ Continue
    │   │      Fail? (Invalid key) → Go to step 4
    │   │
    │   └─ Test connection
    │       └─ Success? ✓ Return GeminiProvider
    │          Fail? → Go to step 4
    │
    ├─ [STEP 4] Try OpenAI Fallback
    │   ├─ import openai
    │   │   └─ Success? ✓ Continue
    │   │      Fail? → Return error
    │   │
    │   ├─ openai.api_key = OPENAI_API_KEY
    │   │   └─ Success? ✓ Continue
    │   │      Fail? → Return error
    │   │
    │   └─ Return OpenAIProvider
    │
    └─ Use selected provider for request

CURRENT SYSTEM STATUS:
──────────────────────
✓ Python 3.11 (supports Gemini)
✓ google-generativeai library installed
✓ GEMINI_API_KEY available
✓ OPENAI_API_KEY available (backup)

TYPICAL BEHAVIOR:
─────────────────
Scenario 1: Gemini working
    └─ Use Gemini (faster, no cost limit)
    
Scenario 2: Gemini API quota exceeded
    └─ Fall back to OpenAI (reliable)
    
Scenario 3: Network issue
    └─ Retry logic kicks in
    └─ Fall back after 3 retries
    
Scenario 4: Both unavailable
    └─ Use MockProvider (for testing)
    └─ Return dummy data
    
All logged in: ProcessingTask model
    └─ Tracks which provider was used
    └─ Tracks success/failure
    └─ Tracks timing
"""

print(FLOW_4)


# ============================================================================
# COMPLETE END-TO-END EXAMPLE
# ============================================================================

COMPLETE_EXAMPLE = """
┌─────────────────────────────────────────────────────────────────┐
│ COMPLETE EXAMPLE: Upload PDF → Generate MCQs → Use in Test      │
└─────────────────────────────────────────────────────────────────┘

TIMELINE:
─────────

9:00 AM - Teacher uploads textbook PDF
──────────────────────────────────────
Admin → GenAI → PDF Uploads → Add
  Title: "Physics - Chapter 3 - Motion"
  Subject: physics
  File: physics_chapter3.pdf (42 pages, 8MB)
  Click SAVE

User sees: Status = "⏳ Uploading..."
System action:
  1. Validates PDF format
  2. Creates PDFUpload record
  3. Saves file to: genai/pdfs/2026/01/25/physics_chapter3.pdf
  4. Sets status = "processing"

9:02 AM - Automatic processing starts
────────────────────────────────────
System (genai/tasks/pdf_processor.py):
  1. Load PDF from disk
  2. Extract text from all 42 pages
     └─ "Chapter 3: Motion
         Newton's Laws of Motion...
         F = ma
         ... [2000+ lines of text]"
  3. Send to LLM with prompt:
     "Generate 15 multiple choice questions about Motion.
      Use the provided text.
      Format as JSON with 4 options each."
  4. Parse JSON response
  5. Save to database:
     ├─ pdf.extracted_text = "[full chapter text]"
     ├─ pdf.total_pages = 42
     ├─ pdf.status = "completed"
     └─ Update ProcessingTask record

9:02:45 AM - Processing complete (45 seconds)
─────────────────────────────────────────
User refreshes admin page
Sees: Status = "✓ Completed" (GREEN)
      Total Pages = 42
      Extracted Text = [full text visible]
      Can now copy MCQs or export

User exports MCQs as JSON:
  [
    {
      "id": 1,
      "question": "What is Newton's second law?",
      "options": [
        "F = ma",
        "F = m²a",
        "F = m/a",
        "F = a/m"
      ],
      "answer": "A"
    },
    ...
  ]

9:05 AM - MCQs imported to main database
──────────────────────────────────────
Admin → Bank → MCQ → Bulk Import
  Subject: Physics
  Chapter: 3
  [Paste exported JSON]
  IMPORT

System creates 15 MCQ records in bank_mcq table

9:10 AM - Test published
───────────────────
Teacher creates test:
  Admin → Bank → Test → Add
    Name: "Physics Chapter 3 - Motion"
    Questions: Select from MCQ (15 auto-generated)
    Publish: YES

9:15 AM - Students take test
─────────────────────────
Students: https://tutionplus.com/test/physics-ch3/
  └─ Answer 15 questions on Motion
  └─ See instant results
  └─ Get performance analysis

10:00 AM - Teacher reviews analytics
──────────────────────────────────
Admin → Analytics
  └─ 150 students completed test
  └─ Average score: 72%
  └─ Hardest question: Q#7 (45% correct)
  └─ Time taken: avg 12 minutes

ENTIRE WORKFLOW SUMMARY:
────────────────────────
✓ 42-page PDF uploaded
✓ Text extracted automatically
✓ 15 MCQs generated by AI
✓ Validated and formatted
✓ Imported to database
✓ Published to students
✓ 150 students completed test
✓ Analytics generated

All completed in 15 minutes (vs 3-4 hours manual work)
Time saved: ~3.75 hours
Cost saved: ~$75-100
Quality: Professional AI-generated content
"""

print(COMPLETE_EXAMPLE)

print("""
═══════════════════════════════════════════════════════════════════
Summary: GenAI System Code Flow Complete

Key Takeaways:
──────────────
1. Upload PDF → Text extracted → LLM generates MCQs
2. Current Affairs → Topic → LLM generates MCQ + Descriptive
3. Math Problems → LaTeX conversion → MCQ generation
4. All operations tracked in ProcessingTask
5. Automatic fallback: Gemini → OpenAI → Mock

Every action is:
  ✓ Logged and tracked
  ✓ Auditable
  ✓ Reversible
  ✓ Monitored for performance
  ✓ Integrated with your database

See GENAI_WORKFLOW_GUIDE.md for detailed documentation!
═══════════════════════════════════════════════════════════════════
""")
