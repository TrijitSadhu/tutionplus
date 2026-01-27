# Debug Tracing: Testing Guide

## Quick Start - See the Full Execution Flow

### Option 1: Via Admin Panel (Easiest)

```bash
1. Start Django server:
   python manage.py runserver

2. Go to Admin:
   http://localhost:8000/admin/
   Login with superuser credentials

3. Navigate to PDF Upload:
   Click "PDFUpload" in left menu
   
4. Add or Select PDF:
   - If no PDFs exist: Click "Add PDF Upload"
   - Upload a test PDF file
   - Set Subject to "polity" (or any subject)
   - Click "Save"
   
5. Process the PDF:
   - Go back to PDFUpload list
   - Select the PDF you just created
   - Click dropdown: "🔄 Process to MCQ"
   - Click "Go"
   
6. Watch Terminal Output:
   You'll see complete execution trace with:
   ✓ ADMIN ACTION header
   ✓ 10-step ROUTER trace
   ✓ PROCESSOR initialization
   ✓ Final completion status
```

### Option 2: Via API (For Automation)

```bash
curl -X POST http://localhost:8000/api/process-pdf/ \
  -H "Content-Type: multipart/form-data" \
  -F "pdf_file=@path/to/file.pdf" \
  -F "subject=polity" \
  -F "task_type=pdf_to_mcq" \
  -F "num_items=5"
```

### Option 3: Via Management Command

```bash
python manage.py process_pdf_tasks --task_type=pdf_to_mcq --limit=1
```

---

## What to Look For in Output

### 1. ADMIN ACTION Header (Green Banner)
```
████████████████████████████████████████████████████████████████████████████████
🎬 ADMIN ACTION: process_pdf_to_mcq()
   Selected items: 1
████████████████████████████████████████████████████████████████████████████████
```
✓ This shows you're in the admin action

### 2. Per-PDF Processing
```
📄 Processing: filename.pdf (Subject: polity)
   File: uploads/filename.pdf
   ProcessingLog created: ID=42
   Calling route_pdf_processing_task()...
```
✓ Shows which PDF is being processed
✓ Shows ProcessingLog ID (use this to track in database)

### 3. Router Entry Point (Blue Banner)
```
════════════════════════════════════════════════════════════════════════════════
[ROUTER] route_pdf_processing_task() - MAIN ENTRY POINT
  INPUT: task_type=pdf_to_mcq, subject=polity, processing_log_id=42
════════════════════════════════════════════════════════════════════════════════
```
✓ This is where processing actually starts

### 4. 10-Step Processing (Numbered)
```
[STEP 1] Updating ProcessingLog status to 'running'
  RESULT: ✅ Status updated

[STEP 2] Determining prompt_type from task_type
  RESULT: prompt_type=mcq

[STEP 3] Getting processor for task_type
  SELECTED: PolityProcessor
  RESULT: ✅ Processor found

[STEP 4] Validating PDF file
  RESULT: ✅ File valid (5.2 MB)

[STEP 5] Extracting content from PDF
  RESULT: ✅ Extracted 156 pages

[STEP 6] Creating processor instance
  RESULT: ✅ Processor initialized

[STEP 7] Processing with LLM
  RESULT: ✅ Generated 5 MCQs

[STEP 8] Saving results to database
  RESULT: ✅ Saved 5 records

[STEP 9] Updating ProcessingLog
  RESULT: ✅ Updated with 5 items_saved

[STEP 10] Task completion
  RESULT: ✅ TASK COMPLETED SUCCESSFULLY
```
✓ Each step shows progress
✓ Look for ✅ (success) or ❌ (failure)

### 5. Final Summary
```
████████████████████████████████████████████████████████████████████████████████
✅ ADMIN ACTION COMPLETE: Processed 1/1 PDFs
████████████████████████████████████████████████████████████████████████████████
```
✓ Shows how many PDFs were successfully processed

---

## Common Issues and How to Fix Them

### Issue 1: STEP 3 shows wrong processor
```
SELECTED: EconomicsProcessor (but expected PolityProcessor)
```
**Cause:** PDF subject field not set correctly
**Fix:** 
```python
# In admin, check the "subject" field on the PDF
# Make sure it matches: polity, economics, math, physics, chemistry, history, geography
```

### Issue 2: STEP 5 shows "Extracted 0 pages"
```
RESULT: ✅ Extracted 0 pages
```
**Cause:** PDF is corrupted or empty
**Fix:**
```bash
# Test the PDF manually:
python
>>> import PyPDF2
>>> with open('uploads/file.pdf', 'rb') as f:
>>>     reader = PyPDF2.PdfReader(f)
>>>     print(len(reader.pages))  # Should be > 0
```

### Issue 3: STEP 7 shows "Generated 0 MCQs"
```
RESULT: ✅ Generated 0 MCQs
```
**Cause 1:** LLMPrompt not found in database
**Cause 2:** LLM API returned empty
**Fix:**
```bash
# Create missing prompts:
python manage.py create_subject_prompts

# Check database:
python manage.py shell
>>> from genai.models import LLMPrompt
>>> LLMPrompt.objects.filter(subject='polity', prompt_type='mcq')
# Should return at least 1 result
```

### Issue 4: STEP 8 shows fewer items than expected
```
RESULT: ✅ Saved 3 records  (expected 5)
```
**Cause:** LLM didn't generate enough items
**Fix:**
```python
# Check LLM prompt quality in admin
# Increase num_items in ProcessingLog
# Try different LLM model via settings.py
```

### Issue 5: See "❌ Error" in output
```
❌ ERROR: [Some error message]
```
**Cause:** Check the full error message
**Fix:**
```bash
# Run with Django logging enabled:
python manage.py runserver --verbosity=2

# Or check logs:
tail -f logs/django.log
```

---

## Database Verification

After processing, verify results:

```bash
python manage.py shell

# Check ProcessingLog was created:
from genai.models import ProcessingLog
log = ProcessingLog.objects.latest('id')
print(f"Task ID: {log.id}")
print(f"Subject: {log.subject}")
print(f"Task Type: {log.task_type}")
print(f"Status: {log.status}")
print(f"Items Saved: {log.items_saved}")

# Check MCQs were saved:
# Example for Polity subject:
from genai.models import Polity_MCQ  # or Economics_MCQ, Math_MCQ, etc.
mcqs = Polity_MCQ.objects.filter(pdf_upload__title='your_file.pdf')
print(f"Total MCQs: {mcqs.count()}")
for mcq in mcqs:
    print(f"  - {mcq.question[:50]}...")
```

---

## File Locations for Debug Output

The debug output is sent to **standard output (stdout)** during execution.

### For Django runserver:
```
Python terminal where you ran: python manage.py runserver
```

### For Gunicorn/Production:
```
Application logs or stdout capture file
Check your deployment's log configuration
```

### For Background Tasks:
```
If using Celery or async tasks:
Check Celery worker logs
Or use: celery -A django_project inspect active
```

---

## Sample Complete Output

Here's what a complete, successful run looks like:

```
████████████████████████████████████████████████████████████████████████████████
🎬 ADMIN ACTION: process_pdf_to_mcq()
   Selected items: 1
████████████████████████████████████████████████████████████████████████████████

📄 Processing: Indian-Polity-Chapter1.pdf (Subject: polity)
   File: uploads/pdfs/Indian-Polity-Chapter1.pdf
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

## Performance Baseline

Typical execution times for one PDF:

| Step | Component | Time | Notes |
|------|-----------|------|-------|
| 1 | Status update | <1s | Database write |
| 2 | Type detection | <1s | String operation |
| 3 | Processor selection | <1s | Dictionary lookup |
| 4 | File validation | <1s | File check |
| 5 | PDF extraction | 2-5s | Depends on PDF size |
| 6 | Processor init | <1s | Class instantiation |
| 7 | LLM processing | 10-30s | API call to Groq/Gemini |
| 8 | Database save | 1-2s | Multiple INSERT statements |
| 9 | ProcessingLog update | <1s | Database update |
| 10 | Final completion | <1s | Status update |
| **TOTAL** | **Complete flow** | **20-50s** | **Full MCQ generation** |

---

## Next Steps

1. **Run a test:** Follow "Option 1" above
2. **Watch the output:** Look for the 10-step trace
3. **Verify in database:** Use the shell commands above
4. **Check admin:** View results in /admin/genai/processinglog/

Questions? Check `EXECUTION_FLOW_TRACE.md` for detailed documentation.
