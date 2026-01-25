# MCQ Admin Interface - Quick Access Guide

## 🔐 Access Admin

**URL:** http://localhost:8000/admin/bank/mcq/

**Login:** Use your Django admin credentials

---

## ➕ Add New MCQ

**URL:** http://localhost:8000/admin/bank/mcq/add/

### Form Fields

```
┌─────────────────────────────────────────┐
│         MCQ Add Form                    │
├─────────────────────────────────────────┤
│                                         │
│ Year Now*          [Select ▼]          │
│  ├─ 2018                               │
│  ├─ 2019                               │
│  ├─ 2020                               │
│  └─ 2026 ◄── NEW FOR 2026             │
│                                         │
│ Month*             [Select ▼]          │
│  ├─ January                            │
│  ├─ February                           │
│  └─ ... December                       │
│                                         │
│ Day*               [Date Picker]       │
│                    (Today by default)  │
│                                         │
│ Creation Time      [Time Field]        │
│                    (Optional)          │
│                                         │
│ Question*          [Large Text Area]   │
│  Example:                              │
│  "25-Jan-2026: What is the capital    │
│   of India?"                           │
│                                         │
│ Option 1*          [Text Input 250]    │
│                    "Delhi"             │
│                                         │
│ Option 2*          [Text Input 200]    │
│                    "Mumbai"            │
│                                         │
│ Option 3*          [Text Input 200]    │
│                    "Bangalore"         │
│                                         │
│ Option 4           [Text Input 200]    │
│                    "Kolkata" (Optional)│
│                                         │
│ Option 5           [Text Input 200]    │
│                    (Optional)          │
│                                         │
│ Ans*               [Number Input]      │
│                    (1-5, default: 1)   │
│                                         │
│ ──────────────────────────────────────│
│ CATEGORIES (Check all that apply)      │
│                                         │
│ ☑ Science_Techonlogy                   │
│ ☐ National                             │
│ ☐ State                                │
│ ☐ International                        │
│ ☐ Business_Economy_Banking             │
│ ☐ Environment                          │
│ ☐ Defence                              │
│ ☐ Art_Culture                          │
│ ☐ Awards_Honours                       │
│ ☐ Persons_in_News                      │
│ ☐ Sports                               │
│ ☐ medical                              │
│ ☐ appointment                          │
│ ☐ obituary                             │
│ ☐ rank                                 │
│ ☐ Government_Schemes                   │
│ ☐ important_day                        │
│ ☐ static_gk                            │
│ ☐ agreement                            │
│ ☐ mythology                            │
│                                         │
│ ──────────────────────────────────────│
│ Extra                [Text Area]       │
│                     (Optional notes)   │
│                                         │
│ ──────────────────────────────────────│
│                                         │
│         [ Save and add another ]       │
│         [ Save and continue editing ]  │
│         [ Save ]                       │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📝 Sample Form Submission

### Example: Adding MCQ from URL

**Input Data:**

```
URL: news.com/story/25jan2026-india-trade
Question: What is India's new trade agreement?
Options: USA, China, Japan, EU
Correct: Option 3 (Japan)
Topic: International, Business
Date: 25-Jan-2026
```

### Form Filling:

```
Year Now:         2026 ◄── Select from dropdown
Month:            January ◄── Select from dropdown
Day:              25-01-2026 ◄── Date picker or manual
Creation Time:    [Leave blank for now()]

Question:         25-Jan-2026: What is India's new trade agreement?
                  (Prefix with date)

Option 1:         USA
Option 2:         China
Option 3:         Japan ◄── Correct answer
Option 4:         EU
Option 5:         [Leave blank]

Ans:              3 ◄── Position of correct answer

Categories:
  ☑ International ◄── Check this
  ☑ Business_Economy_Banking ◄── Check this
  ☐ National
  ☐ State
  [others unchecked]

Extra:            Source: news.com/story/25jan2026-india-trade

[Click: Save and add another]
```

---

## 🔄 Batch Operations

### View All MCQs for 2026

**URL:** http://localhost:8000/admin/bank/mcq/?year_now=2026

**Filters Available:**
- Year Now: 2018, 2019, 2020, 2026
- Month: January-December
- Day: Date range
- Categories: All boolean fields

### Search MCQs

```
Search box searches:
- Question text
- Options
- Extra notes
- ID
```

**Example:** Search "trade" finds all trade-related MCQs

---

## 🔧 Edit Existing MCQ

**URL:** http://localhost:8000/admin/bank/mcq/[ID]/change/

**Example:** http://localhost:8000/admin/bank/mcq/705/change/

All fields are editable. Save changes to update.

---

## 📊 MCQ Info 2026 Management

**URL:** http://localhost:8000/admin/bank/mcq_info_2026/

**View:**
```
Total MCQ:          47
Total MCQ Page:     16
Month List:         January February March April May June July
                    August September October November December

January:            01 Jan, 2026///05 Jan, 2026///10 Jan, 2026...
January_page:       5

February:           12 Feb, 2026///15 Feb, 2026...
February_page:      3

[... other months ...]
```

**Note:** This auto-updates when MCQs are added/removed!

---

## 💡 Pro Tips

### Date Prefix Consistency
```
✓ Format: DD-MMM-YYYY (e.g., 25-Jan-2026)
✓ Always include date at start of question
✓ Example: "25-Jan-2026: Complete the analogy"

This helps:
- Track when question was added
- Sort chronologically
- Identify outdated questions
```

### Option Guidelines
```
✓ Keep options concise (under 200 chars)
✓ Mix correct/incorrect at random
✓ Avoid "All of above" style (unless intentional)
✓ Same length for all options is OK
✓ Different lengths make answer more obvious
```

### Category Selection
```
✓ Select ALL relevant categories
✓ A question can have multiple categories
✓ Example: 
  - "India-Japan trade" = International + Business + National
  - "Climate action" = Environment + National + International

✓ Helps users filter questions by interest
```

### Testing
```
✓ After adding MCQ via admin
✓ Check frontend: 
   http://localhost:8000/current-affairs/mcq/
   current-affairs-January-2026/01/
✓ Should appear in 1-2 seconds
✓ Pagination updates automatically
```

---

## 🚨 Common Issues

### Issue: 2026 option not showing
**Solution:** Refresh page or restart server
```bash
# Server may cache choices
python manage.py runserver
```

### Issue: Question not appearing on frontend
**Solution:** Check:
1. Year = 2026
2. Month = Current month
3. Day = Exact match (or within range)
4. Pagination recalculated

### Issue: Pagination showing 0 pages
**Solution:** Navigate to:
```
http://localhost:8000/admin/bank/mcq_info_2026/
```
Click the single entry and click Save (triggers auto-update)

### Issue: Date format wrong
**Solution:** Use Django date picker
```
Click calendar icon → Select date
Or type: YYYY-MM-DD (2026-01-25)
```

---

## 📋 Quick Checklist for Adding MCQ

- [ ] Year = 2026
- [ ] Month selected from dropdown
- [ ] Day set to actual date
- [ ] Question includes date prefix (25-Jan-2026: ...)
- [ ] Option 1, 2, 3 filled (required)
- [ ] Correct answer number set (1-5)
- [ ] At least one category checked
- [ ] Click Save
- [ ] Verify on frontend

---

## 🔗 Integration with GenAI

When LLM generates MCQ from URL:

```python
from django.contrib.auth import get_user_model
from bank.models import mcq

def save_mcq_from_url(url_data):
    """Fetch URL and save MCQ"""
    
    # Parse URL
    question = url_data['question']
    options = url_data.get('options') or generate_options(question)
    answer = url_data['answer']
    category = url_data.get('category', 'National')
    
    # Add date prefix
    today = date.today()
    formatted_q = f"{today.strftime('%d-%b-%Y')}: {question}"
    
    # Save
    mcq.objects.create(
        year_now='2026',
        month=today.strftime('%B'),
        day=today,
        question=formatted_q,
        option_1=options[0],
        option_2=options[1],
        option_3=options[2],
        option_4=options[3] if len(options) > 3 else '',
        option_5=options[4] if len(options) > 4 else '',
        ans=answer,
        National=(category == 'National'),
        International=(category == 'International'),
        # ... other categories ...
    )
```

---

**Admin Access:** http://localhost:8000/admin/bank/mcq/
**Add New:** http://localhost:8000/admin/bank/mcq/add/
**2026 Info:** http://localhost:8000/admin/bank/mcq_info_2026/
