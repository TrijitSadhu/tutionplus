# URL-Specific Prompt Routing - Complete Analysis

## Quick Answer

**YES** - When you use URLs (instead of PDFs), the system ALSO can use URL-specific prompts, but the routing logic is **DIFFERENT** from PDF processing.

---

## The Two Processing Paths

### Path 1: PDF Upload (What You've Been Testing)
```
Admin → Upload PDF → task_router.py → Uses task_type (pdf_to_mcq, pdf_currentaffairs_mcq, etc.)
```
- Uses `task_type` parameter
- Searches for prompts like `pdf_to_mcq_polity`, `pdf_currentaffairs_mcq`, etc.

### Path 2: URL Fetching (Scraping from Website)
```
Admin → Select URL from ContentSource → current_affairs.py → Uses source_url directly from ContentSource
```
- Uses `source_url` parameter (the URL itself, not a task_type)
- Searches for prompts matching that specific URL

---

## How URL-Specific Prompts Work

### In `current_affairs.py` (lines 369-408)

```python
def get_prompt_from_database(self, prompt_type: str, source_url: str = None) -> str:
    """
    Fetch prompt from database for a given source URL and prompt type
    """
    
    # Step 1: Search for SITE-SPECIFIC prompt first
    if source_url:
        prompt = query.filter(source_url=source_url, is_default=False).first()
        if prompt:
            print(f"✓ Found SITE-SPECIFIC prompt for {source_url[:50]}")
            return prompt.prompt_text
    
    # Step 2: Fall back to DEFAULT prompt
    prompt = query.filter(is_default=True).first()
    if prompt:
        print(f"✓ Using DEFAULT prompt for type '{prompt_type}'")
        return prompt.prompt_text
```

**Key Difference from PDF routing:**
- Searches for `source_url=<actual_URL>` (the real website URL)
- NOT `source_url=pdf_currentaffairs_mcq` (a task_type pattern)

---

## The URL Processing Flow

### For Current Affairs MCQ from URLs

```
1. Admin Action: "📖 Fetch Current Affairs MCQ"
   ↓
2. fetch_all_content management command called
   ↓
3. fetch_and_process_current_affairs('currentaffairs_mcq', skip_scraping=False)
   ↓
4. CurrentAffairsProcessor.run_complete_pipeline()
   ↓
5. Fetches all active ContentSource entries with source_type='currentaffairs_mcq'
   ↓
6. For EACH source URL:
   a) Scrapes website to get content
   b) Calls get_prompt_from_database('mcq', source_url='https://example.com/news')
   c) Searches: LLMPrompt with source_url='https://example.com/news', prompt_type='mcq'
   d) If found: Uses URL-specific prompt
   e) If NOT found: Uses default prompt (source_url='', is_default=True)
   f) Generates MCQs using the selected prompt
   g) Saves to database
```

---

## Example Scenario

### Scenario: You have 3 URLs configured

In ContentSource table:
```
1. URL: https://thehindu.com/news
   source_type: currentaffairs_mcq
   name: "The Hindu News - MCQ"
   is_active: True

2. URL: https://indianexpress.com/news
   source_type: currentaffairs_mcq
   name: "Indian Express - MCQ"
   is_active: True

3. URL: https://bbc.com/news
   source_type: currentaffairs_descriptive
   name: "BBC News - Descriptive"
   is_active: True
```

### You Create URL-Specific Prompts (Optional)

In LLMPrompt table:
```
ID | source_url                              | prompt_type | is_default | is_active
1  | https://thehindu.com/news               | mcq         | False      | True
2  | https://indianexpress.com/news          | mcq         | False      | True
3  | https://bbc.com/news                    | descriptive | False      | True
4  | (empty string)                          | mcq         | True       | True
5  | (empty string)                          | descriptive | True       | True
```

### When You Fetch MCQ from URLs

```
Process:
1. Fetch URL #1: https://thehindu.com/news
   → Searches for prompt with source_url='https://thehindu.com/news'
   → FOUND (ID: 1) → Uses Hindu-specific MCQ prompt
   → Generates MCQs with Hindu-specific logic

2. Fetch URL #2: https://indianexpress.com/news
   → Searches for prompt with source_url='https://indianexpress.com/news'
   → FOUND (ID: 2) → Uses Indian Express-specific MCQ prompt
   → Generates MCQs with Indian Express-specific logic

3. If you add new URL without specific prompt:
   → Searches for that URL's prompt
   → NOT FOUND
   → Falls back to default prompt (ID: 4, is_default=True)
   → Uses generic MCQ prompt
```

---

## Comparison: PDF vs URL Prompt Routing

| Feature | PDF Upload | URL Fetching |
|---------|-----------|--------------|
| **Entry Point** | Upload PDF file | Select URL from ContentSource |
| **Management Command** | process_pdf_content | fetch_all_content |
| **Routing Logic** | task_router.py | current_affairs.py |
| **Searches for** | `source_url=pdf_currentaffairs_mcq` (pattern) | `source_url=https://example.com` (actual URL) |
| **Can Use Site-Specific?** | Only if explicitly created as `pdf_currentaffairs_mcq`, etc. | YES - can create prompt for each URL |
| **Prompt Field** | task_type parameter | source_url parameter |

### Prompt Search Examples

**PDF Upload:**
```python
# File: task_router.py, Line 66-70
if task_type.startswith('pdf_to_'):
    source_url = f"{task_type}_{subject}"  # e.g., "pdf_to_mcq_polity"
else:
    source_url = f"pdf_{subject}_{prompt_type}"  # e.g., "pdf_current_affairs_mcq"

# Searches: LLMPrompt.objects.get(source_url='pdf_current_affairs_mcq')
```

**URL Fetching:**
```python
# File: current_affairs.py, Line 388-393
if source_url:  # source_url = "https://thehindu.com/news"
    prompt = query.filter(source_url=source_url, is_default=False).first()
    
# Searches: LLMPrompt.objects.get(source_url='https://thehindu.com/news')
```

---

## Why Create URL-Specific Prompts?

### ✅ Good Reasons

1. **Different Website Formats**
   - The Hindu has a specific article structure
   - Indian Express has a different structure
   - BBC has yet another structure
   - Different prompts can optimize extraction

2. **Quality Control**
   - You can tune prompt for each source
   - Get better MCQs from sites that work well
   - Use simpler prompt for sites with poor content

3. **Category Handling**
   - The Hindu focuses on Indian politics
   - BBC focuses on international news
   - BBC prompt could ask for categories specific to international affairs

### ❌ When You DON'T Need Them

- If one generic prompt works for all sources
- If you're using default prompts anyway
- If sources have similar content structure

---

## Setting Up URL-Specific Prompts

### Step 1: Add ContentSource (URL)

In Django Admin:
1. Go to "Content Sources"
2. Add new source:
   - Name: "The Hindu News MCQ"
   - source_type: "Current Affairs MCQ Source"
   - URL: `https://www.thehindu.com/news/`
   - content_date: Today's date
   - is_active: ✓

### Step 2: Create URL-Specific Prompt (Optional)

In Django Admin:
1. Go to "LLM Prompts"
2. Add new prompt:
   - source_url: `https://www.thehindu.com/news/`
   - prompt_type: `mcq`
   - prompt_text: (Your custom MCQ prompt tailored for The Hindu)
   - is_default: ☐ (Unchecked)
   - is_active: ✓

### Step 3: Fetch with Admin Action

In ProcessingLog Admin:
1. Select a ProcessingLog entry
2. Click action: "📖 Fetch Current Affairs MCQ"
3. System will:
   - Get all ContentSource with source_type='currentaffairs_mcq'
   - For each URL, search for matching prompt
   - Use URL-specific prompt if found, else default
   - Generate and save MCQs

---

## Current State of Your System

### What Exists Now

✅ **PDF Processing Prompts:**
- `pdf_current_affairs_mcq` (ID: 49) - Has category classification
- Default `mcq` prompt (should exist)
- Default `descriptive` prompt (should exist)

⚠️ **URL-Specific Prompts:**
- None created yet
- System will fall back to default prompts

### When You Process From URLs Today

```
1. Click "Fetch Current Affairs MCQ"
   ↓
2. Gets all ContentSource URLs with source_type='currentaffairs_mcq'
   ↓
3. For each URL, searches: LLMPrompt.objects.get(source_url='<URL>')
   ↓
4. NOT FOUND (no URL-specific prompts created)
   ↓
5. Falls back to: LLMPrompt.objects.get(source_url='', prompt_type='mcq', is_default=True)
   ↓
6. Uses default MCQ prompt
```

---

## Key Takeaway

| Processing Type | URL Path | Prompt Searches For |
|---|---|---|
| **PDF → Current Affairs MCQ** | PDF Upload | `pdf_current_affairs_mcq` (✅ EXISTS ID: 49) |
| **URL → Current Affairs MCQ** | Website URL | `<actual_URL>` (❌ if not created, uses default) |
| **PDF → Current Affairs Descriptive** | PDF Upload | `pdf_current_affairs_descriptive` (❌ if not created, uses default) |
| **URL → Current Affairs Descriptive** | Website URL | `<actual_URL>` (❌ if not created, uses default) |

**Your Prompt ID 49 (`pdf_current_affairs_mcq`)** is specifically for PDFs, NOT for URL fetching.

If you want custom handling for URL fetching, you need to create **separate prompts** with the actual URLs as `source_url`.

---

## Commands to Check Current State

```bash
cd django_project
python manage.py shell

# Check all prompts
from genai.models import LLMPrompt
for p in LLMPrompt.objects.filter(is_active=True):
    print(f"ID: {p.id:3} | source_url: {p.source_url:45} | type: {p.prompt_type:12} | default: {p.is_default}")

# Check ContentSource entries
from genai.models import ContentSource
for cs in ContentSource.objects.filter(is_active=True):
    print(f"ID: {cs.id} | {cs.get_source_type_display()} | {cs.url[:50]}")
```
