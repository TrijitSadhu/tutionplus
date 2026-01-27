# New Feature: Chapter & Difficulty Selection Before PDF Processing

## ✅ What's New

You can now select **Chapter** and **Difficulty Level** before processing PDFs for subjects like Polity. This gives you complete control over question generation!

---

## 🚀 How to Use (Quick Start)

### 1. Go to Admin Panel
```
http://localhost:8000/admin/ → PDFUpload
```

### 2. Select PDFs & Choose Action
- Select one or more PDFs
- Click dropdown: "🔄 Process to MCQ" or "📝 Process to Descriptive"
- Click "Go"

### 3. Configure Options
A form will appear where you select:
- **Chapter:** 1-41 (or blank for entire document)
- **Difficulty:** Easy / Medium / Hard
- **Number of Items:** 1-20 (default: 5)

### 4. Start Processing
- Click "✓ Start Processing"
- You'll be redirected back to PDF list
- Success message shows how many were processed

---

## 📋 Form Fields

### Chapter (Optional)
| Setting | Result |
|---------|--------|
| Blank (default) | Process entire PDF, no chapter filter |
| Chapter 10 | Generate questions for Chapter 10 only |
| Chapter 25 | Generate questions for Chapter 25 only |

### Difficulty (Optional)
| Level | Complexity | Default |
|-------|-----------|---------|
| Easy | Basic concepts | ❌ |
| Medium | Standard questions | ✅ (Default) |
| Hard | Advanced concepts | ❌ |

### Number of Items (Optional)
| Count | Time | Default |
|-------|------|---------|
| 5 | 20-30s | ✅ (Default) |
| 10 | 30-50s | ❌ |
| 15+ | 60-90s | ❌ |

---

## 🔄 Processing Flow

```
Admin Select PDFs
    ↓
Click "Process to MCQ"
    ↓
[NEW] Form appears - Select Chapter & Difficulty
    ↓
Click "Start Processing"
    ↓
Create ProcessingLog with your options
    ↓
Execute 10-step router processing
    ↓
Save questions with chapter & difficulty
    ↓
Redirect to success page
```

---

## 📝 Example Workflow

**Scenario:** Generate hard MCQs for Polity Chapter 10

```
1. Select: "Polity-Chapter10.pdf"
2. Click: "🔄 Process to MCQ"
3. Select:
   - Chapter: 10
   - Difficulty: Hard
   - Num Items: 5
4. Click: "✓ Start Processing"
5. Result: 5 hard MCQs for Polity Chapter 10
```

---

## 🗄️ Database Storage

### ProcessingLog Table
```
task_type: pdf_to_mcq
subject: polity
difficulty_level: hard
num_items: 5
log_details: {"chapter": "10"}  ← Chapter stored as JSON
```

### Subject Table (e.g., polity_mcq)
```
chapter: 10          ← Applied to each question
difficulty: hard     ← Applied to each question
question: "..."
ans: 2
```

---

## ✨ Key Benefits

✅ **Fine-grained control** over question generation  
✅ **Organize by chapter** for structured content  
✅ **Vary difficulty levels** for comprehensive practice sets  
✅ **Control quantity** of generated items  
✅ **Process same PDF multiple times** with different settings  

---

## 📚 Example Use Cases

### Use Case 1: Create Practice Set for Chapter 5
```
Chapter: 5
Difficulty: Medium
Num Items: 10
→ Result: 10 medium-difficulty MCQs for Chapter 5
```

### Use Case 2: Create Difficulty-Based Banks
```
Run 1: Difficulty=Easy, Num Items=5
Run 2: Difficulty=Hard, Num Items=5
→ Result: 10 total questions (mixed difficulty)
```

### Use Case 3: Create Exam-Prep Questions
```
Chapter: 15
Difficulty: Hard
Num Items: 15
→ Result: 15 hard questions to practice
```

---

## 🔍 Verify Results

### In Admin Panel
```
1. Go to: Admin → Polity MCQ (or your subject)
2. Filter by chapter and difficulty
3. See newly generated questions
```

### In Shell
```bash
python manage.py shell
>>> from bank.models import polity
>>> mcqs = polity.objects.filter(chapter='10', difficulty='hard')
>>> print(f"Count: {mcqs.count()}")
```

---

## ⚙️ Technical Details

### Files Modified
- `genai/admin.py` - Added ProcessPDFForm and process_pdf_with_options view
- `genai/urls.py` - Added URL route for processing form
- `genai/templates/admin/genai/process_pdf_form.html` - NEW form template

### Changes Made
1. ✅ Created ProcessPDFForm with chapter, difficulty, num_items fields
2. ✅ Modified admin actions to redirect to intermediate form
3. ✅ Created process_pdf_with_options view for form handling
4. ✅ Created beautiful form template with explanations
5. ✅ Chapter & difficulty stored in ProcessingLog and subject models

### No Breaking Changes
- All existing functionality preserved
- Old processing method still works
- Backward compatible with existing code
- Zero logic changes, pure feature addition

---

## 📖 Complete Guide

For detailed documentation, see:
**[PDF_PROCESSING_WITH_CHAPTER_DIFFICULTY.md](PDF_PROCESSING_WITH_CHAPTER_DIFFICULTY.md)**

---

## ❓ FAQ

**Q: What if I don't select a chapter?**
A: It will process the entire PDF without chapter filtering.

**Q: Can I change difficulty after processing?**
A: No, but you can reprocess the same PDF with different difficulty.

**Q: How long does processing take?**
A: Typically 20-90 seconds depending on file size and num_items.

**Q: Will it create duplicate questions?**
A: No, each processing creates new unique questions.

**Q: Can I process same PDF with different chapters?**
A: Yes, just run the process multiple times with different chapter selections.

---

## 🎉 Ready to Use!

1. Start Django: `python manage.py runserver`
2. Go to Admin: `http://localhost:8000/admin/`
3. Select PDFs and choose action
4. Fill in the form with your preferences
5. Click "Start Processing"
6. Watch your questions being generated!

Enjoy! 🚀
