# Quick Reference - Admin Panel Usage

## Access Admin Panel
```
URL: http://localhost:8000/admin/
Login with your Django superuser credentials
```

---

## Step 1: Upload a PDF ⬆️

**Go to:** GenAI → PDF Uploads → Add PDF Upload

**Fill in:**
| Field | Example | Required |
|-------|---------|----------|
| Title | History Chapter 5 | ✓ |
| Subject | [Dropdown: Polity, Economics, Math, Physics, Chemistry, History, Geography, Biology, Other] | ✓ |
| PDF file | Select file | ✓ |
| Description | Covers independence & constitutions | ✗ |

**Click:** Save

---

## Step 2: Process the PDF 🔄

**Go to:** GenAI → PDF Uploads → Find your PDF

**Select the PDF** → Choose from Actions dropdown:

### Option A: MCQ Generation 📊
1. Check box next to your PDF
2. Select **"🔄 Process to MCQ"**
3. Click **"Go"**
4. Done! MCQs will be generated

### Option B: Descriptive Generation 📝
1. Check box next to your PDF
2. Select **"📝 Process to Descriptive"**
3. Click **"Go"**
4. Done! Descriptive answers will be generated

---

## Step 3: Monitor Progress 📈

**Go to:** GenAI → Processing Logs

**You'll see:**
| Column | Shows |
|--------|-------|
| ID | Task number |
| Task Type | pdf_to_mcq or pdf_to_descriptive |
| Subject | polity, economics, etc. |
| Status | ⏳ Pending / ⚙️ Running / ✅ Completed / ❌ Failed |
| Difficulty | Easy / Medium / Hard |
| Num Items | How many MCQs generated |
| Created At | When task started |

---

## Step 4: View Task Details 🔍

**Click on any task** to see full details:

### Task Information
- Task Type: pdf_to_mcq
- Status: ✅ Completed
- Created By: your_username

### Subject Routing
- Subject: polity
- Difficulty: medium
- Output Format: json
- Num Items: 5

### PDF Processing Options
- Start Page: (optional)
- End Page: (optional)

### Progress Tracking
- Total Items: 5
- Processed Items: 5
- Success Count: 5
- Error Count: 0

### Status Details
- MCQ Status: Generated 5 MCQs
- Error Message: (none if successful)

---

## Understanding Task Types

When you click **"🔄 Process to MCQ"**, here's what happens behind the scenes:

```
Subject: Polity
    ↓
Task Type: pdf_to_mcq → PolityProcessor
    ↓
LLM Prompt: pdf_to_polity_mcq (from database)
    ↓
Difficulty: Medium
    ↓
Generates: 5 MCQs
    ↓
Output Format: JSON
    ↓
Saved ✓
```

---

## Subject Details

Each subject has its own processor and LLM prompts:

| Subject | Processor | MCQ Prompt | Desc Prompt | Status |
|---------|-----------|-----------|------------|--------|
| Polity | PolityProcessor | pdf_polity_mcq | pdf_polity_desc | ✓ |
| Economics | EconomicsProcessor | pdf_economics_mcq | pdf_economics_desc | ✓ |
| Math | MathProcessor | pdf_math_mcq | pdf_math_desc | ✓ |
| Physics | PhysicsProcessor | pdf_physics_mcq | pdf_physics_desc | ✓ |
| Chemistry | ChemistryProcessor | pdf_chemistry_mcq | pdf_chemistry_desc | ✓ |
| History | HistoryProcessor | pdf_history_mcq | pdf_history_desc | ✓ |
| Geography | GeographyProcessor | pdf_geography_mcq | pdf_geography_desc | ✓ |
| Biology | BiologyProcessor | pdf_biology_mcq | pdf_biology_desc | ✓ |

---

## Output Options

When a task completes, it generates content in chosen format:

**MCQ Output (JSON):**
```json
[
  {
    "question": "When was the Constitution of India adopted?",
    "options": [
      "A) 1947",
      "B) 1950",
      "C) 1951",
      "D) 1952"
    ],
    "correct": "B"
  },
  ...
]
```

**Descriptive Output (Markdown):**
```markdown
## Question 1: Describe the Indian Constitution

Answer: The Indian Constitution is...
(150-250 words)

## Question 2: What are Fundamental Rights?

Answer: Fundamental Rights are...
(150-250 words)
```

---

## Troubleshooting

### Task Status is "Pending" but not moving
1. Check if ProcessingLog status is still "pending"
2. Run: `python manage.py process_pdf_tasks` in terminal
3. Refresh the page

### No MCQs Generated
1. Check Error Message field in task details
2. Verify PDF is readable (try uploading again)
3. Check if subject matches a valid option

### Task shows "Failed"
1. Click on the task
2. Look at "Error Message" field
3. Common issues:
   - Invalid PDF format
   - Empty PDF file
   - Wrong subject selected

---

## File Organization

All your PDFs are stored here:
```
media/genai/pdfs/YYYY/MM/DD/filename.pdf
```

Generated content is stored in database tables based on subject.

---

## Tips & Best Practices

✅ **DO:**
- Ensure PDF has clear, readable text
- Select the correct subject before processing
- Monitor task in Processing Logs
- Check error messages if task fails
- Use Medium difficulty for general content

❌ **DON'T:**
- Upload image-only PDFs (need OCR)
- Select wrong subject (affects LLM prompt)
- Process same PDF twice immediately
- Ignore error messages

---

## Quick Checklist

- [ ] PDF uploaded? ⬆️
- [ ] Subject selected? 📚
- [ ] Action chosen? (MCQ or Descriptive) 🔄
- [ ] Task created? (check Processing Logs) 📈
- [ ] Status showing completed? ✅
- [ ] Success count > 0? 📊

---

## Need Help?

**Check Processing Logs for:**
- ⏳ Pending = waiting to start
- ⚙️ Running = currently processing
- ✅ Completed = done successfully
- ❌ Failed = error occurred (see error message)

**Click on task to see:**
- Full error message
- Subject and difficulty used
- Number of items generated
- Who created the task (created_by)

---

## Summary

1. **Upload PDF** → Choose subject
2. **Select Action** → MCQ or Descriptive
3. **Monitor Task** → Check status in Processing Logs
4. **View Results** → Click task for details
5. **Done!** ✅

Everything works from the admin panel. No coding needed!
