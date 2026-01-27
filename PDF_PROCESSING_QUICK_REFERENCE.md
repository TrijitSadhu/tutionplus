# Quick Reference: What Exists vs What's Needed

## File by File Breakdown

### ✅ PRODUCTION READY (No Changes Needed)

#### genai/config.py
```python
Lines 47-49:
✅ PDF_UPLOAD_PATH = defined
✅ MAX_PDF_SIZE = 50MB limit set
Action: USE AS-IS
```

#### genai/tasks/pdf_processor.py
```python
Lines 35-116:  PDFProcessor class
✅ extract_text_from_pdf()     - WORKING
✅ extract_by_page_range()     - WORKING
✅ validate_pdf()               - WORKING
Action: USE AS-IS

Lines 119-153: SubjectMCQGenerator.__init__() & generate_mcq_prompt()
✅ generate_mcq_prompt()        - WORKING
Action: EXTEND for subjects

Lines 155-187: SubjectMCQGenerator.process_pdf_for_subject()
✅ Logic flow                   - WORKING
⚠️  Subject integration         - NEEDS FIXING (line 173-179 saves to 'total' model)
Action: ENHANCE subject handling

Lines 189-216: SubjectMCQGenerator.save_mcqs_to_subject_table()
⚠️  Currently saves to: total model (generic)
Action: UPDATE to support all subjects
```

#### genai/models.py - PDFUpload
```python
Lines 6-44: PDFUpload model
✅ title, subject, pdf_file    - READY
✅ uploaded_by (ForeignKey)    - USER TRACKING ✓
✅ status, total_pages         - READY
✅ extracted_text              - READY
Action: USE & REFERENCE

NEW: Add these to ProcessingLog instead
  - NOT to PDFUpload
```

#### genai/models.py - ProcessingTask
```python
Lines 110-148: ProcessingTask model
✅ task_type='pdf_to_mcq'      - ALREADY DEFINED
✅ pdf_upload FK               - LINKS TO PDF
✅ created_by FK               - USER TRACKING ✓
Action: USE AS FALLBACK
```

#### genai/models.py - ProcessingLog  
```python
Lines 152-236: ProcessingLog model
✅ TASK_TYPES with pdf_ prefix - ALREADY DEFINED
✅ pdf_upload FK               - LINKS TO PDF
✅ created_by FK               - USER TRACKING ✓
✅ Progress tracking fields    - PRESENT
⚠️  TASK_TYPES = 5 types only
❌  Missing 6 new fields
Action: EXTEND with 6 new fields & 10 new types
```

#### genai/admin.py - PDFUploadAdmin
```python
Lines 13-53: PDFUploadAdmin
✅ Display settings            - READY
✅ Filters                      - READY
✅ Search                       - READY
✅ Actions defined             - READY
❌ Actions not connected       - NEEDS IMPLEMENTATION
Action: CONNECT actions to processors
```

---

### ⚠️ PARTIALLY READY (Needs Enhancement)

#### genai/tasks/pdf_processor.py - SubjectMCQGenerator
```python
Current: Saves to generic 'total' model (bank/models.py)
Problem: Not subject-specific

Needed Enhancement:
- Detect subject from task_type
- Route to correct subject table
- Save formatted output

Example Fix:
def save_mcqs_to_subject_table(self, mcq_data, subject):
    if subject == 'polity':
        from bank.models import polity_mcq
        # save to polity_mcq model
    elif subject == 'economics':
        from bank.models import economics_mcq
        # save to economics_mcq model
    # ... etc
```

#### genai/models.py - ProcessingLog TASK_TYPES
```python
Current (5 types):
✅ currentaffairs_mcq_fetch
✅ currentaffairs_descriptive_fetch
✅ both
✅ pdf_currentaffairs_mcq
✅ pdf_currentaffairs_descriptive

Needed (add 10):
❌ pdf_to_mcq
❌ pdf_to_descriptive
❌ pdf_to_polity
❌ pdf_to_economics
❌ pdf_to_math
❌ pdf_to_physics
❌ pdf_to_chemistry
❌ pdf_to_history
❌ pdf_to_geography
❌ pdf_to_biology

Action: Add to TASK_TYPES tuple
```

#### genai/models.py - ProcessingLog Fields
```python
Current (18 fields):
✅ task_type
✅ status
✅ pdf_upload (FK)
✅ started_at, completed_at
✅ total_items, processed_items
✅ success_count, error_count
✅ mcq_status, current_affairs_status
✅ error_message, log_details
✅ scheduled_time, is_scheduled
✅ skip_scraping
✅ created_at, updated_at
✅ created_by (FK)

Needed (add 6):
❌ subject (CharField) - for routing
❌ output_format (CharField) - json/markdown/text
❌ start_page (IntegerField) - page range
❌ end_page (IntegerField) - page range
❌ difficulty_level (CharField) - easy/medium/hard
❌ num_items (IntegerField) - quantity to generate

Action: Add to ProcessingLog.Meta
```

---

### ❌ NOT YET CREATED (Need to Create)

#### NEW: genai/tasks/subject_processor.py
```python
Purpose: Subject-specific processors
File Status: DOES NOT EXIST

Needed Classes:
- PolityProcessor (extends SubjectMCQGenerator)
- EconomicsProcessor (extends SubjectMCQGenerator)
- MathProcessor (extends SubjectMCQGenerator)
- PhysicsProcessor (extends SubjectMCQGenerator)
- ChemistryProcessor (extends SubjectMCQGenerator)
- HistoryProcessor (extends SubjectMCQGenerator)
- GeographyProcessor (extends SubjectMCQGenerator)
- BiologyProcessor (extends SubjectMCQGenerator)

Action: CREATE THIS FILE
Timeline: 2 hours to write & test
```

#### NEW: 10 Subject-Specific LLMPrompts
```python
Current in database (6 prompts):
✅ MCQ - default
✅ Descriptive - default
✅ MCQ - GKToday specific
✅ MCQ - IndiaBIX specific
✅ Descriptive - NDTV specific
✅ MCQ - skip_scraping_mode

Needed in database (10 more):
❌ MCQ - for Polity
❌ Descriptive - for Polity
❌ MCQ - for Economics
❌ Descriptive - for Economics
❌ MCQ - for Math
❌ Descriptive - for Math
❌ MCQ - for Physics
❌ Descriptive - for Physics
❌ MCQ - for Chemistry
❌ Descriptive - for Chemistry
❌ MCQ - for History
❌ Descriptive - for History
❌ MCQ - for Geography
❌ Descriptive - for Geography
❌ MCQ - for Biology
❌ Descriptive - for Biology

Actually needed: 16 new prompts (2 per subject × 8 subjects)

Action: Create via admin interface or migration script
Timeline: 1 hour to create all
```

#### NEW: Management Command
```python
Purpose: CLI interface for PDF processing
File Status: DOES NOT EXIST

Needed: genai/management/commands/process_subject_pdf.py

Usage:
python manage.py process_subject_pdf --pdf-id=1 --subject=polity --format=json

Action: CREATE THIS FILE
Timeline: 1 hour
```

---

## Side-by-Side Comparison

### EXISTING vs NEEDED - PDF Processing Flow

```
CURRENT STATE:
┌─────────────────────────────────────────────────────────────┐
│ PDFUpload Model (bank.models)                               │
│ - title, subject, pdf_file, status                          │
│ - ✅ READY (9 subjects configured)                          │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ ProcessingTask Model (genai.models)                         │
│ - task_type='pdf_to_mcq'                                    │
│ - ✅ DEFINED but not used                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ PDFProcessor.extract_text_from_pdf()                        │
│ - ✅ PRODUCTION READY (248 lines)                           │
│ - Returns: raw text                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ SubjectMCQGenerator.generate_mcq_prompt()                   │
│ - ✅ PRODUCTION READY                                       │
│ - Uses generic prompt (not subject-specific)                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ LLM Processing (Groq/Gemini)                                │
│ - ✅ PRODUCTION READY                                       │
│ - Returns: JSON with MCQs                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ save_mcqs_to_subject_table()                                │
│ - ⚠️  HARDCODED to save to 'total' model                    │
│ - ❌ NOT subject-aware                                      │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ Bank.models.total table                                     │
│ - ❌ Generic table (not subject-specific)                   │
└─────────────────────────────────────────────────────────────┘

PROBLEM: Everything is generic. No subject routing.

═══════════════════════════════════════════════════════════════

NEEDED ENHANCEMENT:
┌─────────────────────────────────────────────────────────────┐
│ PDFUpload Model (genai.models) ✅ EXISTING                  │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ ProcessingLog Model (genai.models)                          │
│ ✅ EXISTING - with new fields:                              │
│   • subject (NEW)                                           │
│   • output_format (NEW)                                     │
│   • start_page, end_page (NEW)                              │
│   • difficulty_level (NEW)                                  │
│   • num_items (NEW)                                         │
│ ✅ New TASK_TYPES (10):                                     │
│   • pdf_to_mcq, pdf_to_descriptive                          │
│   • pdf_to_polity, pdf_to_economics, etc.                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ PDFProcessor.extract_text_from_pdf() ✅ REUSE               │
│ - Returns: raw text by page range                           │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ SubjectProcessor (NEW) - Extends SubjectMCQGenerator        │
│ • PolityProcessor                                           │
│ • EconomicsProcessor                                        │
│ • MathProcessor                                             │
│ • etc.                                                      │
│ - Route based on subject field in ProcessingLog             │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ LLMPrompt (subject-specific) (NEW)                          │
│ • Prompts for polity_mcq, polity_descriptive                │
│ • Prompts for economics_mcq, economics_descriptive          │
│ • etc. (10 new + 6 existing)                                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ LLM Processing (Groq/Gemini) ✅ EXISTING                    │
│ - Returns: JSON with subject-specific output                │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ SubjectProcessor.save_to_subject_table() (ENHANCED)         │
│ - Route based on subject field                              │
│ - Save to correct subject model                             │
│ - Update ProcessingLog with results                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────────────┐
│ Subject-Specific Tables (existing)                          │
│ • bank.models.polity_mcq (if exists)                        │
│ • bank.models.economics_mcq (if exists)                     │
│ • OR: Create generic SubjectOutput table                    │
│ - Update ProcessingLog.success_count                        │
│ - Store results with subject metadata                       │
└─────────────────────────────────────────────────────────────┘

SOLUTION: Route to subject-specific processors & LLM prompts
```

---

## Code Flow Comparison

### Current Flow (Generic MCQ Generation)
```python
# In pdf_processor.py
pdf_path = "/path/to/pdf"
processor = SubjectMCQGenerator()

# 1. Extract (generic)
content = processor.pdf_processor.extract_text_from_pdf(pdf_path)

# 2. Generate prompt (generic - not subject-aware)
prompt = processor.generate_mcq_prompt(
    chapter="Generic",
    topic="Any Topic",
    content=content,
    num_questions=5
)

# 3. Get LLM response
response = processor.llm.generate_json(prompt)

# 4. Save (HARDCODED to 'total' model)
processor.save_mcqs_to_subject_table(response)
# ❌ Always saves to: from bank.models import total
```

### Needed Flow (Subject-Specific)
```python
# In subject_processor.py
pdf_path = "/path/to/pdf"
subject = "polity"  # From ProcessingLog.subject
processor = PolityProcessor()  # or get from factory

# 1. Extract (REUSE existing)
content = processor.pdf_processor.extract_by_page_range(
    pdf_path,
    start_page=0,  # From ProcessingLog.start_page
    end_page=None   # From ProcessingLog.end_page
)

# 2. Generate subject-specific prompt
prompt = processor.generate_mcq_prompt(
    chapter="Polity",
    topic="Indian Constitution",
    content=content,
    num_questions=5,  # From ProcessingLog.num_items
    difficulty=difficulty_level  # From ProcessingLog
)

# 3. Get LLM response using subject-specific LLMPrompt
llm_prompt = LLMPrompt.objects.get(
    source_url=f"pdf_{subject}_mcq",  # ← Subject-specific
    prompt_type='mcq'
)
response = processor.llm.generate_json(llm_prompt.prompt_text.format(...))

# 4. Save to correct subject table
saved = processor.save_mcqs_to_subject_table(
    response,
    subject="polity"  # ← Subject-aware
)

# 5. Update ProcessingLog
processing_log.success_count = len(saved)
processing_log.status = 'completed'
processing_log.save()
```

---

## Implementation Priority Matrix

| Task | Effort | Impact | Dependency | Priority |
|------|--------|--------|-----------|----------|
| Add 6 fields to ProcessingLog | 15 min | HIGH | None | 1️⃣ FIRST |
| Add 10 task types | 10 min | HIGH | None | 1️⃣ FIRST |
| Create migration | 5 min | HIGH | ↑ | 1️⃣ FIRST |
| Create subject_processor.py | 2 hours | HIGH | ↑ | 2️⃣ SECOND |
| Create 16 LLMPrompts | 1 hour | HIGH | ↑ | 2️⃣ SECOND |
| Connect admin actions | 30 min | MEDIUM | 1️⃣ | 3️⃣ THIRD |
| Create management command | 1 hour | MEDIUM | 2️⃣ | 3️⃣ THIRD |
| Test all subjects | 2 hours | MEDIUM | 3️⃣ | 4️⃣ FOURTH |
| Deploy | 30 min | HIGH | 4️⃣ | 5️⃣ LAST |

---

## Copy-Paste Code Blocks

### Add to genai/models.py - ProcessingLog.TASK_TYPES
```python
# EXISTING 5 TYPES (keep these)
TASK_TYPES = [
    ('currentaffairs_mcq_fetch', 'Current Affairs MCQ Fetch from URL'),
    ('currentaffairs_descriptive_fetch', 'Current Affairs Descriptive Fetch from URL'),
    ('both', 'Both MCQ & Current Affairs from URL'),
    ('pdf_currentaffairs_mcq', 'Current Affairs MCQ Generation from PDF'),
    ('pdf_currentaffairs_descriptive', 'Current Affairs Descriptive Generation from PDF'),
    # ADD THESE 10 NEW TYPES:
    ('pdf_to_mcq', 'Generic PDF to MCQ'),
    ('pdf_to_descriptive', 'Generic PDF to Descriptive'),
    ('pdf_to_polity', 'PDF to Polity Questions'),
    ('pdf_to_economics', 'PDF to Economics Concepts'),
    ('pdf_to_math', 'PDF to Math Problems'),
    ('pdf_to_physics', 'PDF to Physics Concepts'),
    ('pdf_to_chemistry', 'PDF to Chemistry Formulas'),
    ('pdf_to_history', 'PDF to History Timeline'),
    ('pdf_to_geography', 'PDF to Geography Facts'),
    ('pdf_to_biology', 'PDF to Biology Concepts'),
]
```

### Add to genai/models.py - ProcessingLog.Meta fields
```python
class ProcessingLog(models.Model):
    # ... existing 18 fields ...
    
    # ADD THESE 6 NEW FIELDS:
    subject = models.CharField(
        max_length=50,
        choices=[
            ('polity', 'Polity'),
            ('history', 'History'),
            ('geography', 'Geography'),
            ('economics', 'Economics'),
            ('physics', 'Physics'),
            ('chemistry', 'Chemistry'),
            ('biology', 'Biology'),
            ('math', 'Math'),
            ('other', 'Other'),
        ],
        default='other',
        blank=True,
        null=True,
        help_text="Subject for PDF processing"
    )
    
    output_format = models.CharField(
        max_length=20,
        choices=[
            ('json', 'JSON Format'),
            ('markdown', 'Markdown Format'),
            ('text', 'Plain Text'),
        ],
        default='json',
        blank=True,
        null=True
    )
    
    start_page = models.IntegerField(
        null=True,
        blank=True,
        help_text="Starting page for large PDFs (1-indexed)"
    )
    
    end_page = models.IntegerField(
        null=True,
        blank=True,
        help_text="Ending page for large PDFs (1-indexed)"
    )
    
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        null=True,
        blank=True
    )
    
    num_items = models.IntegerField(
        default=5,
        help_text="Number of questions/items to generate"
    )
```

---

## Summary Table

| Component | Exists | Status | Action |
|-----------|--------|--------|--------|
| PDFProcessor | ✅ | Production | USE |
| SubjectMCQGenerator | ✅ | Partial | ENHANCE |
| PDFUpload model | ✅ | Ready | REFERENCE |
| ProcessingLog model | ✅ | Partial | EXTEND |
| LLMPrompt system | ✅ | Ready | ADD 16 PROMPTS |
| Admin interface | ✅ | Incomplete | CONNECT |
| Subject routing | ❌ | N/A | CREATE |
| Subject processors | ❌ | N/A | CREATE |
| Management command | ❌ | N/A | CREATE |
| Error handling | ⚠️ | Basic | ENHANCE |
| Progress tracking | ✅ | Present | USE |
| User tracking | ✅ | Present | USE |

---

## DO NOT

```python
❌ DO NOT: Create new text extraction method
    Reason: PDFProcessor.extract_text_from_pdf() exists & works

❌ DO NOT: Create new MCQ generator
    Reason: SubjectMCQGenerator exists & works

❌ DO NOT: Create new PDF model
    Reason: PDFUpload model exists

❌ DO NOT: Create new task tracking
    Reason: ProcessingLog & ProcessingTask exist

❌ DO NOT: Create new admin interface
    Reason: PDFUploadAdmin exists

❌ DO NOT: Duplicate configuration
    Reason: config.py already has PDF settings

❌ DO NOT: Create new prompt storage
    Reason: LLMPrompt model exists & database-driven

❌ DO NOT: Ignore existing user tracking
    Reason: created_by field already integrated everywhere
```

---

## DO

```python
✅ DO: Extend ProcessingLog with 6 new fields
✅ DO: Add 10 new TASK_TYPES to ProcessingLog
✅ DO: Create subject_processor.py (subject-specific logic)
✅ DO: Add 16 new prompts to LLMPrompt table
✅ DO: Enhance SubjectMCQGenerator.save_mcqs_to_subject_table()
✅ DO: Connect PDFUploadAdmin actions to processors
✅ DO: Create management command for CLI access
✅ DO: Test with all 9 subjects
✅ DO: Reuse PDFProcessor.extract_text_from_pdf()
✅ DO: Reuse ProcessingLog for tracking
✅ DO: Reuse LLM configuration (already working)
✅ DO: Leverage existing user authentication
```

---

**CONCLUSION: NO DUPLICATION FOUND. PROCEED WITH EXTENSION APPROACH.**
