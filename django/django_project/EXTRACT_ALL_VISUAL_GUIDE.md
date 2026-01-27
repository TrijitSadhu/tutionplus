# Extract ALL MCQs - Visual Guide

## Form Layout

```
╔════════════════════════════════════════════════════════════════════╗
║               PROCESS PDF TO MCQ - FORM                            ║
╚════════════════════════════════════════════════════════════════════╝

┌─ CHAPTER ──────────────────────────────────────────────────────────┐
│ Dropdown: [Select Chapter 1-41...]                                 │
│ Help: Leave blank to not filter by chapter                          │
└────────────────────────────────────────────────────────────────────┘

┌─ DIFFICULTY LEVEL ─────────────────────────────────────────────────┐
│ Required! Choose one:                                              │
│ ○ Easy (Simple, straightforward questions)                         │
│ ○ Medium (Standard difficulty)                                     │
│ ● Hard (UPSC Civil Services level)                                │
└────────────────────────────────────────────────────────────────────┘

┌─ EXTRACT ALL MCQs FROM PDF ────────────────────────────────────────┐
│ ☑ Extract ALL MCQs from PDF                          ← NEW!        │
│ ✓ Check this to extract ALL MCQs from the PDF                     │
│ ✓ (ignores Number of MCQs field)                                  │
└────────────────────────────────────────────────────────────────────┘

┌─ NUMBER OF MCQs TO GENERATE ──────────────────────────────────────┐
│ Input: [5]                                                         │
│ Help: Enter any number of MCQs to generate                         │
│      (ignored if "Extract ALL" is checked)                         │
└────────────────────────────────────────────────────────────────────┘

┌─ PAGE FROM (Optional) ─────────────────────────────────────────────┐
│ Input: [0]                                                         │
│ Help: Start page number (0 for beginning)                          │
└────────────────────────────────────────────────────────────────────┘

┌─ PAGE TO (Optional) ───────────────────────────────────────────────┐
│ Input: [ ]                                                         │
│ Help: End page number (inclusive). Leave blank for end of PDF      │
└────────────────────────────────────────────────────────────────────┘

                    [SUBMIT]  [CANCEL]
```

## Decision Tree

```
                     PDF Processing Form
                            │
                            ↓
                Is "Extract ALL" checked?
                   /                    \
                 YES                    NO
                 │                       │
                 ↓                       ↓
        Set num_items = 999999    Use entered number
                 │                  (e.g., 5, 10, 25)
                 │                       │
                 └───────────┬───────────┘
                             ↓
                    PDF Processor Receives
                             │
                             ↓
                   Is num_items == 999999?
                        /         \
                      YES         NO
                       │           │
                       ↓           ↓
                Create prompt:  Create prompt:
                "Extract ALL    "Generate N
                questions"      questions"
                       │           │
                       └───────────┴──────────┐
                                              ↓
                                        Send to LLM
                                              │
                                              ↓
                                       Return all MCQs
                                        or N MCQs
```

## Form States Comparison

```
╔═══════════════════════════════════════════════════════════════════╗
║                     BEFORE (Old System)                            ║
╠═══════════════════════════════════════════════════════════════════╣
║ You had to:                                                        ║
║ 1. Manually count MCQs in PDF                                     ║
║ 2. Enter the exact number                                         ║
║ 3. If wrong, miss questions                                       ║
║                                                                    ║
║ Form:                                                              ║
║ ┌──────────────────────────────────────────────────────────────┐  ║
║ │ Chapter: [Select...]                                         │  ║
║ │ Difficulty: [Easy/Medium/Hard]                              │  ║
║ │ Number of MCQs: [5] ← Had to count manually                 │  ║
║ │                                                              │  ║
║ │                    [SUBMIT]                                 │  ║
║ └──────────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════╗
║                      NOW (New System)                              ║
╠═══════════════════════════════════════════════════════════════════╣
║ You can:                                                           ║
║ 1. Just check "Extract ALL MCQs"                                 ║
║ 2. Or specify exact number                                        ║
║ 3. No need to count manually                                      ║
║                                                                    ║
║ Form:                                                              ║
║ ┌──────────────────────────────────────────────────────────────┐  ║
║ │ Chapter: [Select...]                                         │  ║
║ │ Difficulty: [Easy/Medium/Hard]                              │  ║
║ │                                                              │  ║
║ │ ☑ Extract ALL MCQs from PDF      ← NEW! Just check!        │  ║
║ │                                                              │  ║
║ │ Number of MCQs: [5]    (optional, ignored if ☑)            │  ║
║ │                                                              │  ║
║ │                    [SUBMIT]                                 │  ║
║ └──────────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════════╝
```

## Interaction Scenarios

### Scenario A: Extract ALL MCQs
```
┌────────────────────────────────────────┐
│ ADMIN FORM - User Input                 │
├────────────────────────────────────────┤
│ Chapter:              3                 │
│ Difficulty:           Medium            │
│ ☑ Extract ALL MCQs   YES               │
│ Number of MCQs:       5 (ignored)      │
│ Page From:            0                │
│ Page To:              (blank)          │
│ [SUBMIT]                               │
└────────────────────────────────────────┘
           │
           ↓ Form submitted
┌────────────────────────────────────────┐
│ ADMIN PROCESSING (admin.py)             │
├────────────────────────────────────────┤
│ extract_all = True                      │
│ num_items = 999999 ← Marker set        │
│                                         │
│ Creates ProcessingLog(                  │
│   num_items = 999999,                  │
│   chapter = 3,                          │
│   difficulty = 'medium'                 │
│ )                                       │
└────────────────────────────────────────┘
           │
           ↓ Task queued
┌────────────────────────────────────────┐
│ PDF PROCESSOR                           │
├────────────────────────────────────────┤
│ 1. Extract PDF content                  │
│ 2. Detect content type: MCQ            │
│ 3. Check num_items == 999999? YES      │
│ 4. Convert 999999 → "ALL"              │
│ 5. Format prompt:                       │
│    "Extract ALL multiple choice        │
│     questions from the content..."     │
│ 6. Send to LLM                          │
└────────────────────────────────────────┘
           │
           ↓ LLM processes
┌────────────────────────────────────────┐
│ LLM RESPONSE                            │
├────────────────────────────────────────┤
│ {                                       │
│   "questions": [                        │
│     Q1: {...},                          │
│     Q2: {...},                          │
│     Q3: {...},                          │
│     ... (all from PDF) ...             │
│     Q47: {...}                          │
│   ]                                     │
│ }                                       │
│ ✓ Total: 47 questions extracted        │
└────────────────────────────────────────┘
           │
           ↓ Save to database
┌────────────────────────────────────────┐
│ DATABASE                                │
├────────────────────────────────────────┤
│ Polity Table:                           │
│ ├─ Question 1 (Chapter 3)              │
│ ├─ Question 2 (Chapter 3)              │
│ ├─ Question 3 (Chapter 3)              │
│ ├─ ...                                 │
│ └─ Question 47 (Chapter 3)             │
│                                         │
│ ProcessingLog:                          │
│ └─ num_items = 999999 (audit trail)   │
└────────────────────────────────────────┘
```

### Scenario B: Generate Exact 10 MCQs
```
┌────────────────────────────────────────┐
│ ADMIN FORM - User Input                 │
├────────────────────────────────────────┤
│ Chapter:              5                 │
│ Difficulty:           Hard              │
│ ☐ Extract ALL MCQs   NO                │
│ Number of MCQs:       10                │
│ Page From:            0                │
│ Page To:              (blank)          │
│ [SUBMIT]                               │
└────────────────────────────────────────┘
           │
           ↓ Form submitted
┌────────────────────────────────────────┐
│ ADMIN PROCESSING (admin.py)             │
├────────────────────────────────────────┤
│ extract_all = False                     │
│ num_items = 10 ← User value            │
│                                         │
│ Creates ProcessingLog(                  │
│   num_items = 10,                       │
│   chapter = 5,                          │
│   difficulty = 'hard'                   │
│ )                                       │
└────────────────────────────────────────┘
           │
           ↓ Task queued
┌────────────────────────────────────────┐
│ PDF PROCESSOR                           │
├────────────────────────────────────────┤
│ 1. Extract PDF content                  │
│ 2. Detect content type                  │
│ 3. Check num_items == 999999? NO       │
│ 4. num_items = 10 (unchanged)          │
│ 5. Format prompt:                       │
│    "Generate 10 high-quality MCQs      │
│     aligned with competitive exams..."│
│ 6. Send to LLM                          │
└────────────────────────────────────────┘
           │
           ↓ LLM processes
┌────────────────────────────────────────┐
│ LLM RESPONSE                            │
├────────────────────────────────────────┤
│ {                                       │
│   "questions": [                        │
│     Q1: {...},                          │
│     Q2: {...},                          │
│     ...                                │
│     Q10: {...}                          │
│   ]                                     │
│ }                                       │
│ ✓ Total: 10 questions (exactly)       │
│ ✓ Difficulty: HARD (UPSC-level)       │
└────────────────────────────────────────┘
```

## Console Output Comparison

### When Extract ALL is Used:
```
================================================================================
[LLM INPUT] Sending prompt to LLM
================================================================================
Prompt Type: mcq
Task Type: pdf_to_mcq
Subject: polity
Content Type: MCQ
Options Available: True
Difficulty: easy
Mode: EXTRACT ALL MCQs from PDF          ← Shows EXTRACT ALL
Prompt Length: 2450 characters
────────────────────────────────────────────────────────────────────────────────
```

### When Specific Number is Used:
```
================================================================================
[LLM INPUT] Sending prompt to LLM
================================================================================
Prompt Type: mcq
Task Type: pdf_to_mcq
Subject: polity
Content Type: MCQ
Options Available: True
Difficulty: hard
Num Questions Requested: 10              ← Shows specific number
Prompt Length: 2450 characters
────────────────────────────────────────────────────────────────────────────────
```

## Value Flow

```
User Interface
    │
    ├─ Input: extract_all checkbox (True/False)
    ├─ Input: num_items (5, 10, 25, etc.)
    │
    ↓
Admin Processing Layer (admin.py)
    │
    ├─ IF extract_all == True:
    │  └─→ num_items = 999999 ← MARKER
    │
    ├─ ELSE:
    │  └─→ num_items = user_input
    │
    ↓
ProcessingLog Created
    │
    └─ num_items stored (999999 or user value)
    
    ↓
PDF Processor (pdf_processor.py)
    │
    ├─ Check: IF num_items == 999999?
    │
    ├─ YES: Convert to "ALL" for prompt
    │  └─→ "Extract ALL questions"
    │
    ├─ NO: Keep value
    │  └─→ "Generate N questions"
    │
    ↓
LLM Receives Instruction
    │
    ├─ Extract ALL MCQs, OR
    ├─ Generate exactly N MCQs
    │
    ↓
LLM Returns Results
    │
    └─ All MCQs saved to database
```

---

**Visual Guide:** Ready for use  
**Date:** January 27, 2026
