# Debug Tracing: One-Page Quick Start

## Start Here (60 seconds)

```
✅ STATUS: Implementation Complete

4 Python files enhanced
6 documentation files created
335 lines of print statements added
Zero logic changes made

Ready to test immediately!
```

---

## 5-Minute Test

### Step 1: Open Terminal
```bash
cd c:\Users\newwe\Desktop\tution\tutionplus\django\django_project
```

### Step 2: Start Django
```bash
python manage.py runserver
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 3: Open Admin
Navigate to: `http://localhost:8000/admin/`
- Login with your superuser credentials

### Step 4: Go to PDFUpload
- Click "PDFUpload" in left menu
- Select a PDF (or add one)
- Make sure it has a subject set (e.g., "polity")

### Step 5: Process PDF
- Select the PDF
- Click dropdown: "🔄 Process to MCQ"
- Click "Go"

### Step 6: Watch Output
Terminal shows:
```
████████████████████████████████████████████████████████████████████████████████
🎬 ADMIN ACTION: process_pdf_to_mcq()
   Selected items: 1
████████████████████████████████████████████████████████████████████████████████

📄 Processing: filename.pdf (Subject: polity)
   File: uploads/filename.pdf
   ProcessingLog created: ID=42
   Calling route_pdf_processing_task()...

════════════════════════════════════════════════════════════════════════════════
[ROUTER] route_pdf_processing_task() - MAIN ENTRY POINT
  INPUT: task_type=pdf_to_mcq, subject=polity, processing_log_id=42
════════════════════════════════════════════════════════════════════════════════

[STEP 1] Updating ProcessingLog status to 'running'
  RESULT: ✅ Status updated

[STEP 2] Determining prompt_type from task_type
  RESULT: prompt_type=mcq

[STEP 3] Getting processor for task_type
  RESULT: ✅ Processor found

[STEP 4] Validating PDF file
  RESULT: ✅ File valid (5.2 MB)

[STEP 5] Extracting content from PDF
  RESULT: ✅ Extracted 89 pages

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

════════════════════════════════════════════════════════════════════════════════
  OUTPUT: task_id=42, subject=polity, items_saved=5
════════════════════════════════════════════════════════════════════════════════

   ✅ SUCCESS: 5 MCQs generated successfully

████████████████████████████████████████████████████████████████████████████████
✅ ADMIN ACTION COMPLETE: Processed 1/1 PDFs
████████████████████████████████████████████████████████████████████████████████
```

### Success! ✅

You're seeing the complete execution trace with all 10 processing steps.

---

## What to Look For

| Indicator | Meaning |
|-----------|---------|
| ✅ | Success - operation completed |
| ❌ | Failure - investigate this |
| [STEP N] | Processing step number |
| INPUT: | What function received |
| OUTPUT: | What function returned |

---

## If Something Goes Wrong

### Issue: No output appears
**Fix:** Make sure Django is running in the terminal

### Issue: Wrong processor selected
**Fix:** Check PDF subject field in admin (should be "polity", "economics", etc.)

### Issue: STEP 7 shows "Generated 0 MCQs"
**Fix:** Run `python manage.py create_subject_prompts`

### Issue: Timeout or error
**Check:** Internet, API key, file size

---

## Documentation Files

| File | Use When |
|------|----------|
| EXECUTION_FLOW_TRACE.md | You want to understand HOW it works |
| DEBUG_TRACING_TESTING_GUIDE.md | You have issues to debug |
| DEBUG_TRACING_QUICK_REFERENCE.md | You need quick answers |
| DEBUG_TRACING_IMPLEMENTATION_SUMMARY.md | You want technical details |

---

## Files Modified

- ✅ `genai/tasks/task_router.py` (170 lines added)
- ✅ `genai/tasks/subject_processor.py` (20 lines added)
- ✅ `genai/admin.py` (100 lines added)
- ✅ `genai/views.py` (45 lines added)

---

## Key Features

✅ Complete visibility into PDF processing
✅ 10-step processing trace
✅ Input/output for each function
✅ Processor selection tracking
✅ LLM prompt fetching visible
✅ Database save confirmation
✅ Success/failure indicators
✅ Performance tracking possible

---

## That's It!

You now have complete debug tracing for the entire PDF-to-MCQ processing pipeline.

Every step, input, and output is visible in the console.

**Start testing now!** 🚀

---

For more details, see the comprehensive documentation files created.
