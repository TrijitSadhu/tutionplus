# GenAI System Architecture

## System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Django Application                          │
│                   (TutionPlus Project)                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      GenAI Module                               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              API Layer (views.py)                        │  │
│  │  - /genai/api/current-affairs/mcq/                      │  │
│  │  - /genai/api/current-affairs/descriptive/              │  │
│  │  - /genai/api/pdf/process/                              │  │
│  │  - /genai/api/math/process/                             │  │
│  │  - /genai/api/math/batch/                               │  │
│  │  - /genai/api/status/                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            Task Modules (tasks/)                         │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ Current Affairs Task                               │ │  │
│  │  │ ├─ CurrentAffairsScraper                           │ │  │
│  │  │ │  └─ Fetch from websites                          │ │  │
│  │  │ └─ CurrentAffairsProcessor                         │ │  │
│  │  │    ├─ Generate MCQs                                │ │  │
│  │  │    └─ Save to current_affairs table                │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ PDF Processing Task                                │ │  │
│  │  │ ├─ PDFProcessor                                     │ │  │
│  │  │ │  ├─ Extract text from PDF                        │ │  │
│  │  │ │  └─ Select page ranges                           │ │  │
│  │  │ └─ SubjectMCQGenerator                             │ │  │
│  │  │    ├─ Generate subject MCQs                        │ │  │
│  │  │    └─ Save to total/subject table                  │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ Math Processing Task                               │ │  │
│  │  │ ├─ LaTeXConverter                                  │ │  │
│  │  │ │  ├─ Convert to LaTeX                             │ │  │
│  │  │ │  └─ Validate syntax                              │ │  │
│  │  │ ├─ MathMCQGenerator                                │ │  │
│  │  │ │  ├─ Generate math MCQs                           │ │  │
│  │  │ │  └─ Batch processing                             │ │  │
│  │  │ └─ MathParser                                      │ │  │
│  │  │    └─ Parse and validate expressions               │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↓                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Utility Layer (utils/)                          │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ LLM Provider                                       │ │  │
│  │  │ ├─ OpenAIProvider (default)                        │ │  │
│  │  │ ├─ MockLLMProvider (testing)                       │ │  │
│  │  │ └─ Custom providers (extensible)                   │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  │                                                          │  │
│  │  Config & Management:                                  │  │
│  │  ├─ config.py (Settings)                               │  │
│  │  └─ management/commands/ (CLI)                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         ↓                              ↓                   ↓
    ┌────────┐              ┌──────────────────┐      ┌─────────┐
    │ OpenAI │              │  Website Sources │      │ Django  │
    │   API  │              │  (Web Scraping)  │      │ Models  │
    │        │              │                  │      │ (DB)    │
    └────────┘              └──────────────────┘      └─────────┘
       (gpt-4)              (Current Affairs)    (bank.models.*)
```

## Data Flow Diagram

### 1. Current Affairs Processing Flow

```
Website
  ↓
[Scraper] → Extract HTML & Text
  ↓
[Parser] → Identify articles
  ↓
[LLM] → Generate MCQs/Descriptive
  ↓
[Validator] → Check quality
  ↓
[Database] → Save to current_affairs
  ↓
[API] → Return to user
```

### 2. PDF Processing Flow

```
PDF File
  ↓
[Validator] → Check file size & type
  ↓
[Extractor] → Extract text (select pages)
  ↓
[LLM] → Generate subject MCQs
  ↓
[Processor] → Format & validate
  ↓
[Database] → Save to subject table
  ↓
[API] → Return results
```

### 3. Math Processing Flow

```
Math Problem
  ↓
[Parser] → Analyze expression
  ↓
[LaTeX] → Convert to LaTeX
  ↓
[Validator] → Validate syntax
  ↓
[LLM] → Generate MCQ
  ↓
[Formatter] → Format with LaTeX
  ↓
[Database] → Save to math table
  ↓
[API] → Return MCQ
```

## Component Relationship Diagram

```
┌────────────────────────────────────────────────────────────┐
│                      Django URLconf                        │
│                    (django_project/urls.py)                │
└─────────────────┬──────────────────────────────────────────┘
                  │
                  ↓
        ┌─────────────────────┐
        │   genai/urls.py     │
        │  (Route requests)   │
        └──────────┬──────────┘
                   │
         ┌─────────┼──────────┬────────────┬──────────┐
         ↓         ↓          ↓            ↓          ↓
      [MCQ]   [DESC]    [PDF]      [MATH]      [BATCH]
        ↓         ↓          ↓            ↓          ↓
    ┌───────────────────────────────────────────────────┐
    │         genai/views.py (API endpoints)           │
    ├───────────────────────────────────────────────────┤
    │ - process_current_affairs_mcq()                   │
    │ - process_current_affairs_descriptive()           │
    │ - process_subject_pdf_view()                      │
    │ - process_math_problem_view()                     │
    │ - batch_process_math_view()                       │
    │ - genai_status()                                  │
    └──────────────┬──────────────────────────────────┘
                   │
         ┌─────────┼──────────┬────────────┬──────────┐
         ↓         ↓          ↓            ↓          ↓
    [CA Task]  [PDF]     [Math]        [LLM]      [Utils]
         ↓         ↓          ↓            ↓          ↓
    ┌──────────────────────────────────────────────────┐
    │         genai/tasks/ (Core Logic)               │
    ├──────────────────────────────────────────────────┤
    │ - current_affairs.py                             │
    │ - pdf_processor.py                               │
    │ - math_processor.py                              │
    │         +                                        │
    │     genai/utils/                                 │
    │ - llm_provider.py                                │
    └──────────────┬──────────────────────────────────┘
                   │
         ┌─────────┼──────────┬────────────┐
         ↓         ↓          ↓            ↓
    ┌────────┐ ┌──────┐ ┌──────┐    ┌─────────┐
    │ OpenAI │ │ Web  │ │ PDF  │    │ Django  │
    │  API   │ │Scraper│ │ Libs │    │ Models  │
    └────────┘ └──────┘ └──────┘    └─────────┘
```

## Class Hierarchy

```
LLMProvider (Abstract)
├── OpenAIProvider ✓ (Default)
│   ├── generate()
│   ├── generate_json()
│   └── Error handling
├── MockLLMProvider
│   ├── generate() [Mock]
│   └── generate_json() [Mock]
└── CustomProvider (Extensible)

CurrentAffairsScraper
├── fetch_page()
├── extract_content()
└── scrape_from_sources()

CurrentAffairsProcessor
├── generate_mcq_prompt()
├── generate_descriptive_prompt()
├── process_mcq_content()
├── process_descriptive_content()
├── save_mcq_to_database()
└── run_complete_pipeline()

PDFProcessor
├── extract_text_from_pdf()
├── extract_by_page_range()
└── validate_pdf()

SubjectMCQGenerator
├── generate_mcq_prompt()
├── process_pdf_for_subject()
└── save_mcqs_to_subject_table()

LaTeXConverter
├── is_latex_formatted()
├── generate_latex_conversion_prompt()
└── convert_to_latex()

MathMCQGenerator
├── generate_math_mcq_prompt()
├── process_math_problem()
├── process_math_chapter()
└── save_math_mcqs_to_database()

MathParser
├── extract_formulas()
└── validate_latex_syntax()
```

## Configuration Hierarchy

```
.env (Environment Variables)
  ↓
genai/config.py (Default Settings)
  ├── OPENAI_API_KEY
  ├── OPENAI_MODEL
  ├── CURRENT_AFFAIRS_SOURCES
  ├── PDF_UPLOAD_PATH
  └── MAX_PDF_SIZE
  
Settings passed to:
  ├── LLMProvider (API config)
  ├── CurrentAffairsScraper (Sources)
  ├── PDFProcessor (Storage)
  └── Other modules
```

## Request Processing Pipeline

```
HTTP Request
    ↓
[Django Router]
    ↓
[genai/urls.py] (matches pattern)
    ↓
[genai/views.py] (API handler)
    ↓
[Input Validation]
    ├─ Check required fields
    ├─ Validate file types
    └─ Sanitize inputs
    ↓
[Task Module] (Process)
    ├─ Scraper/Extractor
    ├─ LLM Processing
    └─ Database Save
    ↓
[Error Handling]
    ├─ Catch exceptions
    ├─ Log errors
    └─ Return user-friendly message
    ↓
[Response Formatting]
    ├─ JSON conversion
    └─ Status code
    ↓
HTTP Response
```

## Database Integration

```
Django Models
    ↓
current_affairs
├── upper_heading (question)
├── yellow_heading (explanation)
├── key_1 (option A)
├── key_2 (option B)
├── key_3 (option C)
├── key_4 (option D)
└── day, creation_time

total (Subject)
├── subtopic
├── subtopic_more
└── other_fields

Custom Math Model
├── problem_latex
├── question
├── options
├── correct_answer
└── explanation
```

## Deployment Architecture

```
Local Development
├── .env (local config)
├── SQLite (local DB)
└── Development API keys

Production Deployment
├── Environment variables (secure)
├── PostgreSQL (production DB)
├── Redis (caching/queue)
├── Celery (async tasks)
└── Production API keys
```

## Security Architecture

```
Input
  ↓
[CSRF Protection] ✓
  ↓
[Input Validation] ✓
  ├─ File type check
  ├─ Size validation
  └─ Content sanitization
  ↓
[API Key Security] ✓
  ├─ Stored in .env
  └─ Never in code
  ↓
[Database] ✓
  ├─ ORM protection
  └─ Parameterized queries
  ↓
[Error Handling] ✓
  ├─ No sensitive info leaked
  └─ Logged securely
  ↓
Output
```

## Performance Optimization Strategy

```
Request Optimization
├─ Input validation (fast fail)
├─ Caching (Redis)
└─ Async processing (Celery)

API Optimization
├─ Rate limiting
├─ Batch processing
└─ Token optimization

Database Optimization
├─ Indexing
├─ Query optimization
└─ Connection pooling

Monitoring
├─ API usage tracking
├─ Error logging
└─ Performance metrics
```

---

This architecture provides a scalable, maintainable, and extensible system for GenAI content generation.
