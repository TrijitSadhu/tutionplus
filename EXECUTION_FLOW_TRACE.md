# PDF to MCQ/Descriptive Processing: Complete Execution Flow Trace

## Overview

This document explains the complete execution flow of PDF processing with detailed debug tracing. Every step, input, and output is now logged to the console for visibility.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ADMIN INTERFACE                                  │
│  /admin/genai/pdfupload/ → Select PDF → 🔄 Process to MCQ/📝 Desc   │
└────────────────┬────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ADMIN ACTION (admin.py)                          │
│  process_pdf_to_mcq() or process_pdf_to_descriptive()               │
│  - For each selected PDF:                                            │
│    * Create ProcessingLog record                                     │
│    * Call route_pdf_processing_task()                                │
└────────────────┬────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    TASK ROUTER (task_router.py)                     │
│  route_pdf_processing_task(processing_log)                           │
│  - 10-step processing pipeline                                       │
│  - MAIN ENTRY POINT for all PDF processing                          │
└────────────────┬────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 SUBJECT PROCESSORS (subject_processor.py)            │
│  PolityProcessor, EconomicsProcessor, MathProcessor, etc.            │
│  - Subject-specific MCQ generation                                   │
│  - Database persistence                                              │
└─────────────────────────────────────────────────────────────────────┘
```

## Execution Path: Admin Action

### Step 1: Admin Panel Selection
```
USER ACTION: Go to /admin/genai/pdfupload/
  - Select one or more PDFs
  - Click "🔄 Process to MCQ" or "📝 Process to Descriptive"
  - Confirm action
```

### Step 2: Admin Action Entry Point

**FILE:** `genai/admin.py`

**FUNCTION:** `process_pdf_to_mcq()` or `process_pdf_to_descriptive()`

**Console Output:**
```
████████████████████████████████████████████████████████████████████████████████
🎬 ADMIN ACTION: process_pdf_to_mcq()
   Selected items: 2
████████████████████████████████████████████████████████████████████████████████

📄 Processing: polity_book.pdf (Subject: polity)
   File: uploads/polity_book.pdf
   ProcessingLog created: ID=42
   Calling route_pdf_processing_task()...

────────────────────────────────────────────────────────────────────────────────
```

**What Happens:**
1. Loop through each selected PDF
2. Create ProcessingLog record
3. Extract subject from PDF object
4. Call `route_pdf_processing_task(log)`
5. Handle success/failure for each PDF

**Print Format:**
```python
print("\n" + "█"*80)
print(f"🎬 ADMIN ACTION: {action_name}()")
print(f"   Selected items: {queryset.count()}")
print("█"*80 + "\n")

# For each PDF:
print(f"📄 Processing: {pdf.title} (Subject: {pdf.subject})")
print(f"   File: {pdf.pdf_file.name}")
print(f"   ProcessingLog created: ID={log.id}")
print(f"   Calling route_pdf_processing_task()...")
```

---

## Execution Path: Task Router (MAIN PROCESSOR)

### Step 3: Task Router Entry Point

**FILE:** `genai/tasks/task_router.py`

**FUNCTION:** `route_pdf_processing_task(processing_log)`

**PURPOSE:** Main dispatcher that coordinates entire PDF processing

**Console Output:**
```
════════════════════════════════════════════════════════════════════════════════
[ROUTER] route_pdf_processing_task() - MAIN ENTRY POINT
  INPUT: task_type=pdf_to_mcq, subject=polity, processing_log_id=42
════════════════════════════════════════════════════════════════════════════════

[STEP 1] Updating ProcessingLog status to 'running'
  ACTION: Mark task as active
  RESULT: ✅ Status updated

[STEP 2] Determining prompt_type from task_type
  INPUT: task_type=pdf_to_mcq
  LOGIC: Extract prompt_type (mcq, descriptive, summary, etc.)
  RESULT: prompt_type=mcq

[STEP 3] Getting processor for task_type
  INPUT: task_type=pdf_to_mcq, subject=polity
  SEARCHING: in processor mapping
  SELECTED: PolityProcessor (class="PolityProcessor", subject="polity")
  RESULT: ✅ Processor found

[STEP 4] Validating PDF file
  INPUT: pdf_upload.id=15
  CHECKING: File exists and readable
  RESULT: ✅ File valid (5.2 MB)

[STEP 5] Extracting content from PDF
  INPUT: start_page=None, end_page=None (full extraction)
  ACTION: Reading all pages
  RESULT: ✅ Extracted 156 pages

[STEP 6] Creating processor instance
  ACTION: Instantiate PolityProcessor
  RESULT: ✅ Processor initialized

[STEP 7] Processing with LLM
  ACTION: Extracting summary and generating MCQs
  RESULT: ✅ Generated 5 MCQs

[STEP 8] Saving results to database
  ACTION: Creating MCQ records in polity_mcq table
  RESULT: ✅ Saved 5 records

[STEP 9] Updating ProcessingLog
  ACTION: Mark as completed with result data
  RESULT: ✅ Updated with 5 items_saved

[STEP 10] Task completion
  ACTION: Final status update
  RESULT: ✅ TASK COMPLETED SUCCESSFULLY

════════════════════════════════════════════════════════════════════════════════
  OUTPUT: task_id=42, subject=polity, items_saved=5
════════════════════════════════════════════════════════════════════════════════
```

### Inside Step 3: Processor Selection

**FUNCTION:** `get_processor_for_task_type()`

```
────────────────────────────────────────────────────────────────────────────────
[ROUTER] get_processor_for_task_type()
  INPUT: task_type=pdf_to_mcq, subject=polity
────────────────────────────────────────────────────────────────────────────────
  Checking processor mapping...
  MATCHED: task_type=pdf_to_mcq → uses subject mapping
  SELECTED: subject=polity → PolityProcessor
  OUTPUT: processor_class=PolityProcessor
────────────────────────────────────────────────────────────────────────────────
```

### Inside Step 7: LLM Prompt Fetching

**FUNCTION:** `get_llm_prompt_for_task()`

```
────────────────────────────────────────────────────────────────────────────────
[ROUTER] get_llm_prompt_for_task()
  INPUT: task_type=pdf_to_mcq, subject=polity, prompt_type=mcq
────────────────────────────────────────────────────────────────────────────────
  SEARCHING: LLMPrompt with source_url=pdf_polity_mcq
  ✅ FOUND: LLMPrompt ID=12
  Retrieved: prompt_text (1850 chars)
  OUTPUT: prompt loaded successfully
────────────────────────────────────────────────────────────────────────────────
```

---

## Execution Path: Subject Processor

### Inside Step 6-8: Subject Processor Execution

**FILE:** `genai/tasks/subject_processor.py`

**CLASS HIERARCHY:**
```
SubjectSpecificProcessor (base class)
├── PolityProcessor
├── EconomicsProcessor
├── MathProcessor
├── PhysicsProcessor
├── ChemistryProcessor
├── HistoryProcessor
└── GeographyProcessor
```

### Processor Initialization

```
────────────────────────────────────────────────────────────────────────────────
[PROCESSOR] PolityProcessor.__init__()
  SUBJECT_NAME: Polity
  SUBJECT_SLUG: polity
────────────────────────────────────────────────────────────────────────────────
```

### Getting Subject-Specific Prompt

**FUNCTION:** `get_subject_specific_prompt()`

```
────────────────────────────────────────────────────────────────────────────────
[PROCESSOR] PolityProcessor.get_subject_specific_prompt()
  INPUT: prompt_type=mcq
────────────────────────────────────────────────────────────────────────────────
  SEARCHING: source_url=pdf_polity_mcq
  ✅ FOUND: LLMPrompt ID=12
  OUTPUT: prompt_text length=1850 chars
────────────────────────────────────────────────────────────────────────────────
```

---

## Execution Path: View-Based Processing

### Alternative: API View Processing

**FILE:** `genai/views.py`

**FUNCTION:** `process_subject_pdf_view()` (POST endpoint)

**Console Output:**
```
════════════════════════════════════════════════════════════════════════════════
[VIEW] process_subject_pdf_view()
════════════════════════════════════════════════════════════════════════════════
  FILE: political_science.pdf (2.5 MB)
  PARAMS: subject=polity, task_type=pdf_to_mcq
          difficulty=medium, format=json, items=5
  Creating PDFUpload record...
  ✅ PDFUpload created: ID=15
  Creating ProcessingLog record...
  ✅ ProcessingLog created: ID=42
  Routing to task processor...
  ✅ Route completed: success=True
  OUTPUT: saved_items=5
════════════════════════════════════════════════════════════════════════════════
```

---

## Complete Console Output Example

Here's what you'll see when processing a PDF to MCQs:

```
████████████████████████████████████████████████████████████████████████████████
🎬 ADMIN ACTION: process_pdf_to_mcq()
   Selected items: 1
████████████████████████████████████████████████████████████████████████████████

📄 Processing: Indian-Polity.pdf (Subject: polity)
   File: uploads/indian-polity.pdf
   ProcessingLog created: ID=42
   Calling route_pdf_processing_task()...

════════════════════════════════════════════════════════════════════════════════
[ROUTER] route_pdf_processing_task() - MAIN ENTRY POINT
  INPUT: task_type=pdf_to_mcq, subject=polity, processing_log_id=42
════════════════════════════════════════════════════════════════════════════════

[STEP 1] Updating ProcessingLog status to 'running'
  ACTION: Mark task as active
  RESULT: ✅ Status updated

[STEP 2] Determining prompt_type from task_type
  INPUT: task_type=pdf_to_mcq
  LOGIC: Extract prompt_type (mcq, descriptive, summary, etc.)
  RESULT: prompt_type=mcq

[STEP 3] Getting processor for task_type
  INPUT: task_type=pdf_to_mcq, subject=polity
────────────────────────────────────────────────────────────────────────────────
[ROUTER] get_processor_for_task_type()
  INPUT: task_type=pdf_to_mcq, subject=polity
────────────────────────────────────────────────────────────────────────────────
  Checking processor mapping...
  MATCHED: task_type=pdf_to_mcq → uses subject mapping
  SELECTED: subject=polity → PolityProcessor
  OUTPUT: processor_class=PolityProcessor

  SELECTED: PolityProcessor (class="PolityProcessor", subject="polity")
  RESULT: ✅ Processor found

[STEP 4] Validating PDF file
  INPUT: pdf_upload.id=25
  CHECKING: File exists and readable
  RESULT: ✅ File valid (3.7 MB)

[STEP 5] Extracting content from PDF
  INPUT: start_page=None, end_page=None (full extraction)
  ACTION: Reading all pages
  RESULT: ✅ Extracted 89 pages

[STEP 6] Creating processor instance
────────────────────────────────────────────────────────────────────────────────
[PROCESSOR] PolityProcessor.__init__()
  SUBJECT_NAME: Polity
  SUBJECT_SLUG: polity

  ACTION: Instantiate PolityProcessor
  RESULT: ✅ Processor initialized

[STEP 7] Processing with LLM
  ACTION: Extracting summary and generating MCQs
  Getting prompt...
────────────────────────────────────────────────────────────────────────────────
[PROCESSOR] PolityProcessor.get_subject_specific_prompt()
  INPUT: prompt_type=mcq
────────────────────────────────────────────────────────────────────────────────
  SEARCHING: source_url=pdf_polity_mcq
  ✅ FOUND: LLMPrompt ID=12
  OUTPUT: prompt_text length=1850 chars

  RESULT: ✅ Generated 5 MCQs

[STEP 8] Saving results to database
  ACTION: Creating MCQ records in polity_mcq table
  RESULT: ✅ Saved 5 records

[STEP 9] Updating ProcessingLog
  ACTION: Mark as completed with result data
  RESULT: ✅ Updated with 5 items_saved

[STEP 10] Task completion
  ACTION: Final status update
  RESULT: ✅ TASK COMPLETED SUCCESSFULLY

════════════════════════════════════════════════════════════════════════════════
  OUTPUT: task_id=42, subject=polity, items_saved=5
════════════════════════════════════════════════════════════════════════════════

   ✅ SUCCESS: 5 MCQs generated successfully

████████████████████████████████████████████████████████████████████████████████
✅ ADMIN ACTION COMPLETE: Processed 1/1 PDFs
████████████████████████████████████████████████████████████████████████████████
```

---

## Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                         INPUT                                        │
│  PDFUpload(title, subject, pdf_file)                                 │
│  Request: task_type, subject, num_items, etc.                        │
└─────────────────────────┬──────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  ADMIN ACTION LAYER                                  │
│  process_pdf_to_mcq() / process_pdf_to_descriptive()                │
│  ✓ Create ProcessingLog(task_type, subject, status='pending')       │
└─────────────────────────┬──────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────┐
│              ROUTER/DISPATCHER LAYER                                 │
│  route_pdf_processing_task(processing_log)                           │
│  ✓ Determine prompt_type                                             │
│  ✓ Select processor based on task_type + subject                     │
│  ✓ Extract PDF content                                               │
│  ✓ Fetch LLM prompt from database                                    │
│  ✓ Call subject-specific processor                                   │
└─────────────────────────┬──────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────┐
│          SUBJECT PROCESSOR LAYER                                     │
│  PolityProcessor / EconomicsProcessor / etc.                         │
│  ✓ Get subject-specific LLM prompt                                   │
│  ✓ Call LLM with extracted content + prompt                          │
│  ✓ Parse response                                                    │
│  ✓ Save to subject-specific table (e.g., polity_mcq)               │
└─────────────────────────┬──────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        OUTPUT                                        │
│  ProcessingLog: status='completed', items_saved=5                    │
│  Subject Table: 5 MCQ records (polity_mcq, economics_mcq, etc.)     │
│  Response: {success: true, saved_items: 5, task_id: 42}            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## How to Read the Debug Output

### 1. Top-Level Execution (Admin Action)
```
████████████ (visual separator)
🎬 ADMIN ACTION: process_pdf_to_mcq()
   Selected items: 2
████████████
```
**Meaning:** User clicked "Process to MCQ" and 2 PDFs were selected

### 2. Per-PDF Processing
```
📄 Processing: filename.pdf (Subject: polity)
   File: path/to/file
   ProcessingLog created: ID=42
   Calling route_pdf_processing_task()...
```
**Meaning:** For this specific PDF, a ProcessingLog was created and routing started

### 3. Router Entry Point
```
════════════ MAIN ENTRY POINT ════════════
[ROUTER] route_pdf_processing_task()
  INPUT: task_type=pdf_to_mcq, subject=polity
════════════════════════════════
```
**Meaning:** Entering the main task router function

### 4. Processing Steps
```
[STEP 1] Updating ProcessingLog status to 'running'
  RESULT: ✅ Status updated

[STEP 2] Determining prompt_type...
  RESULT: prompt_type=mcq
```
**Meaning:** Each numbered step shows a logical processing phase

### 5. Nested Function Calls
```
────────────────────────────────────────────
[ROUTER] get_processor_for_task_type()
  INPUT: task_type=pdf_to_mcq
────────────────────────────────────────────
  SELECTED: PolityProcessor
```
**Meaning:** When a function calls another function, it's clearly indented

### 6. Processor Execution
```
────────────────────────────────────────────
[PROCESSOR] PolityProcessor.__init__()
  SUBJECT_NAME: Polity
  SUBJECT_SLUG: polity
```
**Meaning:** Subject processor being instantiated with its configuration

### 7. Final Result
```
════════════ OUTPUT ════════════
  OUTPUT: task_id=42, items_saved=5
════════════════════════════════
```
**Meaning:** Successful completion with results

---

## Troubleshooting Guide

### If you see: "❌ NOT FOUND: Using default prompt"
**Problem:** LLMPrompt not found in database
**Solution:** Run `python manage.py create_subject_prompts` to create prompts

### If you see: "❌ File valid" (step 4 fails)
**Problem:** PDF file doesn't exist or isn't readable
**Solution:** Check file path in admin, ensure file uploaded successfully

### If you see: "STEP 3" shows different processor
**Problem:** Wrong subject assignment
**Solution:** Verify subject field on PDFUpload in admin

### If you see: "STEP 8" shows fewer items than expected
**Problem:** LLM didn't generate expected number
**Solution:** Check LLM prompt quality, try different model via settings

---

## Performance Notes

- **STEP 1:** Instant (database write)
- **STEP 2:** Instant (string extraction)
- **STEP 3:** Instant (dictionary lookup)
- **STEP 4:** < 1 sec (file check)
- **STEP 5:** 2-5 sec (PDF parsing, depends on file size)
- **STEP 6:** < 1 sec (class instantiation)
- **STEP 7:** 10-30 sec (LLM API call)
- **STEP 8:** 1-2 sec (database writes)
- **STEP 9:** < 1 sec (update ProcessingLog)
- **STEP 10:** < 1 sec (final status)

**Total Time:** Usually 20-50 seconds per PDF

---

## Summary

The complete execution flow is now fully visible in the console:

1. **ADMIN LAYER:** Shows user action and PDF selection
2. **ROUTER LAYER:** Shows 10-step processing with clear separators
3. **PROCESSOR LAYER:** Shows subject-specific configuration and execution
4. **VIEW LAYER:** Shows alternative API-based processing

Each level provides INPUT → PROCESSING → OUTPUT visibility, making it easy to track the exact flow of data through the system.
