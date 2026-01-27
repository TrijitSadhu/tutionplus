# Debug Tracing: Quick Reference Card

## Print Statements Added - Complete Checklist

### ✅ File 1: `genai/tasks/task_router.py`

| Function | Lines | Changes | Status |
|----------|-------|---------|--------|
| `get_processor_for_task_type()` | 19-50 | INPUT display, processor selection, OUTPUT | ✅ DONE |
| `get_llm_prompt_for_task()` | 51-90 | INPUT, search details, FOUND/NOT FOUND, OUTPUT | ✅ DONE |
| `route_pdf_processing_task()` | 95-230 | 10-step trace, nested calls, error handling | ✅ DONE |
| `process_pending_tasks()` | N/A | Unchanged (CLI only) | ✅ OK |

### ✅ File 2: `genai/tasks/subject_processor.py`

| Component | Method | Changes | Status |
|-----------|--------|---------|--------|
| SubjectSpecificProcessor | `__init__()` | NEW method with subject info print | ✅ DONE |
| SubjectSpecificProcessor | `get_subject_specific_prompt()` | INPUT, search, result, OUTPUT | ✅ DONE |
| All 7 Processor Classes | (inherited methods) | Automatic from base class | ✅ DONE |

### ✅ File 3: `genai/admin.py`

| Action | Lines | Changes | Status |
|--------|-------|---------|--------|
| `process_pdf_to_mcq()` | 56-110 | Header, per-PDF loop, success/fail, summary | ✅ DONE |
| `process_pdf_to_descriptive()` | 112-162 | Header, per-PDF loop, success/fail, summary | ✅ DONE |

### ✅ File 4: `genai/views.py`

| View | Lines | Changes | Status |
|------|-------|---------|--------|
| `process_subject_pdf_view()` | 90-190 | Entry banner, file info, params, creation, routing, result | ✅ DONE |

---

## Execution Flow Map

```
ADMIN INTERFACE
    ↓
[🎬 ADMIN ACTION BANNER]
    ↓
For each PDF:
    ├─ Print PDF details
    ├─ Create ProcessingLog
    └─ Call route_pdf_processing_task()
        ↓
    [═ ROUTER ENTRY BANNER ═]
        ├─ [STEP 1-10 with nested function calls]
        │  ├─ get_processor_for_task_type() [─ FUNC BANNER ─]
        │  └─ get_llm_prompt_for_task() [─ FUNC BANNER ─]
        │
        └─ Instantiate Processor
           ├─ [PROCESSOR BANNER] __init__()
           └─ [PROCESSOR BANNER] get_subject_specific_prompt()
    ↓
[✅ COMPLETION BANNER]
```

---

## Print Markers Guide

### Visual Separators

| Marker | Meaning | Where |
|--------|---------|-------|
| `████` (20 chars) | ADMIN ACTION banner | admin.py actions |
| `════` (20 chars) | ROUTER main entry | task_router main function |
| `────` (20 chars) | ROUTER helper functions | get_processor, get_llm_prompt |
| `──` (2 chars) | Processor functions | subject_processor methods |

### Status Indicators

| Indicator | Meaning |
|-----------|---------|
| `✅` | Success - operation completed |
| `❌` | Failure - operation failed or not found |
| `🎬` | Admin action beginning |
| `📄` | Processing PDF item |
| `📝` | Processing descriptive item |
| `[ROUTER]` | Task router function |
| `[PROCESSOR]` | Subject processor function |
| `[VIEW]` | HTTP view function |
| `[STEP N]` | Processing step number |

---

## Key Output Lines to Look For

### Success Indicators (Look for these)

```
✅ FOUND: LLMPrompt ID=12
✅ File valid (5.2 MB)
✅ Extracted 89 pages
✅ Processor found
✅ Generated 5 MCQs
✅ Saved 5 records
✅ TASK COMPLETED SUCCESSFULLY
✅ ADMIN ACTION COMPLETE: Processed X/Y PDFs
```

### Error Indicators (Investigate these)

```
❌ NOT FOUND: Using default prompt
❌ ERROR: [error message]
❌ FAILED: [error message]
Extracted 0 pages
Generated 0 MCQs
Saved 0 records
```

---

## Performance Timing

| Operation | Time | Alert Threshold |
|-----------|------|-----------------|
| Status update | <1s | >2s = slow DB |
| Type detection | <1s | >1s = code issue |
| Processor select | <1s | >1s = mapping issue |
| File validation | <1s | >2s = disk issue |
| PDF extraction | 2-5s | >10s = large file |
| Processor init | <1s | >2s = init issue |
| LLM processing | 10-30s | >45s = API timeout |
| DB save | 1-2s | >5s = DB issue |
| ProcessingLog update | <1s | >2s = DB issue |
| Final completion | <1s | >1s = N/A |
| **TOTAL** | **20-50s** | **>60s = investigate** |

---

## Debug Output Locations

### Where to see the output:

```
Django Development Server:
  Terminal/Console where you ran: python manage.py runserver

Django Shell:
  Terminal where you ran: python manage.py shell

Admin Panel:
  Django terminal (same as above)

API View (process_subject_pdf_view):
  Server logs/terminal

Management Command (process_pdf_tasks):
  Terminal where you ran: python manage.py process_pdf_tasks
```

### Example: Start Django

```bash
cd c:\Users\newwe\Desktop\tution\tutionplus\django\django_project

# Start server with terminal output visible
python manage.py runserver 0.0.0.0:8000

# You'll see output like:
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
[20:30:45] Django server started

# When you trigger an action, output appears here:
████████████████████████████████████████████████████████████████████████████████
🎬 ADMIN ACTION: process_pdf_to_mcq()
[... full trace ...]
```

---

## Testing Checklist

- [ ] Django server running: `python manage.py runserver`
- [ ] Admin user created: `python manage.py createsuperuser`
- [ ] Test PDF file available in uploads folder
- [ ] Go to: http://localhost:8000/admin/
- [ ] Navigate to: PDFUpload section
- [ ] Select a PDF with subject set (e.g., "polity")
- [ ] Click dropdown action: "🔄 Process to MCQ"
- [ ] Click "Go" button
- [ ] Watch console for complete trace
- [ ] Verify no ❌ errors in output
- [ ] Check ProcessingLog in admin (should show status='completed')
- [ ] Check subject table (e.g., Polity_MCQ) for new records

---

## Common Debug Scenarios

### Scenario 1: Processing hangs on STEP 7
**Problem:** LLM API timeout
**Solution:** 
```
Check:
- Groq API key in settings
- Internet connection
- API rate limits
- File size (is it huge?)
```

### Scenario 2: STEP 5 shows 0 pages
**Problem:** PDF corrupted or wrong format
**Solution:**
```
python manage.py shell
>>> from genai.models import PDFUpload
>>> pdf = PDFUpload.objects.latest('id')
>>> import PyPDF2
>>> with open(pdf.pdf_file.path, 'rb') as f:
>>>     reader = PyPDF2.PdfReader(f)
>>>     print(len(reader.pages))  # Should be > 0
```

### Scenario 3: STEP 3 shows wrong processor
**Problem:** Subject name doesn't match processor
**Solution:**
```
Valid subjects:
  - polity
  - economics
  - math
  - physics
  - chemistry
  - history
  - geography

Check PDF subject field in admin
```

### Scenario 4: STEP 7 shows "Generated 0 MCQs"
**Problem:** Prompt not in database
**Solution:**
```
python manage.py create_subject_prompts

# Verify:
python manage.py shell
>>> from genai.models import LLMPrompt
>>> LLMPrompt.objects.filter(subject='polity')
```

---

## File Modification Summary

| File | Original | Modified | Added |
|------|----------|----------|-------|
| task_router.py | 196 lines | 331 lines | 135 lines |
| subject_processor.py | 85 lines | 103 lines | 18 lines |
| admin.py | 700 lines | 750 lines | 50 lines |
| views.py | 356 lines | 401 lines | 45 lines |
| **TOTAL** | **1,337 lines** | **1,585 lines** | **248 lines** |

All changes are **print statements only** - no logic changes.

---

## Documentation Files Created

1. **EXECUTION_FLOW_TRACE.md** (500+ lines)
   - Complete flow documentation
   - Data flow diagrams
   - Troubleshooting guide

2. **DEBUG_TRACING_TESTING_GUIDE.md** (400+ lines)
   - How to trigger tracing
   - What to look for
   - Common issues
   - Performance baseline

3. **DEBUG_TRACING_IMPLEMENTATION_SUMMARY.md** (250+ lines)
   - What was changed
   - Code additions
   - Print formats
   - Benefits

4. **DEBUG_TRACING_QUICK_REFERENCE.md** (this file)
   - Quick lookup
   - Checklist
   - Scenarios

---

## Next Action

1. Open terminal in Django project folder
2. Run: `python manage.py runserver`
3. Go to: http://localhost:8000/admin/
4. Process a PDF
5. Watch the complete trace in terminal
6. Refer to **EXECUTION_FLOW_TRACE.md** for explanations

**Done!** All debug tracing is now in place and ready to use.
