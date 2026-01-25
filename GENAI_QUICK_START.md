# GenAI Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup API Keys (2 minutes)

Create file: `.env` in root folder
```
Location: C:\Users\newwe\Desktop\tution\tutionplus\.env
```

**Get GEMINI Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy it

**Get OpenAI Key (Optional):**
1. Visit: https://platform.openai.com/account/api-keys
2. Create new secret key
3. Copy it

**Fill .env file:**
```bash
DEFAULT_LLM_PROVIDER=gemini
GEMINI_API_KEY=AIzaSy_YOUR_KEY_HERE
OPENAI_API_KEY=sk-YOUR_KEY_HERE
```

### Step 2: Start Django Server (1 minute)

```powershell
# Open PowerShell
cd c:\Users\newwe\Desktop\tution\tutionplus

# Activate venv
& '.\env\Scripts\Activate.ps1'

# Start server
cd django\django_project
python manage.py runserver 0.0.0.0:8000
```

### Step 3: Access Admin Panel (1 minute)

Open: http://localhost:8000/admin/
- Login with admin account
- Look for "GenAI" in left sidebar

### Step 4: Try Your First Feature (1 minute)

**Option A: Upload a PDF**
```
GenAI → PDF Uploads → Add PDF Upload
  - Title: "My Chapter"
  - Subject: Select one
  - Upload: Your PDF file
  - Click Save

Watch status change: ⏳ → ✓
Takes ~30-60 seconds depending on PDF size
```

**Option B: Generate Current Affairs**
```
GenAI → Current Affairs → Add
  - Topic: "Budget 2026"
  - Click Save

Instantly generated MCQ + descriptive answer!
```

---

## 📊 What Each Feature Does

| Feature | Input | Output | Time |
|---------|-------|--------|------|
| **PDF Upload** | PDF file | 50-100 MCQs | 30-60s |
| **Current Affairs** | Topic name | 5 MCQs + Answer | 5-10s |
| **Math Problem** | Math expression | LaTeX + MCQ | 2-5s |

---

## 🔍 Monitor Your Work

**View all operations:**
```
Admin → GenAI → Processing Tasks

Shows:
  ✓ What was processed
  ✓ How long it took
  ✓ Success or failure
  ✓ Input/output data
```

---

## 💡 Common First Steps

### I want to create MCQs from my textbook PDFs

```
1. Have your PDF ready
2. Visit: Admin → GenAI → PDF Uploads
3. Click "Add PDF Upload"
4. Upload the PDF
5. Wait for processing (green ✓)
6. Copy the generated MCQs
7. Paste to your test/question bank

Time: ~2 minutes per PDF
Result: 50-100 professional MCQs
```

### I want to generate current affairs questions weekly

```
1. Create a recurring task in your schedule
2. Visit: Admin → GenAI → Current Affairs
3. Add new topic (e.g., "This Week's News")
4. System auto-generates content
5. Review and publish
6. Students access questions

Time: ~5 minutes
Frequency: Weekly
Effort: Minimal
```

### I want to include math problems with proper formatting

```
1. Visit: Admin → GenAI → Math Problems
2. Add: "Solve x² - 5x + 6 = 0"
3. Difficulty: Medium
4. System creates:
   - LaTeX version: $x^2 - 5x + 6 = 0$
   - MCQ version with 4 options
5. Copy/Export for use

Time: ~5 seconds
Quality: Professional
Reusable: Yes
```

---

## 🎯 Real-World Workflow Example

### Scenario: Create a 100-question biology test

**Timeline:**

**Monday 9:00 AM**
- Visit Admin → GenAI → PDF Uploads
- Upload: "Biology_Textbook_Ch5.pdf" (50 pages)
- Click Save

**Monday 9:15 AM**
- Refresh page
- Status = ✓ Completed
- 100 MCQs generated

**Monday 9:20 AM**
- Copy generated MCQs
- Paste to question bank
- Select 50 best ones

**Monday 9:30 AM**
- Create test with selected MCQs
- Publish to students

**Monday 10:00 AM**
- 200 students take test
- Analytics auto-generate

**Result:**
```
Time spent: 30 minutes
MCQs created: 100
Questions good enough to use: 50
Manual creation time: 3-4 hours
Time saved: 3.5 hours
```

---

## ⚡ Tips & Tricks

### Tip 1: Use Bulk Import
Instead of manual copy-paste, export as CSV:
```
Admin → PDF Uploads → Export Selected → CSV
Then bulk import to your main database
```

### Tip 2: Set Difficulty Levels
Math problems auto-tagged by difficulty:
- Easy: Basic concepts
- Medium: Multi-step problems
- Hard: Complex scenarios

Use this for progressive difficulty in tests!

### Tip 3: Monitor Performance
Keep an eye on Processing Tasks:
```
Admin → Processing Tasks

Track:
  - Average processing time
  - Success rate
  - Peak usage times
```

### Tip 4: Use Multiple Topics
For current affairs, create entries for different categories:
```
- "Politics - Union Budget"
- "Economy - Stock Market"
- "Science - Space Mission"
- "Sports - Olympics"
```

---

## 🔧 Troubleshooting

**Problem: API Key not working**
```
Solution:
  1. Check .env file exists in root folder
  2. Verify key is copied completely
  3. Restart Django server
  4. Check console for error messages
```

**Problem: Processing takes very long**
```
Solution:
  1. Check PDF file size (>50MB is slow)
  2. Try splitting PDF into chapters
  3. Monitor with Processing Tasks
  4. Check server logs for errors
```

**Problem: Generated content is not good quality**
```
Solution:
  1. Try OpenAI provider (fallback)
  2. Adjust TEMPERATURE in .env (0=deterministic, 1=creative)
  3. Include more context in prompts
  4. Review and manually improve
```

**Problem: "API Quota Exceeded"**
```
Solution:
  1. Gemini free tier: 60 requests/minute
  2. OpenAI free tier: Limited credits
  3. Check provider dashboard for usage
  4. Upgrade plan if needed
  5. System automatically falls back to OpenAI
```

---

## 📚 Documentation Files

In your project root, you have:

| File | Purpose |
|------|---------|
| `GENAI_WORKFLOW_GUIDE.md` | Complete detailed guide (read this first!) |
| `GENAI_CODE_FLOW.md` | Technical code flow explanation |
| `GENAI_EXAMPLES.py` | Practical examples (run with Python) |
| `GENAI_QUICK_START.md` | This file - quick reference |

---

## ✅ Checklist: Are You Ready?

- [ ] Virtual environment activated (Python 3.11)
- [ ] .env file created with API keys
- [ ] Django server running without errors
- [ ] Can access http://localhost:8000/admin/
- [ ] Can see "GenAI" section in admin
- [ ] Tried uploading a PDF or creating current affairs entry
- [ ] Got green ✓ status on a task
- [ ] Can see results in Processing Tasks

If all checked ✓, **you're ready to use GenAI!**

---

## 🚀 Next Steps

1. **Create your first content**
   - Upload a real PDF from your course
   - Generate MCQs
   - Review quality

2. **Configure your workflow**
   - Set up regular uploads
   - Create current affairs entries
   - Publish to students

3. **Monitor & Optimize**
   - Check Processing Tasks daily
   - Track quality metrics
   - Adjust difficulty levels

4. **Scale Up**
   - Automate with cron jobs
   - Batch process multiple PDFs
   - Integrate with your main database

---

## 💬 Quick Reference Commands

```powershell
# Start server
cd c:\Users\newwe\Desktop\tution\tutionplus\django\django_project
& 'C:\Users\newwe\Desktop\tution\tutionplus\env\Scripts\Activate.ps1'
python manage.py runserver 0.0.0.0:8000

# View admin
http://localhost:8000/admin/

# View GenAI section
http://localhost:8000/admin/genai/

# View processing tasks
http://localhost:8000/admin/genai/processingtask/

# Check database
python manage.py shell
>>> from genai.models import PDFUpload
>>> PDFUpload.objects.all()
```

---

## 📞 Need Help?

Check these files in order:
1. **GENAI_QUICK_START.md** (this file) - Quick answers
2. **GENAI_WORKFLOW_GUIDE.md** - Detailed workflow
3. **GENAI_CODE_FLOW.md** - How it works technically
4. **Django Admin** - See your data directly
5. **Server logs** - Error messages help diagnose issues

---

**Congratulations! You have a fully functional AI content generation system!** 🎉

Start with the quick steps above, and you'll have your first AI-generated MCQs in minutes!
