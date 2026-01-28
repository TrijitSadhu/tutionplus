# 🧪 COMPREHENSIVE TEST PLAN - ALL 34 TABLES

**Total Test Records**: 31 records (IDs 13-43)
**Date**: January 28, 2026
**Status**: Ready for Testing

---

## 📋 TEST RECORDS OVERVIEW

### **SECTION 1: Subject MCQ (10 Records)**

| ID | Table | Description | Expected Result |
|----|----|-----------|--------|
| 13 | polity | Constitution (395 Articles) | 1 record in polity table |
| 14 | history | Indian Independence (1947) | 1 record in history table |
| 15 | geography | Pacific Ocean largest | 1 record in geography table |
| 16 | economics | GDP definition | 1 record in economics table |
| 17 | physics | Speed of light | 1 record in physics table |
| 18 | chemistry | Carbon atomic number | 1 record in chemistry table |
| 19 | biology | Mitochondria powerhouse | 1 record in biology table |
| 20 | reasoning | Deductive reasoning | 1 record in reasoning table |
| 21 | error | Grammar error finding | 1 record in error table |
| 22 | mcq | France capital | 1 record in mcq table |

### **SECTION 2: Current Affairs (3 Records)**

| ID | Table | Description | Expected Result |
|----|----|-----------|--------|
| 23 | currentaffairs_mcq | G20 summit 2025 | 1 record in currentaffairs_mcq table |
| 24 | currentaffairs_descriptive | Global Economic Trends | 1 record in currentaffairs_descriptive table |
| 25 | current_affairs_slide | Climate Action Report | 1 record in current_affairs_slide table |

### **SECTION 3: Other Tables (18 Records)**

| ID | Table | Description | Expected Result |
|----|----|-----------|--------|
| 26 | total | General Purpose Test | 1 record in total table |
| 27 | total_english | Spelling question | 1 record in total_english table |
| 28 | total_math | Math calculation | 1 record in total_math table |
| 29 | total_job | Software Engineer position | 1 record in total_job table |
| 30 | total_job_category | IT Jobs category | 1 record in total_job_category table |
| 31 | total_job_state | Karnataka jobs | 1 record in total_job_state table |
| 32 | home | Welcome to Platform | 1 record in home table |
| 33 | topic | Machine Learning topic | 1 record in topic table |
| 34 | math | Circle area calculation | 1 record in math table |
| 35 | job | Data Scientist position | 1 record in job table |
| 36 | the_hindu_word_Header1 | Ubiquitous (word) | 1 record in the_hindu_word_Header1 table |
| 37 | the_hindu_word_Header2 | Ephemeral (word) | 1 record in the_hindu_word_Header2 table |
| 38 | the_hindu_word_list1 | Ameliorate (word) | 1 record in the_hindu_word_list1 table |
| 39 | the_hindu_word_list2 | Benevolent (word) | 1 record in the_hindu_word_list2 table |
| 40 | the_economy_word_Header1 | Inflation (word) | 1 record in the_economy_word_Header1 table |
| 41 | the_economy_word_Header2 | Recession (word) | 1 record in the_economy_word_Header2 table |
| 42 | the_economy_word_list1 | Deflation (word) | 1 record in the_economy_word_list1 table |
| 43 | the_economy_word_list2 | Equity (word) | 1 record in the_economy_word_list2 table |

---

## 🔄 TESTING PROCEDURE - ONE BY ONE

### **For Each Test:**

1. **Go to Admin**: http://localhost:8000/admin/genai/jsonimport/
2. **Find Record**: Search for ID (e.g., 13, 14, 15...)
3. **Select Record**: Check the checkbox next to the record
4. **Action**: Select "Bulk Import" from Action dropdown
5. **Go**: Click "Go" button
6. **Form Page**: You should see the intermediate form with date field
7. **Console**: Open DevTools (F12) → Console tab
8. **Proceed**: Click "Proceed with Import"
9. **Monitor**:
   - Watch Django terminal for logs
   - Watch browser console for JavaScript logs
   - Look for success message

### **Expected Output Pattern:**

```
✅ Django Terminal Should Show:
   - ✅ Entry Point reached
   - ✅ Detecting form type...
   - ✅ Form is VALID
   - ✅ Processing JsonImport ID: XX
   - ✅ CREATED Record (ID: XX)
   - ✅ Total created: 1

✅ Browser Console Should Show:
   - ✅ Date auto-set to: 2026-01-28
   - [Multiple log statements tracking form submission]
   - ✅ Form submitted successfully

✅ Admin Interface Should Show:
   - Success message at top
   - New record visible in respective table
```

---

## 📊 DETAILED TEST CASES

### **TEST 1: ID 13 - POLITY (Subject MCQ)**

**Command**: Go to http://localhost:8000/admin/genai/jsonimport/
**Select**: Record ID 13 (polity)
**Action**: Bulk Import → Go → Proceed

**Expected JSON**:
```json
[{
    "question": "How many Articles are in the Indian Constitution?",
    "option_1": "390",
    "option_2": "395",
    "option_3": "400",
    "option_4": "405",
    "option_5": "",
    "ans": 2,
    "explanation": "The Indian Constitution has 395 Articles divided into 22 Parts.",
    "categories": ["National"],
    "year_now": "2026",
    "month": "January",
    "creation_time": "10:00:00"
}]
```

**Success Criteria**:
- ✅ 1 record created in `bank_polity` table
- ✅ Question text matches
- ✅ Answer is 2 (395)
- ✅ Category is "National"

**Action on Pass**: Continue to TEST 2
**Action on Fail**: Check logs and report

---

### **TEST 2: ID 14 - HISTORY (Subject MCQ)**

**Command**: Go to http://localhost:8000/admin/genai/jsonimport/
**Select**: Record ID 14 (history)
**Action**: Bulk Import → Go → Proceed

**Expected JSON**:
```json
[{
    "question": "In which year did the Indian Independence Act become effective?",
    "option_1": "1945",
    "option_2": "1946",
    "option_3": "1947",
    "option_4": "1948",
    "option_5": "",
    "ans": 3,
    "explanation": "August 15, 1947 is when India became independent from British rule.",
    "categories": ["National"],
    "year_now": "2026",
    "month": "January",
    "creation_time": "10:00:00"
}]
```

**Success Criteria**:
- ✅ 1 record created in `bank_history` table
- ✅ Answer is 3 (1947)
- ✅ Category is "National"

---

### **TEST 3: ID 15 - GEOGRAPHY (Subject MCQ)**

**Command**: Go to http://localhost:8000/admin/genai/jsonimport/
**Select**: Record ID 15 (geography)
**Action**: Bulk Import → Go → Proceed

**Expected JSON**:
```json
[{
    "question": "Which is the largest ocean in the world?",
    "option_1": "Atlantic Ocean",
    "option_2": "Indian Ocean",
    "option_3": "Pacific Ocean",
    "option_4": "Arctic Ocean",
    "option_5": "",
    "ans": 3,
    "explanation": "The Pacific Ocean is the largest and deepest ocean on Earth.",
    "categories": ["National"],
    "year_now": "2026",
    "month": "January",
    "creation_time": "10:00:00"
}]
```

**Success Criteria**:
- ✅ 1 record created in `bank_geography` table
- ✅ Answer is 3 (Pacific Ocean)

---

### **TEST 4: ID 16 - ECONOMICS (Subject MCQ)**

**Expected JSON**: GDP question
**Success Criteria**:
- ✅ 1 record created in `bank_economics` table
- ✅ Category is "Business_Economy_Banking"

---

### **TEST 5: ID 17 - PHYSICS (Subject MCQ)**

**Expected JSON**: Speed of light question
**Success Criteria**:
- ✅ 1 record created in `bank_physics` table
- ✅ Category is "Science_Techonlogy"

---

### **TEST 6: ID 18 - CHEMISTRY (Subject MCQ)**

**Expected JSON**: Carbon atomic number question
**Success Criteria**:
- ✅ 1 record created in `bank_chemistry` table
- ✅ Category is "Science_Techonlogy"

---

### **TEST 7: ID 19 - BIOLOGY (Subject MCQ)**

**Expected JSON**: Mitochondria powerhouse question
**Success Criteria**:
- ✅ 1 record created in `bank_biology` table
- ✅ Category is "Science_Techonlogy"

---

### **TEST 8: ID 20 - REASONING (Subject MCQ)**

**Expected JSON**: Deductive reasoning question
**Success Criteria**:
- ✅ 1 record created in `bank_reasoning` table

---

### **TEST 9: ID 21 - ERROR (Subject MCQ)**

**Expected JSON**: Grammar error finding question
**Success Criteria**:
- ✅ 1 record created in `bank_error` table

---

### **TEST 10: ID 22 - MCQ (General MCQ)**

**Expected JSON**: France capital question
**Success Criteria**:
- ✅ 1 record created in `bank_mcq` table

---

### **TEST 11: ID 23 - CURRENTAFFAIRS_MCQ**

**Expected JSON**:
```json
[{
    "question": "Which country hosted the G20 summit in 2025?",
    "option_1": "Japan",
    "option_2": "Brazil",
    "option_3": "India",
    "option_4": "USA",
    "option_5": "",
    "ans": 2,
    "explanation": "Brazil is hosting the G20 summit for 2025.",
    "categories": ["International"],
    "year_now": "2026",
    "month": "January",
    "creation_time": "10:00:00"
}]
```

**Success Criteria**:
- ✅ 1 record created in `bank_currentaffairs_mcq` table
- ✅ Category is "International"

---

### **TEST 12: ID 24 - CURRENTAFFAIRS_DESCRIPTIVE**

**Expected JSON**:
```json
[{
    "upper_heading": "Global Economic Trends 2026",
    "yellow_heading": "Market Performance Overview",
    "key_1": "Stock markets show mixed performance",
    "key_2": "Cryptocurrency market recovery continuing",
    "key_3": "Gold prices increase due to geopolitical tensions",
    "key_4": "Real estate market stabilizes",
    "all_key_points": "Economic outlook shows cautious optimism",
    "categories": ["Business_Economy_Banking"],
    "year_now": "2026",
    "month": "January",
    "creation_time": "10:00:00"
}]
```

**Success Criteria**:
- ✅ 1 record created in `bank_currentaffairs_descriptive` table
- ✅ Upper heading is "Global Economic Trends 2026"
- ✅ Category is "Business_Economy_Banking"

---

### **TEST 13: ID 25 - CURRENT_AFFAIRS_SLIDE**

**Expected JSON**:
```json
[{
    "upper_heading": "Climate Action Report 2026",
    "yellow_heading": "Progress on Net-Zero Targets",
    "key_1": "150 countries meet renewable energy goals",
    "key_2": "Carbon emissions decline by 8% YoY",
    "key_3": "Green technology investments reach $2 trillion",
    "key_4": "New climate treaties signed by 180 nations",
    "creation_time": "10:00:00"
}]
```

**Success Criteria**:
- ✅ 1 record created in `bank_current_affairs_slide` table
- ✅ Upper heading is "Climate Action Report 2026"

---

### **TEST 14: ID 26 - TOTAL (Generic Table)**

**Expected JSON**:
```json
[{
    "name": "Test Record 1",
    "title": "General Test Data",
    "content": "This is a general purpose test record",
    "year_now": "2026",
    "month": "January",
    "creation_time": "10:00:00"
}]
```

**Success Criteria**:
- ✅ 1 record created in `bank_total` table
- ✅ Tests generic processor fallback

---

### **TEST 15-31: Other Tables (Generic Processing)**

**Tests 15-31** follow the same pattern. Each tests a different table with generic content.

**ID 27-31: Job Tables** (total_job, total_job_category, total_job_state, job)
**ID 32-35: Other Tables** (home, topic, math)
**ID 36-43: Vocabulary Tables** (the_hindu_word_*, the_economy_word_*)

All should:
- ✅ Create 1 record in respective table
- ✅ Show success message
- ✅ Use generic processor if no specific processor exists

---

## 📈 SUMMARY TABLE

| Test | ID | Table | Status | Notes |
|------|----|----|--------|-------|
| 1 | 13 | polity | ⏳ Pending | Subject MCQ |
| 2 | 14 | history | ⏳ Pending | Subject MCQ |
| 3 | 15 | geography | ⏳ Pending | Subject MCQ |
| 4 | 16 | economics | ⏳ Pending | Subject MCQ |
| 5 | 17 | physics | ⏳ Pending | Subject MCQ |
| 6 | 18 | chemistry | ⏳ Pending | Subject MCQ |
| 7 | 19 | biology | ⏳ Pending | Subject MCQ |
| 8 | 20 | reasoning | ⏳ Pending | Subject MCQ |
| 9 | 21 | error | ⏳ Pending | Subject MCQ |
| 10 | 22 | mcq | ⏳ Pending | Subject MCQ |
| 11 | 23 | currentaffairs_mcq | ⏳ Pending | Current Affairs MCQ |
| 12 | 24 | currentaffairs_descriptive | ⏳ Pending | Current Affairs Descriptive |
| 13 | 25 | current_affairs_slide | ⏳ Pending | Current Affairs Slide |
| 14 | 26 | total | ⏳ Pending | Generic Table 1 |
| 15 | 27 | total_english | ⏳ Pending | Generic Table 2 |
| 16 | 28 | total_math | ⏳ Pending | Generic Table 3 |
| 17 | 29 | total_job | ⏳ Pending | Job Table 1 |
| 18 | 30 | total_job_category | ⏳ Pending | Job Table 2 |
| 19 | 31 | total_job_state | ⏳ Pending | Job Table 3 |
| 20 | 32 | home | ⏳ Pending | Home Table |
| 21 | 33 | topic | ⏳ Pending | Topic Table |
| 22 | 34 | math | ⏳ Pending | Math Table |
| 23 | 35 | job | ⏳ Pending | Job Listing Table |
| 24 | 36 | the_hindu_word_Header1 | ⏳ Pending | Vocabulary 1 |
| 25 | 37 | the_hindu_word_Header2 | ⏳ Pending | Vocabulary 2 |
| 26 | 38 | the_hindu_word_list1 | ⏳ Pending | Vocabulary 3 |
| 27 | 39 | the_hindu_word_list2 | ⏳ Pending | Vocabulary 4 |
| 28 | 40 | the_economy_word_Header1 | ⏳ Pending | Economy Word 1 |
| 29 | 41 | the_economy_word_Header2 | ⏳ Pending | Economy Word 2 |
| 30 | 42 | the_economy_word_list1 | ⏳ Pending | Economy Word 3 |
| 31 | 43 | the_economy_word_list2 | ⏳ Pending | Economy Word 4 |

---

## ✅ SUCCESS CRITERIA (Overall)

- **All 31 Tests Pass**: ✅ Complete Implementation
- **30/31 Pass**: ✅ Good - Investigate 1 failure
- **25-29 Pass**: ⚠️ Most functional - Fix failing tables
- **<25 Pass**: ❌ Significant issues - Debug comprehensively

---

## 🔧 DEBUGGING CHECKLIST

If a test fails:

1. **Check Django Terminal** (CTRL+C to stop server if needed)
   - Look for exception in logs
   - Check error message
   
2. **Check Browser Console** (F12 → Console)
   - Look for JavaScript errors
   - Check form submission logs
   
3. **Check Admin Success Message**
   - May show partial success
   
4. **Common Issues**:
   - ❌ Model not found: Check TABLE_CHOICES in JsonImport model
   - ❌ Field not found: Check JSON field names match model
   - ❌ Category not found: Ensure category exists in database
   - ❌ Type error: Check data types in JSON

---

## 📝 REPORTING RESULTS

When done, report:

```
✅ TESTS PASSED: XX/31
❌ TESTS FAILED: X/31

PASSED:
- ID 13: polity ✅
- ID 14: history ✅
- ...

FAILED:
- ID XX: [table_name] ❌
  Error: [specific error message]
  
SUMMARY:
[Any patterns in failures]
```

---

**Ready to Start Testing!** 🚀
