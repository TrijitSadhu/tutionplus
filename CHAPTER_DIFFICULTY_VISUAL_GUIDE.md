# Chapter & Difficulty Selection: Visual Guide

## Step-by-Step Screenshots & Instructions

### Step 1: Go to Admin PDFUpload
```
URL: http://localhost:8000/admin/genai/pdfupload/

You'll see a list of all uploaded PDFs with columns:
- Title
- Subject
- Status (color-coded badge)
- Total Pages
- Uploaded At
- Uploaded By
```

**What you see:**
```
┌─────────────────────────────────────────────────────────────────┐
│ PDFUpload                                                       │
├─────────────────────────────────────────────────────────────────┤
│ [ ] Indian-Polity.pdf          polity  ✓ Uploaded  89  2024-01  │
│ [ ] Economics-101.pdf          econ    ✓ Uploaded  156 2024-01  │
│ [ ] History-Review.pdf         history ✓ Uploaded  245 2024-01  │
├─────────────────────────────────────────────────────────────────┤
│ Action: [Process to MCQ ▼]  [Go]                                │
└─────────────────────────────────────────────────────────────────┘
```

---

### Step 2: Select PDFs
```
1. Check the checkbox for each PDF you want to process
2. OR use the header checkbox to select all visible PDFs
3. You can select multiple PDFs at once

Multiple selections example:
[✓] Indian-Polity.pdf
[✓] Economics-101.pdf
[  ] History-Review.pdf  (not selected)
```

---

### Step 3: Choose Processing Action
```
Bottom of the page has a dropdown and button:

Action: [▼ Process to MCQ] [Go]
        
Or:
        [▼ Process to Descriptive] [Go]

Options available:
1. "🔄 Process to MCQ" - Generate multiple choice questions
2. "📝 Process to Descriptive" - Generate descriptive answers
3. "📄 Extract Text" - Extract text from PDFs
```

**Important:** Select the dropdown first, then click "Go"

---

### Step 4: Form Appears
After clicking "Go", you'll be redirected to a beautiful form:

```
╔═══════════════════════════════════════════════════════════════╗
║           Process PDFs - Select Options                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ 📄 Selected PDFs (2)                                          ║
║                                                               ║
║ • Indian-Polity.pdf (Subject: Polity)                         ║
║ • Economics-101.pdf (Subject: Economics)                      ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ ⚙️  Processing Options                                         ║
║                                                               ║
║ Configure the options below for processing these PDFs to MCQ │
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ Chapter (Optional)                                            ║
║ [▼ -- Select Chapter --]                                     ║
║ Leave blank to not filter by chapter                          ║
║                                                               ║
║ Difficulty Level (Optional)                                  ║
║ [▼ -- Select Difficulty --]                                  ║
║ Leave blank to use medium difficulty                         ║
║                                                               ║
║ Number of MCQs/Items to Generate                             ║
║ [_________] (default: 5)                                     ║
║ How many items should be generated (1-20)                    ║
║                                                               ║
║ [✓ Start Processing]  [Cancel]                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

### Step 5: Fill in Chapter (Optional)
```
Click the Chapter dropdown to see chapters:

Chapter: [▼ -- Select Chapter --]

Dropdown shows:
-- Select Chapter --
1
2
3
...
40
41

You can select any chapter from 1-41
Or leave it blank (default) to process entire PDF
```

**Example selections:**
```
No selection:   [▼ -- Select Chapter --]  → Process all chapters
Chapter 5:      [▼ 5]                      → Only Chapter 5
Chapter 20:     [▼ 20]                     → Only Chapter 20
```

---

### Step 6: Fill in Difficulty (Optional)
```
Click the Difficulty dropdown:

Difficulty Level: [▼ -- Select Difficulty --]

Dropdown shows:
-- Select Difficulty --
Easy
Medium
Hard

Choose one based on your needs
```

**Difficulty Guide:**
```
Easy   → Basic concepts, introductory questions
        Good for: Learning fundamentals
        
Medium → Standard difficulty (RECOMMENDED)
        Good for: Regular practice
        
Hard   → Complex, analytical questions
        Good for: Exam preparation
```

---

### Step 7: Set Number of Items
```
Number of MCQs/Items to Generate: [___]

Default: 5 (if left blank)
Min: 1
Max: 20

Examples:
[5]   → Generate 5 questions (FAST)
[10]  → Generate 10 questions (MEDIUM)
[15]  → Generate 15 questions (SLOW)
[20]  → Generate 20 questions (SLOWEST)
```

---

### Step 8: Review & Submit
```
Before clicking "Start Processing", verify:

✓ Chapter selection (if needed)
✓ Difficulty selection (if needed)  
✓ Number of items (1-20)

Then click:
[✓ Start Processing]
```

---

### Step 9: Processing Starts
```
After clicking "Start Processing":

1. Your selections are sent to the server
2. ProcessingLog is created with your options
3. Processing starts (you'll see in Django terminal)
4. Takes 20-90 seconds depending on file size
5. You'll be redirected to success page

In terminal, you'll see:
████████████████████████████████████████
🎬 ADMIN ACTION: process_pdf_to_mcq()
   Chapter: 10
   Difficulty: hard
   Num Items: 5
   Selected PDFs: 1
████████████████████████████████████████

[STEP 1] Status updated... ✅
[STEP 2] Prompt type... ✅
[STEP 3] Processor... ✅
...and so on
```

---

### Step 10: Success!
```
You'll see a success message at the top:

✓ Successfully processed 1 PDF(s) to MCQ

And you're back at the PDFUpload list:

┌─────────────────────────────────────────────┐
│ ✓ Successfully processed 1 PDF(s) to MCQ    │
├─────────────────────────────────────────────┤
│ PDFUpload list...                           │
└─────────────────────────────────────────────┘
```

---

## Visual Example Walkthrough

### Example: Create 10 Hard MCQs for Chapter 15 of Polity

**1. Admin Page:**
```
Select: [✓] Indian-Polity.pdf
Action: [▼ Process to MCQ] [Go]
```

**2. Form Page (After clicking Go):**
```
Chapter:            [▼ 15]         ← Select Chapter 15
Difficulty Level:   [▼ Hard]       ← Select Hard
Num Items:          [10]           ← Enter 10
```

**3. Click:**
```
[✓ Start Processing]
```

**4. Result:**
```
Processing starts...
[Terminal shows 10-step trace]
...
✓ Successfully processed 1 PDF(s) to MCQ
[Redirected to PDFUpload list]
```

**5. Verify in Database:**
```bash
python manage.py shell
>>> from bank.models import polity
>>> mcqs = polity.objects.filter(chapter='15', difficulty='hard').order_by('-day')
>>> print(f"Found {mcqs.count()} hard MCQs for Chapter 15")
Found 10 hard MCQs for Chapter 15

>>> mcq = mcqs.first()
>>> print(f"Q: {mcq.question[:50]}...\nDifficulty: {mcq.difficulty}")
Q: What are the key functions of the constitutional...
Difficulty: hard
```

---

## Advanced: Multiple Processing Runs

### Create Complete Chapter Bank (Easy + Hard)

**Run 1: Easy Questions**
```
Chapter: 10
Difficulty: Easy
Num Items: 5
→ Result: 5 easy questions for Chapter 10
```

**Run 2: Hard Questions**
```
Chapter: 10
Difficulty: Hard
Num Items: 5
→ Result: 5 hard questions for Chapter 10
```

**Total Result:**
```
10 questions for Chapter 10 (5 easy + 5 hard)
Perfect for progressive difficulty practice!
```

---

## Keyboard Shortcuts & Tips

### Admin Panel Tips
- **Tab** to move between dropdown fields
- **Space/Enter** to open dropdowns
- **Arrow keys** to select from dropdown
- **Ctrl+A** to select all PDFs in the list

### Form Tips
- **Tab** to navigate to next field
- **Shift+Tab** to go to previous field
- **Enter** to submit (when button has focus)
- All fields except action buttons are optional

---

## Troubleshooting

### Issue: Form doesn't appear after clicking "Go"

**Solution:**
```
1. Make sure you selected a PDF (checkbox checked)
2. Make sure you selected an action from dropdown
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try a different browser
5. Check JavaScript is enabled
```

### Issue: "Start Processing" button doesn't work

**Solution:**
```
1. Make sure all fields are filled correctly
2. num_items must be between 1-20
3. Check browser console for errors (F12)
4. Try reloading the page
```

### Issue: Redirects to login page

**Solution:**
```
1. Make sure you're logged in as admin user
2. Log out and log back in
3. Check session expiration time
```

### Issue: Processing seems stuck

**Solution:**
```
1. Wait 2-3 minutes (LLM API calls can be slow)
2. Check Django terminal for error messages
3. If really stuck, restart Django server
4. Try with fewer items (num_items = 1)
```

---

## Summary

The form makes it easy to:
1. ✅ Select chapter for organization
2. ✅ Set difficulty level for question complexity
3. ✅ Control number of questions generated
4. ✅ Process multiple PDFs at once
5. ✅ Create comprehensive question banks

Just fill in the form and let the system generate perfect questions for your needs! 🎉
