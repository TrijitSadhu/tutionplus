# Extract ALL MCQs from PDF - Feature Guide

## Overview
A new checkbox option has been added to the PDF processing form that allows you to **extract ALL MCQs** from a PDF without having to specify a number.

## Problem Solved
Previously, you had to:
- Know how many MCQs were in the PDF
- Specify that number in the "Number of MCQs" field (default was 5)
- If the PDF had 50 MCQs but you put 5, only 5 would be generated/extracted

Now you can simply check "Extract ALL MCQs from PDF" and the system will extract or generate every MCQ from the PDF.

## How to Use

### Step 1: Open Admin Panel
```
http://localhost:8000/admin/
```

### Step 2: Select PDF(s)
- Go to PDF Upload section
- Select one or more PDFs you want to process

### Step 3: Choose Action
- Click either:
  - **"🔄 Process to MCQ"** - For MCQ-based PDFs (will extract existing or create new)
  - **"📝 Process to Descriptive"** - For descriptive content PDFs (will create questions)

### Step 4: Fill the Form
The form will appear with the following fields:

```
┌─────────────────────────────────────────────┐
│ Chapter (Optional)                           │
│ [Select Chapter 1-41...]                    │
│                                              │
│ Difficulty Level (Required) *                │
│ [Easy / Medium / Hard]                       │
│                                              │
│ ☑ Extract ALL MCQs from PDF                │
│ "Check this to extract ALL MCQs from the   │
│  PDF (ignores Number of MCQs field)"        │
│                                              │
│ Number of MCQs to Generate                  │
│ [5] (default, ignored if Extract ALL)       │
│                                              │
│ Page From (Optional)                        │
│ [0] (start from beginning)                  │
│                                              │
│ Page To (Optional)                          │
│ [ ] (end of PDF)                            │
│                                              │
│ [Submit]  [Cancel]                          │
└─────────────────────────────────────────────┘
```

## Two Usage Scenarios

### Scenario 1: Extract ALL MCQs
When PDF contains existing MCQs that you want to extract completely:

1. **Check**: ✅ "Extract ALL MCQs from PDF"
2. **Set**: Difficulty Level = Easy/Medium/Hard
3. **Leave**: "Number of MCQs" unchanged (it will be ignored)
4. **Click**: Submit

**What happens:**
- System detects content type as "MCQ" mode
- LLM receives instruction: "Extract ALL multiple choice questions"
- Every MCQ in the PDF will be extracted/created
- Options will be extracted or intelligently created
- Language will be simplified
- All MCQs saved to subject table

### Scenario 2: Generate Specific Number
When you want to generate a specific number (not all):

1. **Uncheck**: ☐ "Extract ALL MCQs from PDF"
2. **Enter**: Number like 10, 25, 50, 100, etc.
3. **Set**: Difficulty Level = Easy/Medium/Hard
4. **Click**: Submit

**What happens:**
- System generates only that specific number
- Example: If you put 25, it generates exactly 25 MCQs
- Works for both MCQ extraction and Descriptive-to-MCQ creation

## Console Output

When you use "Extract ALL", the console will show:

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
Mode: EXTRACT ALL MCQs from PDF          ← This indicates Extract ALL is active
Prompt Length: 2450 characters
────────────────────────────────────────────────────────────────────────────────
PROMPT:
You are an expert educational content creator specializing in Polity.
Extract ALL multiple choice questions...   ← Notice "Extract ALL" instead of "Generate 5"
...
================================================================================
```

## Behind the Scenes

### Technical Implementation

**Form Change:**
- Added new checkbox field `extract_all` to ProcessPDFForm
- When checked: Sets `num_items = 999999` (internal marker)
- When unchecked: Uses the specified number in `num_items` field

**PDF Processor Change:**
- Detects when `num_items == 999999`
- Converts to "ALL" when formatting LLM prompt
- Tells LLM: "Extract ALL multiple choice questions"
- LLM generates/extracts every MCQ from the PDF

**Database Change:**
- ProcessingLog still stores `num_items = 999999`
- Database knows this means "extract all"
- Audit trail is complete and searchable

## Files Modified

1. **genai/admin.py**
   - Added `extract_all` checkbox field to ProcessPDFForm
   - Updated form processing logic to handle extract_all flag
   - Updated debug output to show "Extract ALL" mode

2. **genai/tasks/pdf_processor.py**
   - Updated `generate_mcq_prompt()` to detect 999999 marker
   - Changed prompt text from "Generate N questions" to "Extract ALL questions"
   - Updated prompt substitution to convert 999999 to "ALL"
   - Updated console output to show "Mode: EXTRACT ALL MCQs from PDF"

## Examples

### Example 1: Extract 50 MCQs from Polity PDF
```
Form Input:
- Chapter: 3
- Difficulty: Medium
- Extract ALL MCQs: ✅ CHECKED
- Number of MCQs: (ignored)

Result:
✓ All MCQs from the PDF extracted
✓ Options created/simplified
✓ Difficulty level = Medium
✓ Chapter = 3 for all
✓ All saved to Polity table
```

### Example 2: Generate 10 Specific MCQs
```
Form Input:
- Chapter: 5
- Difficulty: Hard
- Extract ALL MCQs: ☐ UNCHECKED
- Number of MCQs: 10

Result:
✓ Exactly 10 MCQs generated
✓ UPSC-level difficulty questions
✓ Chapter = 5 for all
✓ All saved to subject table
```

### Example 3: Extract All from Specific Page Range
```
Form Input:
- Chapter: 2
- Difficulty: Easy
- Extract ALL MCQs: ✅ CHECKED
- Page From: 5
- Page To: 15

Result:
✓ All MCQs from pages 5-15 extracted
✓ Language simplified to Easy level
✓ Chapter = 2 for all
✓ All saved to subject table
```

## Troubleshooting

**Q: I checked "Extract ALL" but only got 5 MCQs**
- A: The PDF might only contain 5 MCQs. Check manually.
- A: Content detection might have failed. Check console logs for "Content Type: MCQ"

**Q: Why does "Number of MCQs" still appear if it's ignored?**
- A: For flexibility - you might want to uncheck "Extract ALL" and use that field
- A: Always shows so you can quickly switch between modes

**Q: Can I use page range with "Extract ALL"?**
- A: Yes! You can specify Page From/Page To to limit the range, then Extract ALL from that range

**Q: What if the PDF has no MCQs?**
- A: System will auto-detect this and create questions in Descriptive-to-MCQ mode
- A: Check console output: "Content Type: DESCRIPTIVE" means it's creating from scratch

## Summary

| Feature | Before | After |
|---------|--------|-------|
| Extract all MCQs | Had to count and enter number | Just check "Extract ALL" |
| Specify exact count | Could enter any number | Enter number, leave "Extract ALL" unchecked |
| Form clarity | One field for both modes | Separate checkbox + number field |
| Console output | Ambiguous | Shows "EXTRACT ALL MCQs" explicitly |

---

**Status:** ✅ Feature implemented and ready to use
**Test Date:** January 27, 2026
