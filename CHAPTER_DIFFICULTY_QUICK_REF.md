# Quick Reference: Chapter & Difficulty Selection

## 🚀 Start Here (30 seconds)

```
1. Admin Panel: http://localhost:8000/admin/
2. Click: PDFUpload
3. Select PDFs: Check the boxes
4. Action: Dropdown → "🔄 Process to MCQ"
5. Click: "Go"
6. Form: Select Chapter, Difficulty, Items
7. Click: "✓ Start Processing"
8. Done! Processing starts
```

---

## 📋 Form Fields Reference

| Field | Type | Required | Default | Options |
|-------|------|----------|---------|---------|
| Chapter | Dropdown | No | Blank | 1-41 or blank |
| Difficulty | Dropdown | No | Medium | Easy, Medium, Hard |
| Num Items | Number | No | 5 | 1-20 |

---

## 💡 Quick Examples

### Example 1: Easy MCQs for Chapter 5
```
Chapter: 5
Difficulty: Easy
Num Items: 10
→ Result: 10 easy questions about Chapter 5
```

### Example 2: Hard Questions (Any Chapter)
```
Chapter: (blank)
Difficulty: Hard
Num Items: 5
→ Result: 5 hard questions from entire PDF
```

### Example 3: Medium Mix (Default)
```
Chapter: (blank)
Difficulty: (blank - uses Medium)
Num Items: (blank - uses 5)
→ Result: 5 medium-difficulty questions
```

---

## ⏱️ Processing Time

| Items | Time | Speed |
|-------|------|-------|
| 1-5 | 20-30s | Fast |
| 6-10 | 30-50s | Medium |
| 11-15 | 50-70s | Slow |
| 16-20 | 70-90s | Very Slow |

---

## 🔍 Verify Results

```bash
# In Django Shell
python manage.py shell

>>> from bank.models import polity
>>> polity.objects.filter(chapter='10', difficulty='hard').count()
# Shows: number of questions generated
```

---

## ✅ Checklist

- [ ] Select one or more PDFs
- [ ] Click dropdown action
- [ ] Click "Go" button
- [ ] Form appears correctly
- [ ] Chapter dropdown functional
- [ ] Difficulty dropdown functional
- [ ] Num items field editable
- [ ] Click "Start Processing"
- [ ] Success message appears
- [ ] Check database for results

---

## ❌ Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| No form appears | Ensure PDF is selected & Go button clicked |
| Can't submit | Check num_items is 1-20 |
| Wrong difficulty | Verify dropdown selection |
| No chapter selection | That's OK - blank means entire PDF |

---

## 📞 Help

**Complete Guide:** `PDF_PROCESSING_WITH_CHAPTER_DIFFICULTY.md`  
**Visual Guide:** `CHAPTER_DIFFICULTY_VISUAL_GUIDE.md`  
**Implementation:** `CHAPTER_DIFFICULTY_IMPLEMENTATION.md`  

---

## 🎯 Key Points

✓ Chapter & Difficulty are **optional**  
✓ Form appears **after** selecting action  
✓ Settings applied to **all** selected PDFs  
✓ Results saved to **database**  
✓ Can **reprocess** same PDF with different settings  

---

## 🚦 Status

✅ Feature Complete  
✅ Tested & Working  
✅ Ready to Use  
✅ Fully Documented  

---

**That's it! You're ready to use the feature.** 🎉
