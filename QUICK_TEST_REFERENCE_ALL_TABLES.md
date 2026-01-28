# 🚀 QUICK TEST REFERENCE - ALL 34 TABLES

**Total Tests**: 31 records (IDs 13-43)
**Expected Results**: 1 record per table
**Test Duration**: ~2-3 minutes per test

---

## ⚡ QUICK START

```
1. Open: http://localhost:8000/admin/genai/jsonimport/
2. Find Record: ID 13, 14, 15, ... 43
3. Select checkbox
4. Action: "Bulk Import" → "Go"
5. Click: "Proceed with Import"
6. Watch: Django terminal + Browser console (F12)
7. Verify: Record created in respective table
8. Repeat for next ID
```

---

## 📊 TEST GROUPS

### **Group 1: Subject MCQ (IDs 13-22)** - 10 tests
- 13: polity
- 14: history
- 15: geography
- 16: economics
- 17: physics
- 18: chemistry
- 19: biology
- 20: reasoning
- 21: error
- 22: mcq

### **Group 2: Current Affairs (IDs 23-25)** - 3 tests
- 23: currentaffairs_mcq
- 24: currentaffairs_descriptive
- 25: current_affairs_slide

### **Group 3: Other Tables (IDs 26-43)** - 18 tests
- 26: total
- 27-31: Job related (total_english, total_math, total_job, total_job_category, total_job_state)
- 32: home
- 33: topic
- 34: math
- 35: job
- 36-43: Vocabulary (the_hindu_word_Header1/2, the_hindu_word_list1/2, the_economy_word_Header1/2, the_economy_word_list1/2)

---

## ✅ EXPECTED FOR EACH TEST

```
✅ Django Terminal:
   - Form is VALID
   - Processing JsonImport ID: XX
   - CREATED Record (ID: YY)

✅ Browser Console (F12):
   - Date auto-set to: 2026-01-28
   - Form submitted successfully

✅ Admin Interface:
   - Success message
   - New record in target table
```

---

## 🎯 TEST CHECKLIST

### Group 1: Subject MCQ (13-22)
- [ ] ID 13: polity
- [ ] ID 14: history
- [ ] ID 15: geography
- [ ] ID 16: economics
- [ ] ID 17: physics
- [ ] ID 18: chemistry
- [ ] ID 19: biology
- [ ] ID 20: reasoning
- [ ] ID 21: error
- [ ] ID 22: mcq

### Group 2: Current Affairs (23-25)
- [ ] ID 23: currentaffairs_mcq
- [ ] ID 24: currentaffairs_descriptive
- [ ] ID 25: current_affairs_slide

### Group 3: Other Tables (26-43)
- [ ] ID 26: total
- [ ] ID 27: total_english
- [ ] ID 28: total_math
- [ ] ID 29: total_job
- [ ] ID 30: total_job_category
- [ ] ID 31: total_job_state
- [ ] ID 32: home
- [ ] ID 33: topic
- [ ] ID 34: math
- [ ] ID 35: job
- [ ] ID 36: the_hindu_word_Header1
- [ ] ID 37: the_hindu_word_Header2
- [ ] ID 38: the_hindu_word_list1
- [ ] ID 39: the_hindu_word_list2
- [ ] ID 40: the_economy_word_Header1
- [ ] ID 41: the_economy_word_Header2
- [ ] ID 42: the_economy_word_list1
- [ ] ID 43: the_economy_word_list2

---

## 🔍 VERIFY RECORDS CREATED

After each test, verify in admin:

```
For Subject MCQ (IDs 13-22):
   - Go to Admin → Bank → [subject name] e.g., "Polity"
   - Should see 1 new record

For Current Affairs (IDs 23-25):
   - Admin → Bank → CurrentAffairs MCQ (or Descriptive, or Slide)
   - Should see 1 new record

For Other Tables (IDs 26-43):
   - Admin → Bank → [specific table]
   - Should see 1 new record
```

---

## ❌ IF TEST FAILS

**Step 1: Check Logs**
```
Look for errors in:
- Django Terminal (Ctrl+C to pause, scroll up)
- Browser Console (F12 → Console tab)
- Django log files
```

**Step 2: Common Issues**
```
- "Model not found": Check table name in TABLE_CHOICES
- "Field error": Check JSON field names vs model
- "Category error": Ensure category exists
- "Type error": Check data types in JSON
```

**Step 3: Skip & Continue**
```
If one test fails, try next one to identify patterns
```

---

## 📝 RESULT FORMAT

**For Each Test:**
```
Test ID 13 (polity): ✅ PASS
  - Records created: 1
  - Question: How many Articles...
  - Category: National
```

**Final Summary:**
```
Total Tests: 31
Passed: XX ✅
Failed: X ❌
Success Rate: XX%
```

---

## ⏱️ ESTIMATED TIME

- Per test: 30 seconds
- All 31 tests: ~15 minutes
- With verification: ~20 minutes

---

## 📋 DETAILED JSON DATA

See file: **COMPREHENSIVE_TEST_PLAN_ALL_TABLES.md**

Contains:
- Complete JSON for each table
- Expected results
- Field mappings
- Success criteria

---

## 🎬 READY? START HERE:

1. Open Admin: http://localhost:8000/admin/genai/jsonimport/
2. Find Record ID 13 (polity)
3. Select checkbox
4. Action dropdown → "Bulk Import"
5. Click "Go"
6. Click "Proceed with Import"
7. Watch logs...
8. Report result

**Let's go! 🚀**
