# 📥 JSON Bulk Import Feature - Complete Guide

## Overview
The JSON Bulk Import feature allows you to import large amounts of data directly into any bank model table using JSON format. This is useful for bulk migrations, data transfers, or importing prepared datasets.

---

## ✅ What Was Implemented

### 1. **JsonImport Model** (`genai/models.py`)
- **`to_table`**: Dropdown field to select target bank model (all 22 tables supported)
- **`json_data`**: Large text field to paste JSON array of objects
- **`created_at`**: Auto-timestamp
- **`created_by`**: User who created the import

### 2. **BulkImporter Utility** (`genai/bulk_import.py`)
- Parses JSON data safely
- Maps JSON fields to model fields automatically
- Handles date/time extraction from JSON (priority: JSON > Form date)
- Supports all bank models with specialized processors for:
  - `currentaffairs_mcq` (MCQ records with categories)
  - `currentaffairs_descriptive` (Descriptive records)
  - `current_affairs_slide` (Slide records)
  - Generic fallback for other models
- Creates or updates records (duplicate prevention)

### 3. **Admin Interface** (`genai/admin.py`)
- JSON Import list view with record count
- **"Bulk Import" Action**: Batch import with intermediate date selection form
- Date field for fallback (if not in JSON)
- Success/error messages

### 4. **Template** (`templates/admin/genai/bulk_import_form.html`)
- Clean intermediate form for date selection
- Shows selected records before processing
- One-click import button

---

## 🎯 Supported Bank Models

1. `currentaffairs_mcq` - Current Affairs MCQ
2. `currentaffairs_descriptive` - Current Affairs Descriptive
3. `current_affairs_slide` - Current Affairs Slide
4. `total` - Total
5. `total_english` - Total English
6. `total_math` - Total Math
7. `total_job` - Total Job
8. `total_job_category` - Total Job Category
9. `total_job_state` - Total Job State
10. `home` - Home
11. `topic` - Topic
12. `math` - Math
13. `job` - Job
14. `the_hindu_word_Header1` - The Hindu Word Header 1
15. `the_hindu_word_Header2` - The Hindu Word Header 2
16. `the_hindu_word_list1` - The Hindu Word List 1
17. `the_hindu_word_list2` - The Hindu Word List 2
18. `the_economy_word_Header1` - The Economy Word Header 1
19. `the_economy_word_Header2` - The Economy Word Header 2
20. `the_economy_word_list1` - The Economy Word List 1
21. `the_economy_word_list2` - The Economy Word List 2

---

## 📋 JSON Format Guide

### For `currentaffairs_mcq` Records

```json
[
  {
    "question": "What is the capital of France?",
    "option_1": "Paris",
    "option_2": "Lyon",
    "option_3": "Marseille",
    "option_4": "Toulouse",
    "ans": 1,
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-28",
    "creation_time": "10:30:00",
    "categories": ["International", "Geography"],
    "extra": "Paris is the capital and largest city of France.",
    "is_live": true
  }
]
```

**Supported Fields:**
- `question` (required) - The MCQ question text
- `option_1`, `option_2`, `option_3`, `option_4`, `option_5` - Options
- `ans` - Correct answer (1, 2, 3, 4, 5 OR "A", "B", "C", "D", "E")
- `year_now` - Year (string, optional)
- `month` - Month name (string, optional)
- `day` - Date (optional, formats: "2026-01-28" or "28/01/2026")
- `creation_time` - Time (optional, format: "HH:MM:SS")
- `categories` - Array of category strings (optional)
- `extra` - Explanation or extra info (optional)
- `is_live` - Boolean to show on webpage (optional)

**Category Options:**
- National, International, State
- Science_Techonlogy, Business_Economy_Banking, Environment, Defence
- Sports, Art_Culture, Awards_Honours, Persons_in_News
- Government_Schemes, appointment, obituary, important_day
- rank, mythology, agreement, medical, static_gk

---

### For `currentaffairs_descriptive` Records

```json
[
  {
    "upper_heading": "Economic Reforms in India",
    "yellow_heading": "Recent policy changes",
    "key_1": "GST implementation",
    "key_2": "Foreign Direct Investment",
    "key_3": "Make in India initiative",
    "key_4": "Infrastructure development",
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-28",
    "creation_time": "10:30:00",
    "categories": ["Business_Economy_Banking", "National"],
    "all_key_points": "Summary of key points",
    "paragraph": "Detailed paragraph",
    "link": "https://example.com",
    "url": "https://example.com/article"
  }
]
```

**Supported Fields:**
- `upper_heading` (required) - Main heading
- `yellow_heading` - Secondary heading
- `key_1`, `key_2`, `key_3`, `key_4` - Key points
- `year_now`, `month`, `day`, `creation_time` - Date/time (optional)
- `categories` - Array of category strings (optional)
- `all_key_points` - Summary (optional)
- `paragraph` - Detailed text (optional)
- `link`, `url` - References (optional)

---

## 🚀 How to Use

### Step 1: Prepare JSON Data
Create a JSON file with your data as an array of objects following the format guide above.

### Step 2: Go to Django Admin
1. Navigate to `/admin/genai/jsonimport/`
2. Click **"Add JSON Import"**

### Step 3: Fill the Form
1. **Select Target Table** - Choose the bank model you want to import to
2. **Paste JSON Data** - Copy-paste your JSON array into the text field
3. Click **Save**

### Step 4: Run Bulk Import
1. Go to `/admin/genai/jsonimport/`
2. **Check the records** you want to import
3. From the **Action** dropdown, select **"📥 Bulk Import (Select records & proceed)"**
4. Click **Go**
5. **Select Import Date** - This is the fallback date for records without date fields
6. Click **"✅ Proceed with Import"**

### Step 5: View Results
- Success message shows: "Created: X, Updated: Y, Errors: Z"
- Check the admin list to verify imported records

---

## ⚙️ Date Handling Logic

The system uses this **priority order** for dates:

1. **First Priority**: Values in JSON (year_now, month, day, creation_time)
   - If present in JSON, these values are used
   - Ignores the form date field

2. **Second Priority**: Date from the intermediate form
   - If JSON doesn't have date fields, form date is used
   - Applied to all records lacking date info

3. **Default**: Today's date + current time
   - If neither JSON nor form provides dates
   - Used as absolute fallback

### Example:
```json
{
  "question": "Q1",
  "option_1": "A",
  "option_2": "B",
  "option_3": "C",
  "option_4": "D",
  "ans": 1,
  "year_now": "2026",
  "month": "February",
  "day": "2026-02-15"
  // ↑ These dates will be used, form date is IGNORED
}
```

---

## 🔄 Update vs Create Logic

The system automatically handles duplicates:

- **For currentaffairs_mcq**: Matches by `question + day`, updates if exists
- **For currentaffairs_descriptive**: Matches by `upper_heading + day`, updates if exists
- **Other models**: Matches by first available unique field
- **Result**: No duplicate entries, existing records updated with new values

---

## 📊 Supported Field Types

| Type | Examples | Handling |
|------|----------|----------|
| **String** | question, option_1, upper_heading | Directly assigned |
| **Integer** | ans (1-5), year, day | Converted from string if needed |
| **Boolean** | is_live, Science_Techonlogy | 'true'/'false' or True/False |
| **Date** | 2026-01-28 or 28/01/2026 | Auto-converted |
| **Time** | 10:30:00 | Parsed as HH:MM:SS |
| **Array** | ["cat1", "cat2"] | Each item set as boolean field |

---

## ❌ Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid JSON | Syntax error in JSON | Check JSON syntax at jsonlint.com |
| Missing required field | e.g., `question` is required for MCQ | Add the required field |
| Unknown table | Wrong table name selected | Select from the dropdown |
| Type mismatch | ans = "Five" instead of 5 | Use correct types |

All errors are logged and reported after import.

---

## 🔍 Example: Complete MCQ Import

### Prepare this JSON:

```json
[
  {
    "question": "Which country is the largest by population?",
    "option_1": "India",
    "option_2": "China",
    "option_3": "USA",
    "option_4": "Indonesia",
    "ans": 1,
    "categories": ["National", "Geography"],
    "extra": "As of 2024, India has surpassed China",
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-28",
    "creation_time": "10:00:00",
    "is_live": true
  },
  {
    "question": "What is the capital of Australia?",
    "option_1": "Sydney",
    "option_2": "Canberra",
    "option_3": "Melbourne",
    "option_4": "Brisbane",
    "ans": 2,
    "categories": ["International"],
    "year_now": "2026",
    "month": "January",
    "is_live": true
  }
]
```

### Steps:
1. Go to `/admin/genai/jsonimport/` → **Add JSON Import**
2. Select Table: **"Current Affairs MCQ"**
3. Paste the JSON above
4. Click **Save**
5. Go back to list, **Select** both records
6. Action: **"📥 Bulk Import"** → **Go**
7. Select Date: **2026-01-28** (fallback for 2nd record)
8. Click **"✅ Proceed with Import"**

**Result**: 
- ✅ 2 MCQ records created with categories set
- ✅ Date fields auto-filled
- ✅ First record uses JSON dates, second uses form date

---

## 🛠️ Technical Details

### File Structure:
```
genai/
├── models.py                 # JsonImport model
├── admin.py                  # JsonImportAdmin + BulkImportForm
├── bulk_import.py           # BulkImporter class (core logic)
└── migrations/
    └── 0015_jsonimport.py   # Database migration
templates/admin/genai/
└── bulk_import_form.html    # Intermediate form template
```

### Key Classes:

**`BulkImporter` (genai/bulk_import.py)**
- `__init__(table_name, json_data, form_date, form_time)`
- `parse_json()` - Validates JSON
- `get_model_class()` - Gets Django model
- `import_data()` - Main method, returns result dict
- `process_currentaffairs_mcq()` - MCQ-specific logic
- `process_currentaffairs_descriptive()` - Descriptive-specific logic
- `process_generic_model()` - Fallback for other models

---

## 📝 Notes

- **No file upload**: Data is pasted directly as JSON text
- **Batch processing**: Import multiple records at once
- **Safe**: Validates all data before saving
- **Logged**: All imports logged for audit trail
- **Reversible**: Update records by re-importing with new data

---

## 🎓 Example: Importing from Spreadsheet

If you have data in Excel/CSV:
1. Convert to JSON using a tool: https://www.convertcsv.com/csv-to-json.htm
2. Adjust field names to match bank model fields
3. Paste into admin form
4. Import!

---

## ✨ Features Summary

✅ Supports 22+ bank models  
✅ Automatic date field handling (JSON priority > Form > Today)  
✅ Category auto-mapping (array of strings)  
✅ Duplicate prevention (update if exists)  
✅ Batch import in one click  
✅ Error reporting with details  
✅ Admin interface integration  
✅ User tracking (created_by)  
✅ Audit trail (created_at, updated_at)  
✅ Flexible field mapping per model  

---

## 🎯 Next Steps

1. **Test**: Create a small JSON with 2-3 records, import to test
2. **Verify**: Check admin list to confirm records were created
3. **Scale**: Once working, import larger batches
4. **Automate**: If needed, can be integrated with management commands

