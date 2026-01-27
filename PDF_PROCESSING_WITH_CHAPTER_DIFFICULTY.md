# PDF Processing with Chapter & Difficulty Selection

## Overview

You can now select **Chapter** and **Difficulty Level** before processing PDFs for subjects like Polity. This feature allows fine-grained control over generated MCQs and descriptive answers.

---

## How to Use

### Step 1: Go to Admin Panel
```
1. Navigate to: http://localhost:8000/admin/
2. Click on "PDFUpload" in the left menu
3. Select one or more PDFs you want to process
```

### Step 2: Select Action
```
1. At the bottom of the PDF list, you'll see a dropdown menu
2. Select either:
   - "🔄 Process to MCQ" (for Multiple Choice Questions)
   - "📝 Process to Descriptive" (for Descriptive Answers)
3. Click the "Go" button
```

### Step 3: Configure Options
You'll be redirected to a form where you can configure:

#### Chapter Selection (Optional)
- **Chapters Available:** 1-41
- **Default:** Leave blank to process entire PDF without chapter filtering
- **Use Case:** Select specific chapter to generate questions only from that chapter

**Example:**
```
If you select Chapter 5, questions will be generated only from Chapter 5 content
```

#### Difficulty Level (Optional)
- **Options:** Easy, Medium, Hard
- **Default:** Medium
- **Use Case:** Control the complexity of generated questions

**Chart:**
```
Easy   → Basic concepts, straightforward questions
Medium → Intermediate difficulty (Recommended)
Hard   → Advanced concepts, complex questions
```

#### Number of Items (Optional)
- **Range:** 1-20
- **Default:** 5
- **Use Case:** Control how many questions/answers to generate

**Example:**
```
num_items = 10
Result: 10 MCQs generated (if process_type = mcq)
```

### Step 4: Start Processing
```
1. After selecting options, click "✓ Start Processing"
2. Processing will begin immediately
3. You'll be redirected back to the PDF list
4. A success message will appear at the top
```

---

## Form Fields Explained

### 📌 Chapter Field

**What it does:**
- Filters content to specific chapters in subject models
- Applies only if the subject model supports chapter filtering

**Subject Support:**
- ✅ Polity (Chapters 1-41)
- ✅ Economics (chapter field exists)
- ✅ Math (chapter field exists)
- ✅ History (chapter field exists)
- ✅ Geography (chapter field exists)

**How it works:**
```
When you select Chapter 10 for Polity:
1. PDF content is processed
2. Questions generated are tagged with Chapter 10
3. Questions are saved to polity_mcq table with chapter='10'
```

**Examples:**

Example 1: Full PDF Processing
```
Chapter: (Leave blank)
Result: Questions generated from entire PDF
        Saved without specific chapter filter
```

Example 2: Specific Chapter
```
Chapter: 5
Difficulty: Hard
Result: Questions generated from Chapter 5 content only
        Difficulty level set to 'hard'
        Saved with chapter='5' and difficulty='hard'
```

### 📊 Difficulty Field

**What it does:**
- Sets the complexity level of generated questions
- Affects LLM prompt to request appropriate difficulty

**Impact on Generated Content:**

| Level | Impact | Example |
|-------|--------|---------|
| Easy | Basic, introductory questions | "Who is the President?" |
| Medium | Standard difficulty questions | "What are the powers of the President?" |
| Hard | Complex, analytical questions | "Analyze the constitutional limitations on presidential power" |

**Saved to Database:**
```
ProcessingLog.difficulty_level = 'easy' / 'medium' / 'hard'
Subject Table (e.g., polity_mcq).difficulty = same value
```

### 📝 Number of Items Field

**What it does:**
- Controls how many questions/answers should be generated
- Range: 1-20 items

**Examples:**

Example 1: Generate Few MCQs
```
num_items: 3
Result: 3 MCQs generated and saved
```

Example 2: Generate Many MCQs
```
num_items: 15
Result: 15 MCQs generated and saved
        (May take longer due to LLM processing)
```

---

## Database Fields Updated

When you process a PDF with these options, the following happens:

### ProcessingLog Table
```sql
INSERT INTO genai_processinglog (
    task_type='pdf_to_mcq',
    subject='polity',
    pdf_upload_id=25,
    difficulty_level='hard',
    num_items=5,
    log_details='{"chapter": "10"}',  -- JSON with chapter
    status='pending'
)
```

### Subject Table (e.g., polity_mcq)
```sql
INSERT INTO bank_polity (
    chapter='10',
    difficulty='hard',
    question='...',
    option_1='...',
    option_2='...',
    option_3='...',
    option_4='...',
    ans=2
)
```

---

## Complete Processing Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. Admin Panel - Select PDFs                            │
│    - Click "Process to MCQ" or "Process to Descriptive" │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Configuration Form                                   │
│    - Select Chapter (optional): 1-41                    │
│    - Select Difficulty: Easy/Medium/Hard                │
│    - Select Num Items: 1-20                             │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Form Submission & Processing                         │
│    - Create ProcessingLog with selected options         │
│    - Store chapter in log_details (JSON)                │
│    - Call route_pdf_processing_task()                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Task Router (10-step processing)                     │
│    - Extract PDF content                                │
│    - Select processor (PolityProcessor, etc.)           │
│    - Call LLM with chapter & difficulty context         │
│    - Generate MCQs/Descriptive answers                  │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Subject Processor                                    │
│    - Process with subject-specific logic                │
│    - Apply chapter and difficulty to saved records      │
│    - Save to subject table (polity_mcq, etc.)           │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Success & Redirect                                   │
│    - Redirect to PDF list                               │
│    - Show success message with count                    │
└─────────────────────────────────────────────────────────┘
```

---

## Console Output Example

When processing with Chapter and Difficulty selection:

```
████████████████████████████████████████████████████████████████████████████████
🎬 ADMIN ACTION: process_pdf_to_mcq()
   Chapter: 10
   Difficulty: hard
   Num Items: 5
   Selected PDFs: 1
████████████████████████████████████████████████████████████████████████████████

📄 Processing PDF: Indian-Polity-Chapter10.pdf
   Subject: polity
   File: uploads/indian-polity-chapter10.pdf

   [ADMIN] Creating ProcessingLog...
   [ADMIN] ✓ ProcessingLog created (ID: 45)
   [ADMIN] Chapter saved: 10
   [ADMIN] Calling route_pdf_processing_task()...

════════════════════════════════════════════════════════════════════════════════
[ROUTER] route_pdf_processing_task() - MAIN ENTRY POINT
[STEP 1] Status updated to 'running' ✅
[STEP 2] Prompt type: mcq ✅
[STEP 3] Processor: PolityProcessor ✅
[STEP 4] PDF file valid ✅
[STEP 5] Extracted 15 pages ✅
[STEP 6] Processor initialized ✅
[STEP 7] Generated 5 MCQs ✅
   (With difficulty=hard and chapter context from log_details)
[STEP 8] Saved 5 records ✅
   (Each record has chapter='10' and difficulty='hard')
[STEP 9] Updated ProcessingLog ✅
[STEP 10] Task completed ✅
════════════════════════════════════════════════════════════════════════════════

✅ ADMIN ACTION COMPLETE: Processed 1/1 PDFs
```

---

## Verifying Results in Database

After processing, you can verify the results:

### Option 1: Admin Panel

```
1. Go to Admin > Polity MCQ (or appropriate subject table)
2. Filter by:
   - chapter = 10
   - difficulty = hard
3. You should see the newly generated questions
```

### Option 2: Django Shell

```bash
python manage.py shell

# Check ProcessingLog
>>> from genai.models import ProcessingLog
>>> log = ProcessingLog.objects.latest('id')
>>> print(f"ID: {log.id}, Difficulty: {log.difficulty_level}, Chapter: {log.log_details}")
ID: 45, Difficulty: hard, Chapter: {"chapter": "10"}

# Check generated MCQs
>>> from bank.models import polity
>>> mcqs = polity.objects.filter(chapter='10', difficulty='hard')
>>> print(f"Generated {mcqs.count()} MCQs")
Generated 5 MCQs

# View details
>>> mcq = mcqs.first()
>>> print(f"Q: {mcq.question}\nA: {mcq.ans}")
```

---

## Important Notes

### Chapter Handling

⚠️ **Important:**
- The chapter field is saved to **log_details** as JSON
- It may not automatically filter PDF content extraction
- The chapter is useful for **organizing and categorizing** generated questions
- Subject models store the chapter with each question record

**Recommendation:**
- Use chapter selection to organize questions
- For content filtering, manually ensure your PDF contains the specific chapter

### Difficulty Implementation

- The difficulty level is applied **to all generated MCQs/answers** from that processing batch
- All 5 items generated will have the same difficulty level
- To generate mixed difficulties, run multiple processes

### Performance

| Setting | Impact | Time |
|---------|--------|------|
| num_items=5 | Small batch | 20-30s |
| num_items=10 | Medium batch | 30-50s |
| num_items=20 | Large batch | 60-90s |

**Note:** Times depend on PDF size and LLM API response time

---

## Troubleshooting

### Issue 1: Form doesn't appear after selecting action
**Solution:**
```
1. Check browser's JavaScript is enabled
2. Clear browser cache
3. Ensure CSRF token is being sent
4. Check Django debug toolbar for errors
```

### Issue 2: Chapter field is empty but I selected one
**Solution:**
```
1. Make sure you actually selected a chapter (not "-- Select Chapter --")
2. Refresh the page and try again
3. Check browser console for errors
```

### Issue 3: Difficulty level not applied to generated questions
**Solution:**
```
1. Check ProcessingLog record - difficulty_level should be set
2. Check subject table - difficulty field should match
3. If not set, reprocess with difficulty selected again
```

### Issue 4: Form submission fails
**Solution:**
```
1. Check that num_items is between 1-20
2. Ensure you have at least one PDF selected
3. Check Django logs for detailed error messages
4. Try with fewer PDFs first
```

---

## FAQ

**Q: Can I leave all fields blank?**
A: Yes. Default behavior is:
- Chapter: No filtering
- Difficulty: Medium
- Num Items: 5

**Q: Will changing difficulty re-process old MCQs?**
A: No. Each processing creates new MCQs. Old ones remain unchanged.

**Q: Can I process the same PDF with different difficulties?**
A: Yes! Run the process multiple times with different settings:
```
1. First run: Chapter=5, Difficulty=Easy
2. Second run: Chapter=5, Difficulty=Hard
   Results: 10 total MCQs (5 easy + 5 hard) for Chapter 5
```

**Q: Is chapter filtering automatic?**
A: Partially. The chapter is:
- Stored with the ProcessingLog
- Applied to generated MCQs
- Used for organization and filtering
- NOT used to automatically extract only Chapter X content from PDF

**Q: What happens to invalid selections?**
A: Form validates:
- Num Items must be 1-20
- Difficulty must be one of: Easy, Medium, Hard
- Chapter must be 1-41
- Blank selections are allowed (use defaults)

---

## Summary

The Chapter & Difficulty selection feature gives you **fine-grained control** over PDF processing:

✅ Select specific chapters to organize questions  
✅ Set difficulty level for appropriate complexity  
✅ Control number of items generated  
✅ Organize results by difficulty and chapter  
✅ Generate multiple batches with different settings  

Use this feature to create comprehensive question banks with varied difficulty levels for each chapter!
