# Math PDF Processing - Visual Workflow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MATH PDF PROCESSING SYSTEM                   │
│                                                                 │
│  ┌───────────────┐         ┌──────────────┐                   │
│  │  Expression   │         │  PDF File    │                   │
│  │    Input      │         │   Upload     │                   │
│  └───────┬───────┘         └──────┬───────┘                   │
│          │                         │                           │
│          │                         │                           │
│          ▼                         ▼                           │
│  ┌──────────────────────────────────────────┐                 │
│  │    MathProblemGeneration Model           │                 │
│  │  - expression (optional)                 │                 │
│  │  - chapter (dynamic from bank.math)      │                 │
│  │  - difficulty (easy/medium/hard)         │                 │
│  │  - pdf_file (uploaded PDF)               │                 │
│  │  - status, latex_output, mcqs, errors    │                 │
│  └──────────────┬───────────────────────────┘                 │
│                 │                                              │
│                 │                                              │
│                 ▼                                              │
│  ┌─────────────────────────────────────────┐                  │
│  │     Admin Interface - GO Button         │                  │
│  │  List Display:                          │                  │
│  │  [Expression] [Chapter] [Status] [GO]   │                  │
│  └──────────────┬──────────────────────────┘                  │
│                 │                                              │
│                 │ Click GO                                     │
│                 ▼                                              │
│  ┌─────────────────────────────────────────────────────┐      │
│  │        Configuration Form (11 Fields)               │      │
│  │  ┌─────────────────────────────────────────────┐   │      │
│  │  │ LLM Decision Controls                       │   │      │
│  │  │  ☑ Let LLM decide chapter                  │   │      │
│  │  │  ☑ Let LLM decide difficulty               │   │      │
│  │  └─────────────────────────────────────────────┘   │      │
│  │  ┌─────────────────────────────────────────────┐   │      │
│  │  │ OCR Engine Selection                        │   │      │
│  │  │  ☑ PaddleOCR (high accuracy)               │   │      │
│  │  │  ☑ EasyOCR (80+ languages)                 │   │      │
│  │  │  ☑ Tesseract (fallback)                    │   │      │
│  │  └─────────────────────────────────────────────┘   │      │
│  │  ┌─────────────────────────────────────────────┐   │      │
│  │  │ Page Processing                             │   │      │
│  │  │  Page From: [5]  Page To: [10]             │   │      │
│  │  │  ☑ Process page range                      │   │      │
│  │  │  ☐ Process chunks: [5] pages               │   │      │
│  │  │  ☐ Process all pages                       │   │      │
│  │  └─────────────────────────────────────────────┘   │      │
│  │                     [Proceed]                       │      │
│  └──────────────┬──────────────────────────────────────┘      │
│                 │                                              │
│                 │ Submit                                       │
│                 ▼                                              │
│  ┌─────────────────────────────────────────────────┐          │
│  │         MathPDFProcessor.process()              │          │
│  └──────────────┬──────────────────────────────────┘          │
│                 │                                              │
└─────────────────┼──────────────────────────────────────────────┘
                  │
                  │
┌─────────────────▼─────────────────────────────────────────────┐
│                 MODE ROUTING                                  │
│                                                               │
│     ┌─────────────────────┐         ┌────────────────────┐   │
│     │  Has expression &   │   OR    │  Has PDF & config  │   │
│     │  no PDF             │         │  process_pdf=True  │   │
│     └─────────┬───────────┘         └─────────┬──────────┘   │
│               │                               │              │
│               ▼                               ▼              │
│   ┌───────────────────────┐      ┌──────────────────────┐   │
│   │  EXPRESSION MODE      │      │    PDF MODE          │   │
│   │  (Existing - Preserved)│      │    (New Pipeline)    │   │
│   └───────────┬───────────┘      └──────────┬───────────┘   │
└───────────────┼──────────────────────────────┼───────────────┘
                │                              │
                │                              │
                ▼                              ▼
    ┌──────────────────────┐      ┌──────────────────────────┐
    │  LaTeXConverter      │      │   OCR DISPATCHER         │
    │  MathMCQGenerator    │      │                          │
    └──────────┬───────────┘      │  Try engines in order:   │
               │                  │  1. PaddleOCR            │
               │                  │  2. EasyOCR              │
               │                  │  3. Tesseract            │
               │                  │  Return first success    │
               ▼                  └────────┬─────────────────┘
    ┌──────────────────────┐              │
    │  Save to             │              │
    │  MathProblemGen      │              ▼
    │  - latex_output      │   ┌──────────────────────────┐
    │  - generated_mcqs    │   │  TEXT EXTRACTED          │
    └──────────────────────┘   │  "Solve: x^2+5x+6=0..."  │
                               └────────┬─────────────────┘
                                        │
                                        │
                    ┌───────────────────┴───────────────────┐
                    │                                       │
                    ▼                                       ▼
         ┌──────────────────────┐              ┌──────────────────────┐
         │  LLM CLASSIFICATION  │              │  MANUAL VALUES       │
         │  (if enabled)        │              │  (fallback)          │
         │                      │              │                      │
         │  Chapter:            │              │  Use provided:       │
         │  classify_chapter()  │              │  - chapter           │
         │  → Algebra (95%)     │              │  - difficulty        │
         │                      │              │                      │
         │  Difficulty:         │              │                      │
         │  classify_difficulty │              │                      │
         │  → medium (88%)      │              │                      │
         └──────────┬───────────┘              └──────────┬───────────┘
                    │                                     │
                    └────────────────┬────────────────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  MCQ EXTRACTION      │
                          │  (LLM)               │
                          │                      │
                          │  extract_mcqs()      │
                          │  Input: Text         │
                          │  Output: List[MCQ]   │
                          │                      │
                          │  MCQ Format:         │
                          │  - question          │
                          │  - choice1-4         │
                          │  - correct_answer    │
                          └──────────┬───────────┘
                                     │
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  SAVE TO DATABASE    │
                          │                      │
                          │  bank.math table:    │
                          │  - chapter           │
                          │  - difficulty        │
                          │  - question          │
                          │  - choice1-4         │
                          │  - ans (1-4)         │
                          │  - source='genai-pdf'│
                          └──────────┬───────────┘
                                     │
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  UPDATE LOG          │
                          │                      │
                          │  ProcessingLog:      │
                          │  - task_type         │
                          │  - status=completed  │
                          │  - result_summary:   │
                          │    total_pages: 6    │
                          │    mcqs_extracted: 15│
                          │  - duration          │
                          └──────────┬───────────┘
                                     │
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │  SUCCESS MESSAGE     │
                          │                      │
                          │  "Processing complete│
                          │   15 MCQs extracted  │
                          │   from 6 pages"      │
                          │                      │
                          │  [Back to Admin]     │
                          └──────────────────────┘
```

## OCR Fallback Chain

```
┌─────────────────────────────────────────────────────────────┐
│                  OCR DISPATCHER                             │
│                                                             │
│  Input: PDF file, page number                              │
│                                                             │
│  ┌──────────────────────────────────────────────┐          │
│  │  1. Try PaddleOCR                            │          │
│  │     - Convert PDF to image (pdf2image)       │          │
│  │     - Extract text with paddleocr            │          │
│  │     - Best for: Chinese/English, accuracy    │          │
│  └────────┬─────────────────────────────────────┘          │
│           │                                                 │
│           ▼                                                 │
│     ┌──────────┐                                           │
│     │ Success? │ ──Yes──→ Return text ───────┐             │
│     └────┬─────┘                              │             │
│          │ No                                 │             │
│          ▼                                    │             │
│  ┌──────────────────────────────────────────────┐          │
│  │  2. Try EasyOCR                              │          │
│  │     - Convert PDF to numpy array             │          │
│  │     - Extract text with easyocr              │          │
│  │     - Best for: 80+ languages                │          │
│  └────────┬─────────────────────────────────────┘          │
│           │                                                 │
│           ▼                                                 │
│     ┌──────────┐                                           │
│     │ Success? │ ──Yes──→ Return text ───────┤             │
│     └────┬─────┘                              │             │
│          │ No                                 │             │
│          ▼                                    │             │
│  ┌──────────────────────────────────────────────┐          │
│  │  3. Try Tesseract                            │          │
│  │     - Convert PDF to image                   │          │
│  │     - Extract text with pytesseract          │          │
│  │     - Best for: Traditional OCR              │          │
│  └────────┬─────────────────────────────────────┘          │
│           │                                                 │
│           ▼                                                 │
│     ┌──────────┐                                           │
│     │ Success? │ ──Yes──→ Return text ───────┤             │
│     └────┬─────┘                              │             │
│          │ No                                 │             │
│          ▼                                    │             │
│    ┌───────────┐                             │             │
│    │ Return    │                             │             │
│    │ None      │                             │             │
│    │ (Failed)  │                             │             │
│    └───────────┘                             │             │
│                                               │             │
│  Output: ─────────────────────────────────────┴─────────→  │
│          Extracted text or None                            │
└─────────────────────────────────────────────────────────────┘
```

## Page Processing Strategies

### Strategy 1: Single Page
```
┌────────────────────────────────────┐
│  Config:                           │
│  - page_from: 5                    │
│  - page_to: 5                      │
│  - process_all_mcqs_of_range: True │
└────────────────┬───────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │  Extract page 5│
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  OCR text      │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Extract MCQs  │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Save to DB    │
        └────────────────┘
```

### Strategy 2: Page Range
```
┌────────────────────────────────────┐
│  Config:                           │
│  - page_from: 10                   │
│  - page_to: 20                     │
│  - process_all_mcqs_of_range: True │
└────────────────┬───────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │  Pages 10-20   │
        └────────┬───────┘
                 │
         ┌───────┴───────┐
         │   Loop each   │
         │     page      │
         └───────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Page 10       │
        │  - OCR         │
        │  - Extract MCQs│
        │  - Save        │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Page 11       │
        │  - OCR         │
        │  - Extract MCQs│
        │  - Save        │
        └────────┬───────┘
                 │
                 ▼
              ... (continues)
                 │
                 ▼
        ┌────────────────┐
        │  Page 20       │
        │  - OCR         │
        │  - Extract MCQs│
        │  - Save        │
        └────────────────┘
```

### Strategy 3: Chunked Full PDF
```
┌────────────────────────────────────┐
│  Config:                           │
│  - page_from: 0                    │
│  - page_to: 0 (entire PDF)         │
│  - chunk_size: 5                   │
└────────────────┬───────────────────┘
                 │
                 ▼
        ┌────────────────┐
        │  Calculate     │
        │  chunks        │
        │  PDF: 47 pages │
        │  Chunks:       │
        │  [0-4, 5-9,    │
        │   10-14, ...]  │
        └────────┬───────┘
                 │
         ┌───────┴───────┐
         │  Process each │
         │    chunk      │
         └───────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Chunk 1 (0-4) │
        │  - OCR all     │
        │  - Extract MCQs│
        │  - Save        │
        └────────┬───────┘
                 │
                 ▼
        ┌────────────────┐
        │  Chunk 2 (5-9) │
        │  - OCR all     │
        │  - Extract MCQs│
        │  - Save        │
        └────────┬───────┘
                 │
                 ▼
              ... (continues)
                 │
                 ▼
        ┌────────────────┐
        │  Chunk 10      │
        │  (45-46)       │
        │  - OCR all     │
        │  - Extract MCQs│
        │  - Save        │
        └────────────────┘
```

## LLM Classification Flow

```
┌─────────────────────────────────────────────────────────┐
│              CHAPTER CLASSIFICATION                     │
│                                                         │
│  Input: Extracted text from OCR                         │
│         "Solve the quadratic equation: x^2+5x+6=0"      │
│                                                         │
│  ┌────────────────────────────────────────────┐        │
│  │  Get/Create LLMPrompt                      │        │
│  │  - task_type: 'chapter_classification'     │        │
│  │  - system_prompt: "You are a math expert..."│       │
│  │  - user_prompt_template: "Analyze..."      │        │
│  └────────────────┬───────────────────────────┘        │
│                   │                                     │
│                   ▼                                     │
│  ┌────────────────────────────────────────────┐        │
│  │  Call LLM with chapter list                │        │
│  │  Available chapters:                       │        │
│  │  - Algebra                                 │        │
│  │  - Geometry                                │        │
│  │  - Trigonometry                            │        │
│  │  - Calculus                                │        │
│  │  - ... (from bank.math)                    │        │
│  └────────────────┬───────────────────────────┘        │
│                   │                                     │
│                   ▼                                     │
│  ┌────────────────────────────────────────────┐        │
│  │  LLM Response (JSON):                      │        │
│  │  {                                         │        │
│  │    "chapter": "Algebra",                   │        │
│  │    "confidence": 0.95,                     │        │
│  │    "reasoning": "Contains quadratic..."    │        │
│  │  }                                         │        │
│  └────────────────┬───────────────────────────┘        │
│                   │                                     │
│                   ▼                                     │
│  ┌────────────────────────────────────────────┐        │
│  │  Parse JSON                                │        │
│  │  - Validate chapter exists in list         │        │
│  │  - Check confidence > 0.7                  │        │
│  └────────────────┬───────────────────────────┘        │
│                   │                                     │
│             ┌─────┴─────┐                              │
│             ▼           ▼                              │
│        ┌────────┐  ┌────────┐                         │
│        │Valid?  │  │Invalid │                         │
│        │        │  │or Error│                         │
│        └───┬────┘  └───┬────┘                         │
│            │           │                               │
│            ▼           ▼                               │
│     ┌──────────┐  ┌──────────────┐                    │
│     │ Return:  │  │ Fallback to: │                    │
│     │ "Algebra"│  │ Manual value │                    │
│     └──────────┘  └──────────────┘                    │
│                                                        │
└────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│            DIFFICULTY CLASSIFICATION                    │
│                                                         │
│  Input: Extracted text from OCR                         │
│         "Solve: x^2 + 5x + 6 = 0"                      │
│                                                         │
│  ┌────────────────────────────────────────────┐        │
│  │  Call LLM with difficulty options          │        │
│  │  Options: easy, medium, hard               │        │
│  └────────────────┬───────────────────────────┘        │
│                   │                                     │
│                   ▼                                     │
│  ┌────────────────────────────────────────────┐        │
│  │  LLM Response (JSON):                      │        │
│  │  {                                         │        │
│  │    "difficulty": "medium",                 │        │
│  │    "confidence": 0.88,                     │        │
│  │    "reasoning": "Requires factoring..."    │        │
│  │  }                                         │        │
│  └────────────────┬───────────────────────────┘        │
│                   │                                     │
│                   ▼                                     │
│  ┌────────────────────────────────────────────┐        │
│  │  Parse JSON                                │        │
│  │  - Validate difficulty in [easy|medium|hard│        │
│  │  - Check confidence > 0.7                  │        │
│  └────────────────┬───────────────────────────┘        │
│                   │                                     │
│             ┌─────┴─────┐                              │
│             ▼           ▼                              │
│        ┌────────┐  ┌────────┐                         │
│        │Valid?  │  │Invalid │                         │
│        │        │  │or Error│                         │
│        └───┬────┘  └───┬────┘                         │
│            │           │                               │
│            ▼           ▼                               │
│     ┌──────────┐  ┌──────────────┐                    │
│     │ Return:  │  │ Fallback to: │                    │
│     │ "medium" │  │ Manual value │                    │
│     └──────────┘  └──────────────┘                    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                        INPUT                                 │
├──────────────────────────────────────────────────────────────┤
│  MathProblemGeneration:                                      │
│  - id: 123                                                   │
│  - expression: None                                          │
│  - chapter: None (or "Algebra")                              │
│  - difficulty: "medium"                                      │
│  - pdf_file: "math/pdfs/algebra_ch5.pdf"                     │
│  - status: "pending"                                         │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                     CONFIGURATION                            │
├──────────────────────────────────────────────────────────────┤
│  {                                                           │
│    "chapter_decide_by_llm": True,                            │
│    "difficulty_level_decide_by_llm": False,                  │
│    "use_paddle_ocr": True,                                   │
│    "use_easy_ocr": True,                                     │
│    "use_tesseract": False,                                   │
│    "process_pdf": True,                                      │
│    "page_from": 0,                                           │
│    "page_to": 5,                                             │
│    "process_all_the_mcq_of_the_pageRange": True              │
│  }                                                           │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    PROCESSING                                │
├──────────────────────────────────────────────────────────────┤
│  Page 0:                                                     │
│  - OCR: "1. Solve x^2+5x+6=0 A)x=-2,-3 B)x=2,3..."         │
│  - Chapter (LLM): "Algebra" (0.95)                           │
│  - Difficulty (manual): "medium"                             │
│  - MCQs found: 3                                             │
│                                                              │
│  Page 1:                                                     │
│  - OCR: "2. Factorize x^2-9 A)(x+3)(x-3)..."                │
│  - Chapter (LLM): "Algebra" (0.93)                           │
│  - Difficulty (manual): "medium"                             │
│  - MCQs found: 2                                             │
│                                                              │
│  ... (Pages 2-5)                                             │
│                                                              │
│  Total: 6 pages, 15 MCQs                                     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                      OUTPUT                                  │
├──────────────────────────────────────────────────────────────┤
│  bank.math records created:                                  │
│                                                              │
│  Record 1:                                                   │
│  - chapter: "Algebra"                                        │
│  - difficulty: "medium"                                      │
│  - question: "Solve x^2+5x+6=0"                              │
│  - choice1: "x=-2, x=-3"                                     │
│  - choice2: "x=2, x=3"                                       │
│  - choice3: "x=-5, x=-6"                                     │
│  - choice4: "x=1, x=6"                                       │
│  - ans: 1                                                    │
│  - source: "genai-pdf"                                       │
│                                                              │
│  Record 2:                                                   │
│  - chapter: "Algebra"                                        │
│  - difficulty: "medium"                                      │
│  - question: "Factorize x^2-9"                               │
│  - choice1: "(x+3)(x-3)"                                     │
│  - choice2: "(x+9)(x-1)"                                     │
│  - choice3: "(x+1)(x-9)"                                     │
│  - choice4: "Cannot factorize"                               │
│  - ans: 1                                                    │
│  - source: "genai-pdf"                                       │
│                                                              │
│  ... (13 more records)                                       │
│                                                              │
│  ProcessingLog:                                              │
│  - task_type: "math_pdf_processing"                          │
│  - status: "completed"                                       │
│  - result_summary: {                                         │
│      "total_pages": 6,                                       │
│      "mcqs_extracted": 15,                                   │
│      "mcqs_saved": 15,                                       │
│      "failed_mcqs": 0,                                       │
│      "ocr_failures": 0,                                      │
│      "duration_seconds": 47.2                                │
│    }                                                         │
│                                                              │
│  MathProblemGeneration updated:                              │
│  - status: "completed"                                       │
│  - processed_at: "2026-01-28 23:45:12"                       │
└──────────────────────────────────────────────────────────────┘
```

## Admin Interface Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    ADMIN LIST VIEW                           │
│  /admin/genai/mathproblemgeneration/                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Expression    │Chapter │Difficulty│Status  │PDF│LaTeX│Action│
│  ─────────────────────────────────────────────────────────── │
│  x^2+5x+6      │Algebra │medium    │✓Done  │✗  │✓   │[ GO ]│
│  (No expr)     │-       │-         │Pending│✓  │✗   │[ GO ]│ ◄─ Click
│  3x+7=22       │Linear  │easy      │✓Done  │✗  │✓   │[ GO ]│
│                                                              │
└────────────────────────────────┬─────────────────────────────┘
                                 │
                                 │ Click GO
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│              CONFIGURATION FORM                              │
│  /genai/admin/math-pdf-processing/123/                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │  Problem Information                           │         │
│  │  ─────────────────────────────────────────────│         │
│  │  ID: 123                                       │         │
│  │  Expression: (None)                            │         │
│  │  Current Chapter: (None)                       │         │
│  │  Current Difficulty: medium                    │         │
│  │  PDF File: algebra_ch5.pdf                     │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │  LLM Decision Controls                         │         │
│  │  ─────────────────────────────────────────────│         │
│  │  ☑ Let LLM decide chapter                     │         │
│  │  ☐ Let LLM decide difficulty level            │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │  OCR Engine Selection                          │         │
│  │  ─────────────────────────────────────────────│         │
│  │  ☑ Use PaddleOCR (recommended)                │         │
│  │  ☑ Use EasyOCR (80+ languages)                │         │
│  │  ☐ Use Tesseract (traditional)                │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │  Processing Mode                               │         │
│  │  ─────────────────────────────────────────────│         │
│  │  ☑ Process PDF file                           │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │  Page Controls                                 │         │
│  │  ─────────────────────────────────────────────│         │
│  │  Page From: [0]     (0-indexed)               │         │
│  │  Page To:   [5]     (0 = last page)           │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │  MCQ Extraction Modes                          │         │
│  │  ─────────────────────────────────────────────│         │
│  │  ☑ Process all MCQs in page range             │         │
│  │  ☐ Process entire PDF in chunks: [5] pages    │         │
│  │  ☐ Process all MCQs from all pages            │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
│                   [Cancel]  [Proceed]  ◄─────────────────── Click
│                                                              │
└────────────────────────────────┬─────────────────────────────┘
                                 │
                                 │ Submit form
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                    PROCESSING...                             │
│                                                              │
│  ⏳ Extracting text from PDF...                              │
│  ⏳ Classifying chapter with LLM...                          │
│  ⏳ Extracting MCQs...                                       │
│  ⏳ Saving to database...                                    │
│                                                              │
└────────────────────────────────┬─────────────────────────────┘
                                 │
                                 │ Redirect
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                  SUCCESS MESSAGE                             │
│  /admin/genai/mathproblemgeneration/                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ PDF processing started successfully!                     │
│     Extracted 15 MCQs from 6 pages                           │
│                                                              │
│  Expression    │Chapter │Difficulty│Status  │PDF│LaTeX│Action│
│  ─────────────────────────────────────────────────────────── │
│  x^2+5x+6      │Algebra │medium    │✓Done  │✗  │✓   │[ GO ]│
│  (No expr)     │Algebra │medium    │✓Done  │✓  │✗   │[ GO ]│ ◄─ Updated
│  3x+7=22       │Linear  │easy      │✓Done  │✗  │✓   │[ GO ]│
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

This visual workflow provides a comprehensive overview of the entire Math PDF Processing system architecture, data flow, and user interaction patterns.
