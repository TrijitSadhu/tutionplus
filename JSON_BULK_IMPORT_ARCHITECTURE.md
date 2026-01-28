# JSON Bulk Import - Visual Architecture & Flow

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DJANGO ADMIN INTERFACE                   │
│                  /admin/genai/jsonimport/                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  List View              Add View         Actions            │
│  ────────              ────────         ───────             │
│  • All imports    →    • Table      →   • Bulk              │
│  • Record count        • JSON data      • Import            │
│  • Timestamps          • Save                               │
│                                             ↓               │
│                          Intermediate Form                  │
│                          ──────────────────                 │
│                          📅 Date Selection                  │
│                          ✅ Proceed Button                  │
│                                             ↓               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    BULK IMPORTER                            │
│                  genai/bulk_import.py                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  BulkImporter Class                                         │
│  ──────────────────                                         │
│  ├─ parse_json()           → Validates JSON syntax          │
│  ├─ get_model_class()      → Gets target Django model       │
│  ├─ extract_date_from_...  → Date priority logic            │
│  ├─ process_[model_type]() → Field mapping & save           │
│  └─ import_data()          → Main orchestrator              │
│                                                              │
│  Supported Processors:                                      │
│  • process_currentaffairs_mcq()         [Specialized]       │
│  • process_currentaffairs_descriptive() [Specialized]       │
│  • process_current_affairs_slide()      [Specialized]       │
│  • process_generic_model()              [Fallback]          │
│                                             ↓               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE OPERATIONS                      │
│                      bank/models.py                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Target Models (22+):                                       │
│  ├─ currentaffairs_mcq          [Specialized processor]     │
│  ├─ currentaffairs_descriptive  [Specialized processor]     │
│  ├─ current_affairs_slide       [Specialized processor]     │
│  ├─ total_english               [Generic processor]         │
│  ├─ total_math                  [Generic processor]         │
│  ├─ math                        [Generic processor]         │
│  ├─ job                         [Generic processor]         │
│  ├─ total_job                   [Generic processor]         │
│  ├─ total_job_category          [Generic processor]         │
│  ├─ total_job_state             [Generic processor]         │
│  ├─ home                        [Generic processor]         │
│  ├─ topic                       [Generic processor]         │
│  ├─ total                       [Generic processor]         │
│  └─ ... (7 more models)         [Generic processor]         │
│                                                              │
│  Operations:                                                │
│  • update_or_create() → Prevents duplicates                │
│  • Batch processing   → Multiple records per import        │
│  • Category mapping   → Sets boolean fields                │
│  • Date handling      → Stores with priority order         │
│                                             ↓               │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ✅ Data Persisted
                    📊 Success Report
```

---

## 🔄 Workflow Sequence

```
User Interaction Flow:
═════════════════════

1. ADMIN → Create JsonImport
   ├─ Select Table (dropdown)
   │  └─ currentaffairs_mcq
   │     currentaffairs_descriptive
   │     [21+ others...]
   ├─ Paste JSON (textarea)
   │  └─ [
   │       {"question": "...", "option_1": "...", ...},
   │       {"question": "...", "option_1": "...", ...}
   │     ]
   └─ Save

2. ADMIN → Go to JsonImport List
   ├─ Select records (checkbox)
   ├─ Action dropdown → "Bulk Import"
   └─ Click Go

3. INTERMEDIATE FORM
   ├─ Date field (calendar picker)
   │  └─ 2026-01-28 (used as fallback)
   └─ Submit Button → "Proceed"

4. PROCESSING
   ├─ Parse JSON
   ├─ For each record:
   │  ├─ Extract dates (JSON priority)
   │  ├─ Map fields to model
   │  ├─ Set categories
   │  └─ Create or update
   └─ Return result

5. SUCCESS MESSAGE
   ├─ ✅ Created: 50
   ├─ ✅ Updated: 10
   ├─ ❌ Errors: 2
   └─ Back to list
```

---

## 📊 Data Flow

```
JSON Input:
───────────

[
  {
    "question": "What is AI?",
    "option_1": "Artificial Intelligence",
    "option_2": "...",
    "option_3": "...",
    "option_4": "...",
    "ans": 1,
    "categories": ["Science_Techonlogy", "National"],
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-28"
  },
  {
    "question": "Define ML",
    "option_1": "Machine Learning",
    "option_2": "...",
    "option_3": "...",
    "option_4": "...",
    "ans": 1,
    "categories": ["Science_Techonlogy"]
    // ← No date fields, will use form date
  }
]
        ↓
    PARSING
    (JSON validation)
        ↓
   PROCESSING
   ──────────
   
   Record 1:
   ├─ question → "What is AI?"
   ├─ option_1-4 → mapped
   ├─ ans → 1
   ├─ categories → Science_Techonlogy=True, National=True, others=False
   ├─ year_now → "2026" (from JSON)
   ├─ month → "January" (from JSON)
   ├─ day → 2026-01-28 (from JSON)
   └─ ✅ INSERT/UPDATE
   
   Record 2:
   ├─ question → "Define ML"
   ├─ option_1-4 → mapped
   ├─ ans → 1
   ├─ categories → Science_Techonlogy=True, others=False
   ├─ year_now → "2026" (from form fallback)
   ├─ month → "January" (from form fallback)
   ├─ day → 2026-01-28 (from form fallback)
   └─ ✅ INSERT/UPDATE
        ↓
    DATABASE
    ────────
    currentaffairs_mcq table:
    ├─ Record 1: "What is AI?" (2026-01-28)
    ├─ Record 2: "Define ML" (2026-01-28)
    └─ ✅ Saved
        ↓
    SUCCESS
    ───────
    ✅ Created: 2
    ✅ Updated: 0
    ✅ Errors: 0
```

---

## 🔀 Decision Logic

### Date Priority

```
Is date in JSON?
│
├─ YES → Use JSON date
│        ├─ year_now?      → "2026"
│        ├─ month?         → "January"
│        └─ day?           → "2026-01-28"
│
└─ NO → Use form date as fallback
         ├─ year_now?      → form_date.year
         ├─ month?         → Month name from form_date
         └─ day?           → form_date
```

### Duplicate Detection

```
Model: currentaffairs_mcq

lookup = (question, day)

if exists(question, day):
    └─ UPDATE existing record ✅
else:
    └─ CREATE new record ✅

Result: No duplicates! 🎯
```

### Category Mapping

```
JSON: "categories": ["National", "Science_Techonlogy", "International"]

Model boolean fields:
├─ National = True ✅
├─ Science_Techonlogy = True ✅
├─ International = True ✅
├─ Business_Economy_Banking = False
├─ Defence = False
├─ Environment = False
└─ ... (all others) = False

Result: Fine-grained categorization! 🏷️
```

---

## 📈 Processing Pipeline

```
┌──────────────────┐
│   JSON Import    │
│   Model Created  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│   Admin Bulk Action Selected │
│   Date Form Displayed        │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│   BulkImporter Initialized   │
│   (table, json, date, time)  │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│   parse_json()               │
│   → Validates syntax         │
│   → Converts to list         │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│   get_model_class()          │
│   → Gets Django Model class  │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│   For each record:           │
│                              │
│   1. Extract dates           │
│      (JSON priority)         │
│                              │
│   2. Map fields              │
│      (JSON → Model)          │
│                              │
│   3. Set categories          │
│      (Array → Booleans)      │
│                              │
│   4. Create/Update           │
│      (ORM operation)         │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│   Compile Results            │
│   ├─ Created count           │
│   ├─ Updated count           │
│   ├─ Error list              │
│   └─ Success boolean         │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│   Display Success Message    │
│   ✅ Created: 50             │
│   ✅ Updated: 10             │
│   ❌ Errors: 2               │
└──────────────────────────────┘
```

---

## 📂 File Relationships

```
genai/
│
├── models.py
│   └─ JsonImport model (stores imports)
│       ├─ to_table (FK to model)
│       ├─ json_data (JSON text)
│       ├─ created_by (FK to User)
│       └─ timestamps
│
├── admin.py
│   ├─ JsonImportAdmin (list, add, actions)
│   ├─ BulkImportForm (date selection)
│   └─ bulk_import_action (triggers import)
│
├── bulk_import.py
│   └─ BulkImporter class (core logic)
│       ├─ parse_json()
│       ├─ get_model_class()
│       ├─ extract_date_from_record()
│       ├─ process_currentaffairs_mcq()
│       ├─ process_currentaffairs_descriptive()
│       ├─ process_current_affairs_slide()
│       ├─ process_generic_model()
│       └─ import_data()
│
└── migrations/
    └─ 0015_jsonimport.py (database schema)

templates/admin/genai/
└── bulk_import_form.html (date picker form)

bank/
└── models.py (all 22+ target models)
```

---

## 🎯 Key Features Summary

| Feature | How It Works | Benefit |
|---------|-------------|---------|
| **Table Selection** | Dropdown of 22+ bank models | Choose target table easily |
| **JSON Input** | Paste JSON array directly | No file upload needed |
| **Date Priority** | JSON dates > Form date > Today | Flexible date handling |
| **Category Mapping** | Array → Boolean fields | Auto-categorize records |
| **Duplicate Prevention** | Match by (field + date) | No accidental duplicates |
| **Batch Processing** | Process multiple records | Import 100s at once |
| **Error Handling** | Log errors, continue | Partial success okay |
| **Audit Trail** | created_by, timestamps | Track who imported what |
| **Admin Integration** | Seamless admin UI | No extra tools needed |

---

## ✅ Implementation Status

```
┌─────────────────────────────────────────┐
│  Feature Implementation Checklist        │
├─────────────────────────────────────────┤
│ ✅ JsonImport Model                     │
│ ✅ BulkImporter Utility                 │
│ ✅ Admin Interface                      │
│ ✅ Intermediate Form                    │
│ ✅ Database Migration                   │
│ ✅ All 22+ Models                       │
│ ✅ Date Priority Logic                  │
│ ✅ Category Mapping                     │
│ ✅ Duplicate Prevention                 │
│ ✅ Error Handling                       │
│ ✅ Logging                              │
│ ✅ Documentation                        │
│ ✅ Examples                             │
│ ✅ Verification                         │
└─────────────────────────────────────────┘

Status: 🎉 COMPLETE & READY TO USE
```

---

## 🚀 Getting Started

```
1. Go to Admin
   → /admin/genai/jsonimport/

2. Click "Add JSON Import"
   → Select table
   → Paste JSON
   → Save

3. Select Record
   → Check checkbox
   → Action: "Bulk Import"
   → Go

4. Select Date
   → Pick import date
   → Proceed

5. Done! ✅
   → Records imported
   → See success message
```

