/*
=== COMPREHENSIVE JSON EXAMPLES FOR BULK IMPORTS ===
Use these examples to import data for all subjects

Copy the JSON array format and paste into Django admin:
Admin > Genai > Json Imports > Add Json Import > Select Subject > Paste JSON
*/

// ============================================
// 1. POLITY - Standard MCQ Subject Example
// ============================================
// Field mapping:
// - question (required): The MCQ question
// - option_1, option_2, option_3, option_4, option_5: Answer options
// - ans: Correct answer (1-5)
// - chapter: Chapter number (1-41)
// - difficulty: easy/medium/hard (optional)
// - extra: Explanation (optional)
// - year_now, month, day: Date fields (optional)
// If no date fields, uses form date during import

[
  {
    "question": "Which article of the Indian Constitution deals with Fundamental Rights?",
    "option_1": "Articles 12-35",
    "option_2": "Articles 36-51",
    "option_3": "Articles 52-62",
    "option_4": "Articles 1-11",
    "option_5": "None of the above",
    "ans": 1,
    "chapter": "1",
    "difficulty": "easy",
    "extra": "Part III of Indian Constitution (Articles 12-35) deals with Fundamental Rights",
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-28"
  },
  {
    "question": "How many states are there in India?",
    "option_1": "28",
    "option_2": "29",
    "option_3": "30",
    "option_4": "31",
    "option_5": "32",
    "ans": 2,
    "chapter": "2",
    "difficulty": "easy"
  },
  {
    "question": "What is the term of the President?",
    "option_1": "4 years",
    "option_2": "5 years",
    "option_3": "6 years",
    "option_4": "7 years",
    "option_5": "8 years",
    "ans": 2,
    "chapter": "3",
    "difficulty": "medium",
    "extra": "President serves for 5 years with eligibility for re-election"
  }
]


// ============================================
// 2. HISTORY - Standard MCQ Subject Example
// ============================================

[
  {
    "question": "In which year did the Indian Rebellion of 1857 occur?",
    "option_1": "1855",
    "option_2": "1856",
    "option_3": "1857",
    "option_4": "1858",
    "option_5": "1859",
    "ans": 3,
    "chapter": "1",
    "difficulty": "easy",
    "extra": "Also known as the Sepoy Mutiny, it was the first major revolt against British rule"
  },
  {
    "question": "Who was the first Prime Minister of Independent India?",
    "option_1": "Rajendra Prasad",
    "option_2": "Jawaharlal Nehru",
    "option_3": "Sardar Vallabhbhai Patel",
    "option_4": "B.R. Ambedkar",
    "option_5": "Mahatma Gandhi",
    "ans": 2,
    "chapter": "2",
    "difficulty": "easy"
  }
]


// ============================================
// 3. GEOGRAPHY - Standard MCQ Subject Example
// ============================================

[
  {
    "question": "Which is the longest river in India?",
    "option_1": "Brahmaputra",
    "option_2": "Yamuna",
    "option_3": "Ganges",
    "option_4": "Indus",
    "option_5": "Godavari",
    "ans": 3,
    "chapter": "1",
    "difficulty": "easy"
  },
  {
    "question": "Which mountain range runs along the western coast of India?",
    "option_1": "Eastern Ghats",
    "option_2": "Western Ghats",
    "option_3": "Himalayas",
    "option_4": "Satpura Range",
    "option_5": "Aravalli Range",
    "ans": 2,
    "chapter": "2",
    "difficulty": "medium"
  }
]


// ============================================
// 4. ECONOMICS - Standard MCQ Subject Example
// ============================================

[
  {
    "question": "What is GDP?",
    "option_1": "Gross Domestic Product",
    "option_2": "Gross Development Program",
    "option_3": "Global Domestic Policy",
    "option_4": "General Development Plan",
    "option_5": "Government Development Proposal",
    "ans": 1,
    "chapter": "1",
    "difficulty": "easy"
  },
  {
    "question": "What is inflation?",
    "option_1": "Decrease in prices",
    "option_2": "Increase in prices",
    "option_3": "Stable prices",
    "option_4": "Control of money supply",
    "option_5": "Interest rate change",
    "ans": 2,
    "chapter": "2",
    "difficulty": "easy"
  }
]


// ============================================
// 5. PHYSICS - Standard MCQ Subject Example
// ============================================

[
  {
    "question": "What is the SI unit of force?",
    "option_1": "Dyne",
    "option_2": "Newton",
    "option_3": "Joule",
    "option_4": "Watt",
    "option_5": "Pascal",
    "ans": 2,
    "chapter": "1",
    "difficulty": "easy"
  },
  {
    "question": "What is the speed of light?",
    "option_1": "2 × 10^8 m/s",
    "option_2": "3 × 10^8 m/s",
    "option_3": "4 × 10^8 m/s",
    "option_4": "5 × 10^8 m/s",
    "option_5": "1 × 10^8 m/s",
    "ans": 2,
    "chapter": "2",
    "difficulty": "easy"
  }
]


// ============================================
// 6. BIOLOGY - Standard MCQ Subject Example
// ============================================

[
  {
    "question": "What is the basic unit of life?",
    "option_1": "Atom",
    "option_2": "Molecule",
    "option_3": "Cell",
    "option_4": "Tissue",
    "option_5": "Organ",
    "ans": 3,
    "chapter": "1",
    "difficulty": "easy"
  },
  {
    "question": "How many chambers does the human heart have?",
    "option_1": "2",
    "option_2": "3",
    "option_3": "4",
    "option_4": "5",
    "option_5": "6",
    "ans": 3,
    "chapter": "2",
    "difficulty": "easy"
  }
]


// ============================================
// 7. CHEMISTRY - Standard MCQ Subject Example
// ============================================

[
  {
    "question": "What is the atomic number of Oxygen?",
    "option_1": "6",
    "option_2": "7",
    "option_3": "8",
    "option_4": "9",
    "option_5": "10",
    "ans": 3,
    "chapter": "1",
    "difficulty": "easy"
  },
  {
    "question": "What is the pH value of neutral solution?",
    "option_1": "5",
    "option_2": "6",
    "option_3": "7",
    "option_4": "8",
    "option_5": "9",
    "ans": 3,
    "chapter": "2",
    "difficulty": "easy"
  }
]


// ============================================
// 8. REASONING - Standard MCQ Subject Example
// ============================================

[
  {
    "question": "In a series 2, 4, 8, 16, ?, what is the next number?",
    "option_1": "20",
    "option_2": "24",
    "option_3": "28",
    "option_4": "32",
    "option_5": "36",
    "ans": 4,
    "chapter": "1",
    "difficulty": "easy"
  }
]


// ============================================
// 9. ERROR - Standard MCQ Subject Example
// ============================================

[
  {
    "question": "Identify the error: 'She go to school every day'",
    "option_1": "She",
    "option_2": "go",
    "option_3": "to",
    "option_4": "school",
    "option_5": "every day",
    "ans": 2,
    "chapter": "1",
    "difficulty": "easy",
    "extra": "Should be 'goes' (third person singular)"
  }
]


// ============================================
// 10. MCQ - General Purpose MCQ Example
// ============================================

[
  {
    "question": "What is the capital of France?",
    "option_1": "London",
    "option_2": "Paris",
    "option_3": "Berlin",
    "option_4": "Madrid",
    "option_5": "Rome",
    "ans": 2,
    "chapter": "5",
    "difficulty": "easy"
  }
]


// ============================================
// 11. CURRENT AFFAIRS MCQ - Current Affairs Example
// ============================================
// Note: Options are limited to 4 (option_1 to option_4)
// Categories are AUTO-MAPPED (no need to set boolean fields)

[
  {
    "question": "Who became the Chief Justice of India in January 2026?",
    "option_1": "Justice A",
    "option_2": "Justice B",
    "option_3": "Justice C",
    "option_4": "Justice D",
    "ans": 1,
    "categories": ["National", "appointment"],
    "explanation": "Supreme Court of India leadership update",
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-15"
  },
  {
    "question": "What is the impact of the new economic policy?",
    "option_1": "Increased inflation",
    "option_2": "Reduced inflation",
    "option_3": "Stable prices",
    "option_4": "Currency devaluation",
    "ans": 2,
    "categories": ["National", "Business_Economy_Banking"],
    "explanation": "Economic policy changes January 2026",
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-20"
  }
]


// ============================================
// 12. CURRENT AFFAIRS DESCRIPTIVE - Example
// ============================================
// Maps to: upper_heading, yellow_heading, key_1-4, all_key_points

[
  {
    "upper_heading": "India-China Border Tensions",
    "yellow_heading": "Recent developments in military standoff",
    "key_1": "LAC disputes ongoing since 2020",
    "key_2": "Military buildups reported",
    "key_3": "Diplomatic talks initiated",
    "key_4": "Economic implications analyzed",
    "all_key_points": "LAC has been a contentious border. Military operations escalated. Multiple diplomatic channels engaged. Economic impact on bilateral trade.",
    "categories": ["National", "International", "Defence"],
    "year_now": "2026",
    "month": "January",
    "day": "2026-01-22"
  },
  {
    "upper_heading": "Climate Summit 2026",
    "yellow_heading": "Global agreement on carbon emissions",
    "key_1": "200+ nations participated",
    "key_2": "Targets set for 2030",
    "key_3": "India committed to renewable energy",
    "key_4": "Green technology investments pledged",
    "all_key_points": "Major climate summit concluded with binding agreement. Emission reduction targets set. India plays crucial role in climate action.",
    "categories": ["International", "Environment"]
  }
]


// ============================================
// 13. BULK IMPORT WITH NO DATES (Uses Form Date)
// ============================================
// Omit year_now, month, day fields and they will be filled from form date

[
  {
    "question": "Which is the smallest continent?",
    "option_1": "Europe",
    "option_2": "Australia",
    "option_3": "Africa",
    "option_4": "Antarctica",
    "option_5": "South America",
    "ans": 2,
    "chapter": "3"
  },
  {
    "question": "How many continents are there?",
    "option_1": "5",
    "option_2": "6",
    "option_3": "7",
    "option_4": "8",
    "option_5": "9",
    "ans": 3,
    "chapter": "3"
  }
]


// ============================================
// KEY FIELD MAPPING REFERENCE
// ============================================

STANDARD MCQ SUBJECTS (polity, history, geography, economics, physics, biology, chemistry, reasoning, error, mcq):
{
  "question": "Required - The MCQ question text",
  "option_1": "Required - Option A",
  "option_2": "Required - Option B",
  "option_3": "Required - Option C",
  "option_4": "Optional - Option D",
  "option_5": "Optional - Option E",
  "ans": "Required - Answer (1-5)",
  "chapter": "Optional - Chapter number (1-41)",
  "topic": "Optional - Default: 'question-answare'",
  "subtopic": "Optional - Default: 'mcq'",
  "subtopic_2": "Optional - Default: 'more'",
  "difficulty": "Optional - easy/medium/hard",
  "extra": "Optional - Explanation",
  "year_exam": "Optional - Exam year",
  "home": "Optional - Boolean (true/false)",
  "mocktest": "Optional - Boolean (true/false)",
  "year_now": "Optional - Year string (if omitted, uses form date)",
  "month": "Optional - Month name (if omitted, uses form date)",
  "day": "Optional - Date string YYYY-MM-DD (if omitted, uses form date)"
}

CURRENT AFFAIRS MCQ:
{
  "question": "Required",
  "option_1": "Required",
  "option_2": "Required",
  "option_3": "Required",
  "option_4": "Required",
  "ans": "Required (1-4 only)",
  "categories": "Optional - Array of category strings or single string",
  "explanation": "Optional",
  "extra": "Optional",
  "year_now": "Optional",
  "month": "Optional",
  "day": "Optional"
}

CURRENT AFFAIRS DESCRIPTIVE:
{
  "upper_heading": "Required",
  "yellow_heading": "Required",
  "key_1": "Optional",
  "key_2": "Optional",
  "key_3": "Optional",
  "key_4": "Optional",
  "all_key_points": "Optional - All important points",
  "paragraph": "Optional - Full description",
  "categories": "Optional - Array of category strings",
  "year_now": "Optional",
  "month": "Optional",
  "day": "Optional"
}
