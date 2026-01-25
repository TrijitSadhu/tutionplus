# MCQ System - Complete Guide

## 📋 MCQ Table Structure & Columns

### Main MCQ Table: `bank_mcq`

**Purpose:** Store Multiple Choice Questions with year, month, date categorization

**Available Columns:**

| Column | Type | Max Length | Purpose | Default | Indexed |
|--------|------|-----------|---------|---------|---------|
| `id` | PK | - | Unique identifier | Auto | ✓ |
| `year_now` | CharField | 10 | Year (2018/2019/2020/2026) | 2018 | ✓ |
| `month` | CharField | 15 | Month (January-December) | December | ✓ |
| `day` | DateField | - | Date of question | Today | ✓ |
| `creation_time` | TimeField | - | Time created | NULL | - |
| `question` | TextField | - | Question text | '' | - |
| `option_1` | CharField | 250 | First option | Required | - |
| `option_2` | CharField | 200 | Second option | Required | - |
| `option_3` | CharField | 200 | Third option | Required | - |
| `option_4` | CharField | 200 | Fourth option | Optional | - |
| `option_5` | CharField | 200 | Fifth option | Optional | - |
| `ans` | IntegerField | - | Answer (1-5) | 1 | - |
| `extra` | TextField | - | Extra notes | '' | - |
| `new_id` | CharField | 300 | Generated ID | '' | ✓ |

**Category Fields (Boolean with db_index=True):**
```
appointment, Art_Culture, Awards_Honours, Business_Economy_Banking,
Defence, Environment, Government_Schemes, International, medical,
National, obituary, Persons_in_News, rank, Science_Techonlogy,
Sports, State, static_gk, important_day, agreement, mythology
```

---

## 📊 MCQ Info Tables: Metadata & Pagination

### Year-Based Info Tables

**Available Tables:**
- `mcq_info_2018` (Existing)
- `mcq_info_2019` (Existing)
- `mcq_info_2020` (Existing)
- `mcq_info_2026` (NEW - Created today)

### Structure of mcq_info_YYYY

**Metadata Fields:**

| Column | Type | Purpose |
|--------|------|---------|
| `id` | PK | Auto-increment |
| `total_mcq` | IntegerField | Total MCQ count for that year |
| `total_mcq_page` | IntegerField | Total pages (calculated: (total+300)/3) |
| `month_list` | TextField | Space-separated list of available months |

**Month Fields (Text):**
```
January, February, March, April, May, June,
July, August, September, October, November, December
```
*Each stores: "01 Jan, 2026///05 Jan, 2026///10 Jan, 2026" etc*

**Page Count Fields (Char):**
```
January_page, February_page, March_page, ... December_page
(Stores number of pages for that month)
```

---

## 🔄 Auto-Update Mechanism

### When MCQ is Saved

The `mcq_info_YYYY.save()` method automatically:

1. **Counts total MCQs**: `totall = mcq.objects.count()`
2. **Calculates total pages**: `total_mcq_page = int((totall+300)/3)`
3. **For each month**:
   - Counts entries: `mcq.objects.filter(year_now='2026', month='January').count()`
   - Formats dates: "01 Jan, 2026"
   - Stores in month field: `self.January = "01 Jan, 2026///05 Jan, 2026"...`
   - Stores page count: `self.January_page = str(count)`

**Result:** Pagination metadata updates automatically when MCQs are added/removed!

---

## 💾 MCQ Columns Available for Data Entry

### When Saving to `/admin/bank/mcq/add/`

**Essential Fields:**
- ✓ `question` - The question text
- ✓ `option_1` - First choice
- ✓ `option_2` - Second choice  
- ✓ `option_3` - Third choice
- ✓ `option_4` - Fourth choice (optional)
- ✓ `option_5` - Fifth choice (optional)
- ✓ `ans` - Correct answer number (1-5)

**Date & Organization:**
- ✓ `year_now` - Select from (2018, 2019, 2020, 2026)
- ✓ `month` - Select from 12 months
- ✓ `day` - Date when question appeared
- ✓ `creation_time` - Time created (optional)

**Categorization (Boolean flags):**
- ✓ `Science_Techonlogy`, `National`, `State`, `International`
- ✓ `Business_Economy_Banking`, `Environment`, `Defence`
- ✓ `Art_Culture`, `Awards_Honours`, `Persons_in_News`
- ✓ `Sports`, `medical`, `appointment`, etc.

**Metadata:**
- ✓ `extra` - Additional notes (optional)
- ◌ `new_id` - Auto-generated from question + date

---

## 🎯 Complete MCQ Creation Workflow

### Step 1: Get URL Data
```
When LLM scrapes URLs, extract:
- Question text
- Answer options (creates if not available)
- Correct answer position (1-5)
- Topic/Category for tagging
- Source date
```

### Step 2: Format with Date Prefix
```python
# When saving question, add date prefix:
question = "25-Jan-2026: " + question_text
```

**Example:**
```
25-Jan-2026: What is the capital of India?
```

### Step 3: Fill MCQ Form
```
year_now: 2026
month: January
day: 2026-01-25
creation_time: [current time]
question: "25-Jan-2026: What is the capital of India?"
option_1: "Delhi"
option_2: "Mumbai"
option_3: "Bangalore"
option_4: "Kolkata"
ans: 1
Science_Techonlogy: False
National: True
[other categories]: True/False as needed
```

### Step 4: Save
```
POST to http://localhost:8000/admin/bank/mcq/add/
```

### Step 5: Auto-Updates
```
✓ mcq_info_2026 auto-updates
✓ total_mcq recalculated
✓ January_page updated
✓ month_list refreshed
✓ Pagination ready for frontend
```

---

## 🔗 Frontend Display Integration

### Display MCQs on Page

**URL Structure:**
```
http://localhost:8000/current-affairs/mcq/current-affairs-January-2026/01/
```

**Data Flow:**
```
1. User clicks: January 2026, Page 1
   ↓
2. View queries: mcq.objects.filter(year_now='2026', month='January')
   ↓
3. Pagination calculated from: mcq_info_2026.January_page = "5"
   ↓
4. First 3 MCQs displayed
   ↓
5. Navigation buttons: [1] [2] [3] [4] [5]
```

---

## 📱 Example: Adding MCQs from URL

### Scenario: LLM fetches from 3 URLs

**URL 1:** news-site.com/question-25
```json
{
  "date": "2026-01-25",
  "question": "Which country signed trade deal?",
  "options": ["USA", "China", "India", "Japan"],
  "answer": 3
}
```

**LLM Processing:**
1. Extract all 3 URLs one by one
2. Parse: question, options, answer
3. Auto-create options if missing (LLM logic)
4. Format question: "25-Jan-2026: Which country signed trade deal?"
5. Categorize: National=True
6. Save to: `/admin/bank/mcq/add/`

**Database Result:**
```
year_now: 2026
month: January
day: 2026-01-25
question: "25-Jan-2026: Which country signed trade deal?"
option_1: "USA"
option_2: "China"
option_3: "India"
option_4: "Japan"
ans: 3
National: True
```

**Auto-Updated:**
```
mcq_info_2026.January = "25 Jan, 2026"
mcq_info_2026.January_page = "1"
mcq_info_2026.total_mcq += 1
```

---

## 🎓 Year System: 2018, 2019, 2020, 2026

### Historical Years (Legacy)
- `mcq_info_2018` - Contains past questions from 2018
- `mcq_info_2019` - Contains past questions from 2019
- `mcq_info_2020` - Contains past questions from 2020

### Current/Future Year
- `mcq_info_2026` - NEW TABLE for current year questions
- Automatically populated when MCQs are added with `year_now='2026'`
- Pagination updates in real-time
- Frontend displays: `/current-affairs/mcq/current-affairs-[Month]-2026/[Page]/`

---

## 🔍 Query Examples

### Get all MCQs for January 2026
```python
from bank.models import mcq
january_2026 = mcq.objects.filter(year_now='2026', month='January').order_by('-day')
```

### Get National category MCQs from 2026
```python
national_2026 = mcq.objects.filter(year_now='2026', National=True).order_by('-day')
```

### Get pagination info for January 2026
```python
from bank.models import mcq_info_2026
info = mcq_info_2026.objects.all()[0]
print(info.January_page)  # Number of pages in January
print(info.January)  # List of dates in January
```

### Pagination example (Page 1 of January)
```python
# Get first 3 MCQs for January 2026, Page 1
p = (1 - 1) * 3  # Start position
mul = 1 * 3       # End position
mcqs = mcq.objects.filter(year_now='2026', month='January').order_by('-day')[p:mul]
```

---

## 🚀 LLM Integration Instructions

### When LLM Saves MCQ:

**Step 1: Prepare Question**
```python
from datetime import date

# Get question data from URL
q_text = extracted_from_url['question']
options = extracted_from_url['options']
ans_num = extracted_from_url['answer']
topic = extracted_from_url['category']

# Format with date prefix
today = date.today()
formatted_q = f"{today.strftime('%d-%b-%Y')}: {q_text}"
```

**Step 2: Create Options**
```python
# If options not available in URL, LLM generates using genai
if not options or len(options) < 2:
    options = llm_generate_options(q_text)

# Ensure exactly 4-5 options
while len(options) < 4:
    options.append(llm_generate_option(q_text))
```

**Step 3: Save to Database**
```python
from bank.models import mcq

mcq.objects.create(
    year_now='2026',
    month=today.strftime('%B'),  # January, February, etc
    day=today,
    creation_time=now.time(),
    question=formatted_q,
    option_1=options[0],
    option_2=options[1],
    option_3=options[2],
    option_4=options[3] if len(options) > 3 else '',
    option_5=options[4] if len(options) > 4 else '',
    ans=ans_num,
    # Set category booleans
    National=topic == 'National',
    International=topic == 'International',
    # ... other categories ...
)
```

**Step 4: Auto-Update Happens**
```
✓ mcq_info_2026.save() called automatically
✓ total_mcq updated
✓ January_page recalculated
✓ January field updated with new date
✓ Frontend sees new content immediately
```

---

## 📌 Key Points

✓ **2026 table created** - mcq_info_2026 ready for new content
✓ **Date prefixing** - Questions include date: "25-Jan-2026: Question text"
✓ **Auto-pagination** - Info table updates automatically
✓ **Category tagging** - Set boolean fields for topic filtering
✓ **4 years available** - 2018, 2019, 2020, 2026
✓ **Multiple URLs** - LLM can fetch from many sources one by one
✓ **Option generation** - LLM creates options if not in URL
✓ **Real-time display** - Immediate availability on frontend after save

---

## 🔗 Related Documentation

- [CURRENT_AFFAIRS_ANALYSIS.md](./CURRENT_AFFAIRS_ANALYSIS.md) - Current affairs system
- [GENAI_WORKFLOW_GUIDE.md](./GENAI_WORKFLOW_GUIDE.md) - AI generation workflow
- [genai/models.py](./django/django_project/genai/models.py) - GenAI models

---

**Created:** January 25, 2026
**MCQ Tables:** 4 (2018, 2019, 2020, 2026)
**Status:** Ready for data ingestion
