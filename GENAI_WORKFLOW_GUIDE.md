# GenAI Workflow Guide - Complete Tutorial

## Overview
The GenAI system is an AI-powered content generation platform integrated with your TutionPlus Django project. It uses Gemini Pro (Google's AI) or OpenAI to automatically generate:
- Multiple Choice Questions (MCQs)
- Descriptive answers from current affairs
- Math problems with LaTeX conversion
- Content extraction from PDFs

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Django Admin Interface                    │
│            (http://localhost:8000/admin/genai/)              │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
   ┌────▼─────┐    ┌─────▼────────┐
   │  Models  │    │  Admin Panel  │
   │(Database)│    │  (User UI)    │
   └────┬─────┘    └──────┬────────┘
        │                 │
   ┌────▼─────────────────▼────┐
   │    Task Processors        │
   ├──────────────────────────┤
   │ • PDF Processor          │
   │ • Current Affairs        │
   │ • Math Problem Processor │
   │ • Processing Tasks       │
   └─────────┬────────────────┘
             │
   ┌─────────▼──────────────┐
   │  LLM Provider          │
   ├───────────────────────┤
   │ Gemini Pro (Primary)  │
   │ OpenAI GPT (Fallback) │
   │ Mock Provider (Test)  │
   └───────────────────────┘
```

---

## 4 Main GenAI Models

### 1. PDFUpload Model
**Purpose:** Track PDF documents for processing

**Fields:**
- `title` - Name of the PDF
- `subject` - Subject (polity, history, geography, economics, physics, chemistry, biology, math)
- `pdf_file` - Uploaded PDF file
- `status` - uploaded → processing → completed/failed
- `extracted_text` - Text extracted from PDF
- `total_pages` - Number of pages in PDF

**Example Workflow:**
```
Admin uploads "Biology_Chapter_5.pdf"
    ↓
Status changes to "processing"
    ↓
System extracts text from all pages
    ↓
Generates MCQs from extracted text
    ↓
Status changes to "completed"
    ↓
Output stored in extracted_text field
```

---

### 2. CurrentAffairsGeneration Model
**Purpose:** Generate MCQs and descriptive answers from current affairs topics

**Fields:**
- `topic` - Topic name (e.g., "US-China Trade War", "Climate Summit 2026")
- `source_url` - URL of the source (optional)
- `status` - pending → processing → completed/failed
- `generated_mcq` - Generated MCQ content
- `generated_descriptive` - Generated descriptive answers

**Example Workflow:**
```
User creates entry: Topic = "Budget 2026"
    ↓
LLM generates MCQ based on topic:
    Q: What is the focus of Budget 2026?
    A) Education
    B) Healthcare
    C) Infrastructure
    D) All of the above
    ↓
LLM generates descriptive answer:
    "Budget 2026 focuses on..."
    ↓
Status = "completed"
```

---

### 3. MathProblemGeneration Model
**Purpose:** Convert math expressions and generate MCQ versions with difficulty levels

**Fields:**
- `problem_statement` - Original math problem
- `difficulty` - easy/medium/hard
- `latex_formula` - LaTeX formatted version
- `generated_mcq_version` - MCQ variant
- `status` - pending → processing → completed/failed

**Example Workflow:**
```
Input: "Solve for x: 2x² + 5x - 3 = 0"
    ↓
Convert to LaTeX: $2x^2 + 5x - 3 = 0$
    ↓
Generate MCQ variant:
    Q: Find the roots of 2x² + 5x - 3 = 0
    A) x = -3, x = 0.5
    B) x = 1, x = -2
    C) x = 3, x = -0.5
    D) x = 2, x = -1
    ↓
Status = "completed"
```

---

### 4. ProcessingTask Model
**Purpose:** Generic task tracking for all GenAI operations

**Fields:**
- `task_type` - Type of task (pdf_processing, mcq_generation, etc.)
- `input_data` - JSON with input parameters
- `output_data` - JSON with generated output
- `status` - pending → processing → completed/failed
- `duration_seconds` - How long the task took

---

## How to Use: Step-by-Step Examples

### WORKFLOW 1: Upload and Process a PDF

**Step 1: Access Admin Interface**
```
1. Open browser: http://localhost:8000/admin/
2. Login with your admin credentials
3. Navigate to: GenAI → PDF Uploads
```

**Step 2: Upload PDF**
```
Click "Add PDF Upload" button
Fill in:
  - Title: "Biology Chapter 5 - Cell Division"
  - Subject: Biology
  - PDF File: Select your PDF
  - Description: Optional notes
```

**Step 3: System Processes**
```
Behind the scenes:
  1. PDF is stored in: genai/pdfs/2026/01/25/
  2. Status changes to "processing"
  3. PyPDF2 extracts all text from PDF
  4. LLM (Gemini) reads extracted text
  5. Generates MCQs from content
```

**Step 4: View Results**
```
Admin panel shows:
  - Status badge: GREEN (Completed)
  - Total Pages: 25
  - Extracted Text: Full text from PDF visible in admin
  - Next: Export MCQs to your MCQ database
```

---

### WORKFLOW 2: Generate Current Affairs Content

**Step 1: Create Current Affairs Entry**
```
1. Navigate to: GenAI → Current Affairs Generation
2. Click "Add Current Affairs"
3. Fill in:
   - Topic: "Climate Summit 2026 Results"
   - Source URL: https://example.com/climate-news (optional)
```

**Step 2: Auto-Generation**
```
LLM processes with this prompt:

"Generate 5 multiple choice questions about 'Climate Summit 2026 Results' 
for competitive exams. Make them factual, relevant, and with 4 options."

Generated output example:
  Q1: What was the main agreement at Climate Summit 2026?
  A) Reduce CO2 by 50% by 2030
  B) Ban fossil fuels by 2025
  C) Net-zero emissions by 2050
  D) Phase out coal by 2035

Also generates descriptive answer:
  "The Climate Summit 2026 resulted in..."
```

**Step 3: Use Generated Content**
```
Copy the generated MCQs from admin panel
Paste into your MCQ database
Or use via API: POST /api/genai/current-affairs/
```

---

### WORKFLOW 3: Convert Math Problems to LaTeX + MCQs

**Step 1: Access Math Processor**
```
Navigate to: GenAI → Math Problem Generation
Click "Add Math Problem"
```

**Step 2: Input Problem**
```
Problem Statement: "Find the derivative of x³ + 2x² - 5x + 3"
Difficulty: Medium
```

**Step 3: Automatic Conversion**
```
System converts to LaTeX:
  $\frac{d}{dx}(x^3 + 2x^2 - 5x + 3) = 3x^2 + 4x - 5$

Generates MCQ variant:
  Q: What is the derivative of x³ + 2x² - 5x + 3?
  A) 3x² + 4x - 5  ✓
  B) 3x³ + 2x² - 5
  C) x³ + 2x² - 5x
  D) 2x² + 4x - 3
```

**Step 4: Use in Content**
```
Display in your website/app with proper LaTeX rendering
Students can solve interactively
Track performance per difficulty level
```

---

## Using the LLM Provider System

### What Happens Behind the Scenes

When you trigger any GenAI operation, here's what happens:

**1. Configuration Loading**
```python
# genai/config.py sets up:
DEFAULT_LLM_PROVIDER = 'gemini'  # Primary provider
GEMINI_API_KEY = 'your-key-from-.env'
OPENAI_API_KEY = 'fallback-key'
```

**2. Provider Selection**
```python
# From genai/utils/llm_provider.py

# Try Gemini first (fastest, most capable)
try:
    llm = GeminiProvider(api_key=GEMINI_API_KEY)
except ImportError:
    # Python < 3.8? Fall back to OpenAI
    llm = OpenAIProvider(api_key=OPENAI_API_KEY)
```

**3. Text Generation**
```python
# Simple text generation
response = llm.generate(
    prompt="Generate 5 MCQ questions about Biology",
    temperature=0.7  # Creativity level
)

# JSON structured output
mcqs = llm.generate_json(
    prompt="Generate MCQs in JSON format...",
)
```

---

## Configuration: Setting Up Your API Keys

### Step 1: Create .env File
```bash
Location: c:\Users\newwe\Desktop\tution\tutionplus\.env

Content:
DEFAULT_LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-key-here
OPENAI_API_KEY=your-openai-key-here
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_OUTPUT_TOKENS=2048
```

### Step 2: Get API Keys

**For Gemini Pro:**
```
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key to .env file
4. GEMINI_API_KEY=AIzaSy...
```

**For OpenAI (Fallback):**
```
1. Visit: https://platform.openai.com/account/api-keys
2. Create new secret key
3. Copy to .env file
4. OPENAI_API_KEY=sk-...
```

### Step 3: Restart Django Server
```powershell
Press CTRL+C to stop server
Activate venv: & 'C:\...\env\Scripts\Activate.ps1'
Start server: python manage.py runserver 0.0.0.0:8000
```

---

## Complete Workflow Example: From PDF to MCQ Database

**Scenario:** You have a Biology textbook PDF and want to create MCQs automatically

```
Step 1: Upload PDF
────────────────
Admin → GenAI → PDF Uploads → Add PDF Upload
  Title: "Biology 12th Grade - Chapter 5"
  Subject: Biology
  Upload: chapter5.pdf

Step 2: Extract & Generate
──────────────────────────
System automatically:
  1. Extracts text from 35 pages
  2. Sends to Gemini AI
  3. Receives 70 MCQs with 4 options each
  4. Stores in extracted_text field

Step 3: Review & Export
──────────────────────
Admin can:
  1. View extracted text (verify accuracy)
  2. See processing status
  3. Export MCQs
  4. Copy to clipboard

Step 4: Load into Bank
─────────────────────
Admin → Bank → MCQ → Import
  Paste MCQs
  Select subject: Biology
  Select chapter: 5
  Save

Step 5: Students Use
───────────────────
Students access: https://tutionplus.com/mcq/biology/chapter-5
  1. 70 questions auto-generated
  2. Difficulty tagged
  3. Performance tracked
  4. Analytics generated
```

---

## API Endpoints (Programmatic Access)

If you want to trigger GenAI operations via code instead of admin:

```python
# Example: Process current affairs via API
import requests

response = requests.post(
    'http://localhost:8000/api/genai/current-affairs/mcq/',
    json={'topic': 'Budget 2026'}
)

if response.status_code == 200:
    result = response.json()
    print(result['data'])  # Generated MCQs
```

```python
# Example: Process PDF via API
with open('chapter5.pdf', 'rb') as f:
    files = {'pdf_file': f}
    data = {
        'chapter': '5',
        'topic': 'Cell Division',
        'num_questions': 50
    }
    response = requests.post(
        'http://localhost:8000/api/genai/pdf/process/',
        files=files,
        data=data
    )
    mcqs = response.json()['data']
```

---

## Monitoring: ProcessingTask Model

Each GenAI operation creates a `ProcessingTask` entry:

```
Admin → GenAI → Processing Tasks

Shows:
  Task Type: pdf_processing
  Status: completed
  Duration: 45.2 seconds
  Input: {"pdf_id": 12, "num_pages": 35}
  Output: {"questions_generated": 70, "quality_score": 0.92}
  Timestamp: 2026-01-25 14:30:22
```

Use this to:
- Monitor performance
- Track failures
- Audit all GenAI operations
- Optimize batch processing

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "API Key not found" | .env file missing/incorrect | Create .env file with GEMINI_API_KEY |
| Falls back to OpenAI | Gemini key invalid | Verify API key in Google Cloud console |
| Slow processing | Large PDF | Split into chapters, process separately |
| "No module named google" | Python 3.7 | Upgrade to Python 3.11 (already done!) |
| JSON parsing error | Model response not JSON | Check prompt formatting |

---

## Summary: Quick Reference

```
┌─ PDFs ─┐
│ Upload → Extract → Generate MCQs → Review → Export
└────────┘

┌─ Current Affairs ─┐
│ Enter Topic → LLM generates → MCQ + Descriptive → Save
└────────────────┘

┌─ Math Problems ─┐
│ Input → Convert LaTeX → Create MCQ variant → Display
└────────────────┘

┌─ All Tasks ─┐
│ Tracked in ProcessingTask model → Admin monitoring
└─────────────┘

LLM Selection:
  Gemini Pro (Fast, Best)
       ↓ (falls back if unavailable)
     OpenAI (Reliable)
       ↓ (falls back if needed)
     Mock Provider (Testing)
```

---

**You are now ready to use the GenAI system!** 🚀
