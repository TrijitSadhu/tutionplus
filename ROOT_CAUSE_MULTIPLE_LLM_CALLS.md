# Root Cause Analysis: Why LLM is Called 3 Times Instead of 1

## The Issue

**Observed Behavior:**
- 1 source URL is fetched: `https://www.gktoday.in/bhairav-battalion-and-suryastra-debut-at-republic-day-parade/`
- 3 articles are extracted from that URL
- LLM is called 3 separate times (once for each article)
- Results: 3 different descriptive entries in database

**Expected Behavior (Based on Your Request):**
- 1 source URL → 1 LLM call → 1 result

---

## Root Cause: Article Extraction Strategy

### Where It Happens
**File:** [genai/tasks/current_affairs.py](genai/tasks/current_affairs.py)
**Method:** `extract_content()` - Lines 133-250
**Method:** `scrape_from_sources()` - Lines 332-361

### The Problem Flow

```
1. SOURCE URL
   └─ https://www.gktoday.in/bhairav-battalion-and-suryastra-debut-at-republic-day-parade/
   
2. SCRAPING (Lines 348-352)
   └─ Fetches HTML from URL
   └─ Calls extract_content(html, source_url)
   
3. EXTRACTION (Lines 215-242)
   └─ Finds all <article> or <div> containers
   └─ Extracts EACH article separately
   └─ Returns: List of 3 content items
      ├─ Article 1: Bhairav Battalion and Suryastra Debut...
      ├─ Article 2: Bhairav Battalion and Suryastra Debut...
      └─ Article 3: Bhairav Light Commando Battalion debuts...
   
4. PROCESSING (Lines 837-891 in run_complete_pipeline)
   └─ Loop: for idx, content in enumerate(content_list, 1):
   └─ For EACH article:
      ├─ Call process_descriptive_content() → LLM Call #1
      ├─ Call process_descriptive_content() → LLM Call #2
      └─ Call process_descriptive_content() → LLM Call #3
```

### Relevant Code Sections

**In `extract_content()` (lines 215-242):**
```python
articles = soup.find_all('article')  # Or similar fallback
# ... other selectors ...

print(f"    [EXTRACTION] Found {len(articles)} article containers")

for idx, article in enumerate(articles, 1):
    # Extract title, body from EACH article
    if title and body and len(body) > 50:
        content.append({  # ← Each article added separately
            'title': title[:200],
            'body': body[:2000],
            'source_url': source_url
        })
```

**In `scrape_from_sources()` (lines 345-358):**
```python
for idx, source_url in enumerate(sources, 1):  # ← Loop 1: For each SOURCE URL
    html = self.fetch_page(source_url)
    if html:
        content = self.extract_content(html, source_url)  # Returns LIST of articles
        all_content.extend(content)  # ← Adds ALL extracted articles to list
return all_content  # Returns: [article1, article2, article3, ...]
```

**In `run_complete_pipeline()` (lines 837-887):**
```python
for idx, content in enumerate(content_list, 1):  # ← Loop 2: For EACH article
    print(f"\n  [{idx}/{len(content_list)}] Processing: {display_title}...")
    
    if content_type == 'currentaffairs_mcq':
        processed = self.process_mcq_content(...)  # ← LLM Call for article 1
        # ... save ...
    else:
        processed = self.process_descriptive_content(...)  # ← LLM Call for article 2
        results['processed_items'].append(processed)      # ← LLM Call for article 3
```

---

## Why This Happens

### HTML Structure on the Website
The gktoday.in website likely has:
```html
<div class="item">
  <h2>Bhairav Battalion and Suryastra Debut...</h2>
  <p>First public appearance of Bhairav Battalion...</p>
</div>

<div class="item">
  <h2>Bhairav Battalion and Suryastra Debut...</h2>
  <p>The parade took place on Kartavya Path...</p>
</div>

<div class="item">
  <h2>Bhairav Light Commando Battalion debuts...</h2>
  <p>First public appearance of Bhairav Light Commando...</p>
</div>
```

The `extract_content()` method at line 215 finds ALL of these `<div class="item">` containers and extracts each as a separate article.

---

## Current Logic Chain

```
1 Source URL
   ↓
1 HTML Page Fetched
   ↓
3 Articles Extracted (all_content.extend(content))
   ↓
Return content_list with 3 items
   ↓
Process Each Item in Loop
   ↓
3 LLM Calls
   ↓
3 Entries in Database
```

---

## What You Need to Decide

To fix this, we need to know: **What should happen with multiple articles from one URL?**

### Option A: Combine All Articles Into One LLM Call
```
1 Source URL
   ↓
Extract all 3 articles
   ↓
Concatenate into single content block
   ↓
1 LLM Call with combined content
   ↓
1 Result in Database
```

**Changes needed:**
- Modify `extract_content()` to return a SINGLE content item with all articles combined
- OR modify `run_complete_pipeline()` to group articles by source_url and send them together

### Option B: Process Only First Article Per URL
```
1 Source URL
   ↓
Extract articles
   ↓
Keep only FIRST article
   ↓
1 LLM Call with first article only
   ↓
1 Result in Database
```

**Changes needed:**
- Modify `extract_content()` to return only first article
- OR modify scraper to stop after extracting enough

### Option C: Keep Current Behavior (3 Separate Entries)
This is what's happening now - each article gets its own database entry.

---

## My Recommendation

Before I make changes, please clarify:

1. **Should each article from the same URL be treated as separate content?** (Option C)
   - Pro: All content is preserved
   - Con: 3x LLM calls, 3x storage

2. **Should we combine all articles from one URL into a single prompt?** (Option A)
   - Pro: Efficient (1 LLM call)
   - Con: Very long prompts, might hit token limits

3. **Should we process only the first/main article per URL?** (Option B)
   - Pro: Efficient, clean
   - Con: Loses some content

**What's your preference?**
