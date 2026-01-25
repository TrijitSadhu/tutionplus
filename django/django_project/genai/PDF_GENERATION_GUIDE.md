# PDF-Based MCQ & Current Affairs Generation Guide

## Overview

You can now generate MCQ and Current Affairs content directly from PDF files through the Django admin panel. No manual URL configuration needed!

## Available Actions

### From URL Sources
- 🚀 **Fetch Both (MCQ & Current Affairs)** - Fetch from configured URL sources
- 📖 **Fetch MCQ Only** - Fetch MCQ from configured URL sources
- 📰 **Fetch Current Affairs Only** - Fetch CA from configured URL sources

### From PDF Files (NEW!)
- 📄 **Generate MCQ from PDF** - Extract text from PDF and generate MCQ
- 📋 **Generate Current Affairs from PDF** - Extract text from PDF and generate CA

---

## How to Use PDF Generation

### Step 1: Go to Processing Log Admin
```
http://localhost:8000/admin/genai/processinglog/
```

### Step 2: Select a Record
- Click any checkbox in the list (the selected record doesn't matter)

### Step 3: Choose PDF Action
- Dropdown menu shows all available actions
- Select either:
  - **📄 Generate MCQ from PDF**
  - **📋 Generate Current Affairs from PDF**

### Step 4: Click "Go"
- The action will:
  1. Ask you to upload a PDF file
  2. Create a new processing task
  3. Start extracting and generating content
  4. Show success message with Task ID

### Step 5: Monitor Progress
- Check the ProcessingLog list to see:
  - Task type (pdf_mcq or pdf_current_affairs)
  - Status (pending → running → completed)
  - Progress bar
  - Duration

---

## Process Flow

### PDF Generation Workflow

```
1. You click action button in admin
          ↓
2. System displays file upload dialog
          ↓
3. You select a PDF file
          ↓
4. System creates ProcessingLog entry
          ↓
5. System stores PDF in PDFUpload model
          ↓
6. Management command processes the PDF:
   - Extracts text from PDF
   - Sends to LLM (Gemini/OpenAI)
   - Generates MCQ or Current Affairs
   - Saves to database
          ↓
7. Processing completes
          ↓
8. View results in admin dashboard
```

---

## Admin Features for PDF Processing

### ProcessingLog List Shows:
- **Task Type Display:**
  - 📄 MCQ Generation from PDF
  - 📋 Current Affairs Generation from PDF
  - 📖 MCQ Fetch from URL
  - 📰 Current Affairs Fetch from URL

- **Status Badges:**
  - ⏳ Pending (Orange)
  - ⚙️ Running (Red)
  - ✅ Completed (Green)
  - ❌ Failed (Dark Red)

- **Progress Bar:**
  - Shows X/Y items processed
  - Updates in real-time

- **Duration:**
  - Shows how long task took
  - Format: 5m 30s or 45s

### Related Records:
Each ProcessingLog entry shows:
- **pdf_upload** - Link to the PDFUpload record if PDF-based
- **Source** - Either URL sources or PDF file
- **Error Message** - Details if task failed
- **Log Details** - Full JSON log of processing

---

## Example: Generate MCQ from Textbook PDF

### Scenario
You have a PDF textbook on "Biology" and want to generate MCQs from it.

### Steps

1. **Upload to Admin:**
   - Go to: `/admin/genai/processinglog/`
   - Select any checkbox
   - Choose: "📄 Generate MCQ from PDF"
   - Upload your Biology_Textbook.pdf

2. **Processing Starts:**
   - System extracts text from PDF
   - Sends to LLM
   - LLM generates MCQs with options and answers
   - Results saved automatically

3. **Monitor Progress:**
   - Go to `/admin/genai/processinglog/`
   - See task with status "Running" → "Completed"
   - View extracted page count
   - Check error message if any

4. **View Results:**
   - Check ProcessingLog entry
   - View log details (JSON format)
   - Verify MCQs were generated

---

## Combining URL & PDF Approaches

You can use both at the same time!

```
┌─────────────────────────────────┐
│   MCQ & Current Affairs System   │
├─────────────────────────────────┤
│                                 │
│  From URLs (ContentSources):    │
│  ✓ Daily API feeds              │
│  ✓ News websites                │
│  ✓ Question banks               │
│                                 │
│  From PDFs:                     │
│  ✓ Textbooks                    │
│  ✓ Study materials              │
│  ✓ Previous papers              │
│                                 │
└─────────────────────────────────┘
```

---

## Task Tracking

### ProcessingLog Fields for PDF Tasks

| Field | Value | Meaning |
|-------|-------|---------|
| **task_type** | pdf_mcq | Generating MCQ from PDF |
| **task_type** | pdf_current_affairs | Generating CA from PDF |
| **status** | running | Currently processing |
| **status** | completed | Successfully finished |
| **status** | failed | Error occurred |
| **pdf_upload** | [Link] | Associated PDF file |
| **started_at** | Timestamp | When task started |
| **completed_at** | Timestamp | When task finished |
| **processed_items** | Number | Pages/items processed |
| **success_count** | Number | Successfully processed |
| **error_count** | Number | Errors during processing |

---

## Performance Tips

✅ **DO:**
- Use clear, well-formatted PDFs for better text extraction
- Keep PDFs under 50MB
- Process one PDF at a time for better resource usage
- Monitor task completion before uploading new PDFs
- Archive completed tasks periodically

❌ **DON'T:**
- Upload scanned images (not readable)
- Upload password-protected PDFs
- Upload very large files (>50MB)
- Interrupt processing midway
- Mix URL and PDF fetches simultaneously (use sequentially)

---

## Troubleshooting PDF Generation

### Issue: "No PDF file provided"
**Solution:** Make sure you select a PDF file before clicking the action button

### Issue: PDF upload fails
**Solution:** 
- Check file size (must be < 50MB)
- Verify file is a valid PDF
- Check PDF is not password-protected

### Issue: Processing shows "failed"
**Solution:**
- Click task to view error message
- Check log details for specific error
- Verify PDF is readable (not scanned image)
- Try with a smaller PDF first

### Issue: No content generated
**Solution:**
- Verify LLM API key is configured (Gemini/OpenAI)
- Check PDF contains readable text (not just images)
- Check error message in ProcessingLog
- Try with a test PDF first

---

## Admin Actions Summary

### From Processing Log List:

**FETCH Actions (from URL sources):**
1. Select checkbox
2. Choose action: "Fetch Both", "Fetch MCQ", or "Fetch CA"
3. Click "Go"
4. System fetches from all active URL sources

**PDF Actions:**
1. Select checkbox
2. Choose action: "Generate MCQ from PDF" or "Generate CA from PDF"
3. Click "Go"
4. Upload a PDF file
5. System processes and generates content

**Management Actions:**
1. Mark Completed - Mark selected tasks as done
2. Mark Failed - Mark selected tasks as failed
3. Clear Error - Clear error messages

---

## API Keys Required

For PDF content generation, ensure these are configured:

### For MCQ Generation:
```python
# .env file
GEMINI_API_KEY=your-key-here
# OR
OPENAI_API_KEY=your-key-here
```

### LLM Selection:
```python
# config.py
DEFAULT_LLM_PROVIDER='gemini'  # or 'openai'
```

---

## Next Steps

1. **Prepare PDFs:**
   - Use clear, readable PDFs
   - Keep under 50MB
   - Ensure text is extractable

2. **Generate Content:**
   - Go to `/admin/genai/processinglog/`
   - Click PDF generation actions
   - Upload files and process

3. **Monitor:**
   - Watch progress in admin list
   - Check status and error messages
   - View generated content in logs

4. **Store Results:**
   - Content is stored in database
   - Can export/download later
   - Full audit trail maintained

---

## Questions?

- Check ProcessingLog error message
- Review task log details (JSON format)
- Check LLM API status
- Verify PDF file is valid

Your PDF generation system is ready to use!
