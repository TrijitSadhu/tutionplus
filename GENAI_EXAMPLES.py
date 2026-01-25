"""
GenAI Practical Examples
Quick script to understand how GenAI works programmatically
"""

# EXAMPLE 1: Setup and Configuration
# ===================================

print("=" * 60)
print("EXAMPLE 1: Understanding the Configuration")
print("=" * 60)

# Your .env file should contain:
env_content = """
# File: .env
DEFAULT_LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxx  # Get from Google AI Studio
OPENAI_API_KEY=sk-xxxxxxxxx           # Get from OpenAI Dashboard
GEMINI_TEMPERATURE=0.7                # 0=deterministic, 1=creative
GEMINI_MAX_OUTPUT_TOKENS=2048         # Max response length
"""

print(env_content)

# EXAMPLE 2: How Models Work
# ===========================

print("\n" + "=" * 60)
print("EXAMPLE 2: Database Models")
print("=" * 60)

model_examples = """
1. PDFUpload Model
   ├── Stores PDF files
   ├── Tracks extraction status
   ├── Stores extracted text
   └── Output: Text ready for MCQ generation

2. CurrentAffairsGeneration Model
   ├── Topic name (e.g., "Climate Summit")
   ├── Generates MCQs automatically
   ├── Generates descriptive answers
   └── Output: Ready-to-use Q&A content

3. MathProblemGeneration Model
   ├── Input: "Solve 2x² + 5x - 3 = 0"
   ├── Converts to LaTeX: $2x^2 + 5x - 3 = 0$
   ├── Creates MCQ version
   └── Output: Properly formatted math content

4. ProcessingTask Model
   ├── Tracks ALL GenAI operations
   ├── Records timing and performance
   ├── Stores input/output
   └── For debugging and monitoring
"""

print(model_examples)

# EXAMPLE 3: Admin Interface Workflow
# ====================================

print("\n" + "=" * 60)
print("EXAMPLE 3: Using the Django Admin Interface")
print("=" * 60)

admin_steps = """
Step 1: Open Admin
─────────────────
URL: http://localhost:8000/admin/
Login with your admin account

Step 2: Navigate to GenAI
────────────────────────
Left sidebar → GenAI section
You'll see:
  • PDF Uploads
  • Current Affairs Generation
  • Math Problem Generation
  • Processing Tasks

Step 3: Example - Upload a PDF
──────────────────────────────
1. Click "PDF Uploads"
2. Click "Add PDF Upload" (blue button)
3. Fill form:
   - Title: "History Chapter 10"
   - Subject: history
   - PDF File: Select your PDF
   - Description: (optional)
4. Click Save

Step 4: Monitor Processing
──────────────────────────
Refresh the page and watch:
  • Status badge changes: orange → blue → green
  • Total Pages: Auto-filled
  • Extracted Text: Populated with full content
  • Takes ~30-60 seconds depending on PDF size

Step 5: Use the Output
─────────────────────
Now you have two options:
  a) Copy extracted text manually
  b) Export to CSV/JSON via Django admin
  c) Access via API (see Example 5)

Status Badges:
  🟠 Uploaded  = Just uploaded, not processed
  🔵 Processing = Currently being handled
  🟢 Completed = Done, ready to use
  🔴 Failed = Error occurred, check error_message
"""

print(admin_steps)

# EXAMPLE 4: LLM Provider Selection
# ==================================

print("\n" + "=" * 60)
print("EXAMPLE 4: How LLM Provider Selection Works")
print("=" * 60)

provider_logic = """
Your system has automatic fallback logic:

When you trigger any GenAI operation:

┌─ Start Task ─────────────────────────┐
│  (e.g., Upload PDF)                  │
└──────────────┬──────────────────────┘
               │
        ┌──────▼──────┐
        │ Try Gemini  │
        └──────┬──────┘
               │
        ┌──────▼──────────────┐
        │ Gemini key valid?   │
        │ Python 3.8+?        │
        │ API working?        │
        └──────┬──────────────┘
               │
        ┌──────▼──────────────┐
        │ Success?           │
        │   YES → Use Gemini │
        │   NO → Fall back   │
        └──────┬──────────────┘
               │
        ┌──────▼────────────┐
        │ Try OpenAI        │
        └──────┬────────────┘
               │
        ┌──────▼──────────────┐
        │ OpenAI key valid?   │
        │ API working?        │
        └──────┬──────────────┘
               │
        ┌──────▼──────────────┐
        │ Success?           │
        │   YES → Use OpenAI │
        │   NO → Return err  │
        └────────────────────┘

Your current setup:
  ✓ Python 3.11 (supports Gemini)
  ✓ Gemini API available
  ✓ OpenAI API available (fallback)
  
Result: Fast, reliable, with automatic fallback!
"""

print(provider_logic)

# EXAMPLE 5: Using API (Programmatic)
# ====================================

print("\n" + "=" * 60)
print("EXAMPLE 5: Programmatic API Usage")
print("=" * 60)

api_examples = """
# Example 1: Generate Current Affairs MCQs
import requests

response = requests.post(
    'http://localhost:8000/api/genai/current-affairs/mcq/',
    json={
        'topic': 'Union Budget 2026',
        'source_url': 'https://example.com/budget'
    }
)

result = response.json()
if result['success']:
    print(result['data'])  # Your generated MCQs!
    # Output example:
    # {
    #     'mcqs': [
    #         {
    #             'question': 'What was the allocation for education?',
    #             'options': ['10%', '15%', '20%', '25%'],
    #             'answer': 'B'
    #         },
    #         ...
    #     ]
    # }


# Example 2: Process a PDF
import requests

with open('biology_chapter_5.pdf', 'rb') as pdf:
    response = requests.post(
        'http://localhost:8000/api/genai/pdf/process/',
        files={'pdf_file': pdf},
        data={
            'chapter': '5',
            'topic': 'Cell Division',
            'num_questions': 50
        }
    )

result = response.json()
if result['success']:
    mcqs = result['data']  # 50 auto-generated MCQs
    for mcq in mcqs:
        print(f"Q: {mcq['question']}")
        print(f"A) {mcq['option_a']}")
        print(f"B) {mcq['option_b']}")
        print()


# Example 3: Process Math Problem
import requests

response = requests.post(
    'http://localhost:8000/api/genai/math/process/',
    json={
        'problem': 'Find the derivative of x³ + 2x² - 5x + 3',
        'difficulty': 'medium'
    }
)

result = response.json()
if result['success']:
    problem = result['data']
    print(f"LaTeX: {problem['latex']}")
    # Output: $\\frac{d}{dx}(x^3 + 2x^2 - 5x + 3) = 3x^2 + 4x - 5$
    
    print(f"MCQ: {problem['mcq_version']}")
"""

print(api_examples)

# EXAMPLE 6: Real-World Scenario
# ===============================

print("\n" + "=" * 60)
print("EXAMPLE 6: Complete Real-World Scenario")
print("=" * 60)

scenario = """
Scenario: You teach Biology to 1000 students. You have a textbook PDF.
Goal: Create 100 unique MCQs for the chapter.

Timeline:
─────────

Monday 9:00 AM
└─ Visit Admin Panel: /admin/genai/pdfs/
└─ Click "Add PDF Upload"
└─ Upload: "Biology_12th_Textbook_Chapter5.pdf" (45 pages)
└─ Save

Monday 9:15 AM
└─ System processing...
   └─ Extracts text from 45 pages
   └─ Sends to Gemini Pro
   └─ Generates MCQs with options
   └─ Validates JSON format
   └─ Status changes to "Completed"

Monday 9:20 AM
└─ Open admin again
└─ See status: ✓ COMPLETED
└─ See extracted text: Full chapter content
└─ Download MCQs as JSON/CSV

Monday 9:25 AM
└─ Import MCQs to your main MCQ database
   └─ Admin → Bank → MCQ → Import
   └─ Subject: Biology
   └─ Chapter: 5
   └─ Difficulty: Medium (auto-detected)
   └─ Total imported: 100 questions

Monday 10:00 AM
└─ MCQs go LIVE on platform
└─ 1000 students can access

Result:
───────
✓ 45-page PDF → 100 quality MCQs in 20 minutes
✓ Average manual creation: 5-6 hours
✓ Time saved: ~5.5 hours
✓ Cost saved: ~$50-100 in contractor fees
✓ All tracked in ProcessingTask database
"""

print(scenario)

# EXAMPLE 7: Monitoring & Debugging
# ==================================

print("\n" + "=" * 60)
print("EXAMPLE 7: Monitoring with ProcessingTask Model")
print("=" * 60)

monitoring = """
Every GenAI operation creates a ProcessingTask entry

View in Admin: /admin/genai/processingtask/

Shows:
  task_type: "pdf_processing"
  status: "completed"
  input_data: {
      "pdf_id": 5,
      "pages": 45,
      "file_size": "5.2 MB"
  }
  output_data: {
      "questions_generated": 100,
      "quality_score": 0.94,
      "processing_time": 15.3
  }
  created_at: 2026-01-25 14:30:22
  completed_at: 2026-01-25 14:30:37
  duration_seconds: 15.3

Use this data to:
  1. Monitor system performance
  2. Identify bottlenecks
  3. Track all operations
  4. Calculate statistics:
     - Average processing time
     - Success rate
     - Quality metrics
     - Peak usage times
"""

print(monitoring)

# EXAMPLE 8: Troubleshooting
# ===========================

print("\n" + "=" * 60)
print("EXAMPLE 8: Common Issues & Solutions")
print("=" * 60)

troubleshooting = """
Issue: "GENAI_API_KEY not found"
────────────────────────────────
Location: Check genai/config.py

Solution:
  1. Create .env file in project root
  2. Add: GEMINI_API_KEY=your_key
  3. Restart Django server
  4. Check: python manage.py check

Issue: "PDF processing takes too long"
──────────────────────────────────────
Cause: Large PDF (>50 MB)

Solution:
  1. Split PDF into chapters
  2. Process separately
  3. Or increase GEMINI_MAX_OUTPUT_TOKENS
  4. Monitor with ProcessingTask

Issue: "JSON parsing error"
──────────────────────────
Cause: Model returned invalid JSON

Solution:
  1. Check the prompt formatting
  2. Add JSON instruction to prompt
  3. Try OpenAI provider instead
  4. Check error_message field

Issue: "Gemini fallback to OpenAI"
──────────────────────────────────
Possible causes:
  • Invalid GEMINI_API_KEY
  • API quota exceeded
  • Network issue

Check:
  1. Verify key in Google AI Studio
  2. Check API usage quota
  3. See logs in Django console
  
This is OK - OpenAI fallback works fine!
"""

print(troubleshooting)

print("\n" + "=" * 60)
print("END OF EXAMPLES")
print("=" * 60)
print("""
Next Steps:
───────────
1. Create .env file with API keys
2. Visit http://localhost:8000/admin/genai/
3. Try uploading a PDF
4. Watch the magic happen!
5. Check ProcessingTask for details
6. Export and use the generated content

Questions? Check GENAI_WORKFLOW_GUIDE.md for detailed documentation!
""")
