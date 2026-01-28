// JSON Bulk Import - Quick Examples

// ==========================================
// Example 1: Current Affairs MCQ Records
// ==========================================

[
  {
    "question": "What is GDP?",
    "option_1": "Gross Domestic Product",
    "option_2": "Gross Development Product",
    "option_3": "Global Domestic Product",
    "option_4": "Growth Domestic Product",
    "ans": 1,
    "categories": ["Business_Economy_Banking", "National"],
    "extra": "GDP measures the total monetary value of goods and services produced in a country",
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-28",
    "creation_time": "10:30:00",
    "is_live": true
  },
  {
    "question": "Who is the current RBI Governor?",
    "option_1": "Urjit Patel",
    "option_2": "Sanjay Malhotra",
    "option_3": "Raghuram Rajan",
    "option_4": "Y. V. Reddy",
    "ans": 2,
    "categories": ["National", "Persons_in_News"],
    "extra": "Sanjay Malhotra became RBI Governor in December 2023",
    // No date fields provided → will use form date automatically
  }
]


// ==========================================
// Example 2: Current Affairs Descriptive
// ==========================================

[
  {
    "upper_heading": "India's Space Mission: Chandrayaan-3",
    "yellow_heading": "Successful lunar landing mission",
    "key_1": "Successfully landed on the lunar south pole",
    "key_2": "Cost: $75 million",
    "key_3": "Chandrayaan-1 found water ice on the Moon",
    "key_4": "Part of India's exploration program",
    "all_key_points": "India's Chandrayaan-3 made a historic landing on the south pole of the Moon in August 2023, marking India as the first country to successfully reach this region.",
    "categories": ["Science_Techonlogy", "National"],
    "paragraph": "The Chandrayaan-3 mission was launched in July 2023. It successfully soft-landed near the south pole region of the Moon on August 23, 2023, with a lander and rover.",
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-28"
  }
]


// ==========================================
// Example 3: Mixed with and without dates
// ==========================================

[
  {
    "question": "What is the Preamble to the Constitution?",
    "option_1": "Opening statement of the Constitution",
    "option_2": "Final section of the Constitution",
    "option_3": "Amendment to the Constitution",
    "option_4": "Explanation of rights",
    "ans": 1,
    "categories": ["National"],
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-20",
    "creation_time": "09:15:00"
    // This record HAS date fields → uses JSON dates
  },
  {
    "question": "Define Sovereignty",
    "option_1": "Unlimited power of the government",
    "option_2": "Independence and self-governance",
    "option_3": "Power of the monarchy",
    "option_4": "Control by foreign powers",
    "ans": 2,
    "categories": ["National"]
    // This record has NO date fields → will use form date (2026-01-28)
  }
]


// ==========================================
// Example 4: Minimal Required Fields (MCQ)
// ==========================================

[
  {
    "question": "What is photosynthesis?",
    "option_1": "Process of water absorption",
    "option_2": "Process of converting light to chemical energy",
    "option_3": "Process of respiration",
    "option_4": "Process of decomposition",
    "ans": 2
    // Minimal: Only required fields
    // Will use today's date + default time when imported
  }
]


// ==========================================
// Example 5: Common Field Mapping
// ==========================================

MCQ Record Mapping:
{
  "question"       → Model: question (TextField)
  "option_1"       → Model: option_1 (CharField)
  "option_2"       → Model: option_2 (CharField)
  "option_3"       → Model: option_3 (CharField)
  "option_4"       → Model: option_4 (CharField, optional)
  "option_5"       → Model: option_5 (CharField, optional)
  "ans"            → Model: ans (IntegerField, 1-5 or "A"-"E")
  "year_now"       → Model: year_now (CharField, optional)
  "month"          → Model: month (CharField, optional)
  "day"            → Model: day (DateField, optional)
  "creation_time"  → Model: creation_time (TimeField, optional)
  "categories"     → Model: [Boolean fields] (optional)
  "extra"          → Model: extra (TextField, optional)
  "is_live"        → Model: is_live (BooleanField, optional)
}

Descriptive Record Mapping:
{
  "upper_heading"  → Model: upper_heading (CharField)
  "yellow_heading" → Model: yellow_heading (CharField)
  "key_1"          → Model: key_1 (CharField)
  "key_2"          → Model: key_2 (CharField)
  "key_3"          → Model: key_3 (CharField)
  "key_4"          → Model: key_4 (CharField, optional)
  "year_now"       → Model: year_now (CharField, optional)
  "month"          → Model: month (CharField, optional)
  "day"            → Model: day (DateField, optional)
  "creation_time"  → Model: creation_time (TimeField, optional)
  "categories"     → Model: [Boolean fields] (optional)
  "all_key_points" → Model: all_key_points (TextField, optional)
  "paragraph"      → Model: paragraph (TextField, optional)
  "link"           → Model: link (TextField, optional)
  "url"            → Model: url (TextField, optional)
}


// ==========================================
// Example 6: Category Examples
// ==========================================

Valid Categories (as string array):
[
  "National",                    // India-specific
  "International",              // Global news
  "State",                       // State-specific
  "Science_Techonlogy",         // Technology/Science
  "Business_Economy_Banking",   // Business/Economy
  "Environment",                // Environmental
  "Defence",                    // Military/Defence
  "Sports",                     // Sports
  "Art_Culture",                // Arts/Culture
  "Awards_Honours",             // Awards
  "Persons_in_News",           // Notable people
  "Government_Schemes",         // Government programs
  "appointment",                // Appointments
  "obituary",                   // Deaths
  "important_day",              // Special days
  "rank",                       // Rankings
  "mythology",                  // Historical references
  "agreement",                  // Treaties/Agreements
  "medical",                    // Medical
  "static_gk"                   // Static GK
]

Example:
{
  "question": "...",
  "option_1": "...",
  // ...
  "categories": ["National", "Business_Economy_Banking", "Sports"]
  // Will set National=True, Business_Economy_Banking=True, Sports=True
  // All other categories set to False
}


// ==========================================
// Example 7: Date Formats Accepted
// ==========================================

Day field accepts:
- "2026-01-28"        ✅ (ISO format)
- "28/01/2026"        ✅ (DD/MM/YYYY)
- 2026-01-28          ✅ (as actual date object if you're using API)

Creation time format:
- "10:30:00"          ✅ (HH:MM:SS)
- "10:30"             ❌ (will fail - needs seconds)

Month accepts:
- "January", "February", "March", ... "December"
- Case doesn't matter

Year accepts:
- Any string: "2025", "2026", "2027", etc.


// ==========================================
// Example 8: Update Existing Records
// ==========================================

If you import the SAME question with SAME date:
→ The system will UPDATE the existing record instead of creating a duplicate

Original record:
{
  "question": "What is AI?",
  "option_1": "Artificial Intelligence",
  "option_2": "...",
  "ans": 1,
  "day": "2026-01-28"
}

New import (same question + day):
{
  "question": "What is AI?",
  "option_1": "Artificial Intelligence (Updated)",  ← Updated
  "option_2": "...",
  "ans": 1,
  "day": "2026-01-28",
  "categories": ["Science_Techonlogy"]  ← Added categories
}

Result: Record is UPDATED, no duplicate created


// ==========================================
// Example 9: Correct Answer Formats
// ==========================================

All these are equivalent:
{
  "ans": 1           ✅ Integer
}

{
  "ans": "1"         ✅ String number
}

{
  "ans": "A"         ✅ Letter (auto-converted: A→1, B→2, C→3, D→4)
}

{
  "correct_answer": 2  ✅ Alternative field name
}


// ==========================================
// Testing & Validation
// ==========================================

Before importing to production:

1. Validate JSON syntax:
   → https://jsonlint.com/

2. Count records:
   → JSON should be a [ ] array
   → Each item { } is one record

3. Check required fields:
   → MCQ: question, option_1-4, ans
   → Descriptive: upper_heading, yellow_heading, key_1-4

4. Small test import:
   → Import 1-2 records first
   → Check admin to verify it worked
   → Then import the rest in batches

