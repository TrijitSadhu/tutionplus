# Three Processing Modes - Visual Guide

## 1. Standard Scraping (Default)

```
ContentSource.send_url_directly = False  ✗
ContentSource.skip_scraping = False      ✗

URL: https://gktoday.in/article
        ↓
[Step 1] scrape_from_sources()
        ├─ Fetch HTML
        ├─ Parse article structure
        └─ Extract: Title, Body, Author, Date
        ↓
[Step 2] Process each article separately
        ├─ Article 1 → LLM Call
        ├─ Article 2 → LLM Call
        └─ Article 3 → LLM Call
        ↓
        ❌ 3 LLM Calls from 1 URL
        ❌ (But with your fix: Combines into 1 call)
        
Output: MCQ/Descriptive entries in database
```

---

## 2. Skip-Scraping Mode (Downloaded Content)

```
ContentSource.send_url_directly = False  ✗
ContentSource.skip_scraping = True       ✓

URL: https://gktoday.in/article
        ↓
[Step 1] Get URL from ContentSource
        ↓
[Step 2] Download Page
        ├─ Selenium.fetch_page() → Full HTML (388KB)
        └─ No article detection
        ↓
[Step 3] Extract Text
        ├─ Remove <script>, <style> tags
        ├─ Extract all text
        └─ Limit to 5000 chars
        ↓
[Step 4] Send to LLM
        └─ 1 LLM Call with full-page text
        ↓
Output: MCQ/Descriptive entries in database
```

---

## 3. URL-Only Mode (NEW - Sends URL Directly)

```
ContentSource.send_url_directly = True   ✓
ContentSource.skip_scraping = * (ignored)

URL: https://gktoday.in/article
        ↓
[Step 1] Get URL from ContentSource
        ↓
[Step 2] Check Flags
        ├─ send_url_directly = True
        ├─ SKIP downloading
        └─ SKIP content extraction
        ↓
[Step 3] Send URL String to LLM
        └─ body = "https://gktoday.in/article"
        ↓
[Step 4] LLM Processes URL
        └─ LLM has URL only, no content
        └─ LLM needs internet to fetch
        ↓
Output: MCQ/Descriptive entries in database
```

---

## Comparison Table

| Aspect | Standard | Skip-Scraping | URL-Only |
|--------|----------|---------------|----------|
| **Model Setting** | skip_scraping=False<br/>send_url_directly=False | skip_scraping=True<br/>send_url_directly=False | send_url_directly=True |
| **Processing** | Article detection | HTML-to-text extraction | None |
| **Download** | ✓ Yes (via article parser) | ✓ Yes (Selenium) | ✗ No |
| **Content Extraction** | ✓ Smart (per-article) | ✓ Generic (full page) | ✗ None |
| **LLM Receives** | Article content | Extracted text (5000 chars) | URL string |
| **LLM Calls** | 1 per article | 1 per URL | 1 per URL |
| **LLM Needs Internet** | ✗ No | ✗ No | ✓ Yes |
| **Best For** | News/article sites | Generic web pages | Testing/special cases |
| **Quality** | Highest | High | Lowest |

---

## Code Decision Tree

```python
if skip_scraping=True:
    Get URLs from ContentSource table
    
    for each URL:
        ├─ Check send_url_directly flag
        │
        ├─ IF send_url_directly=True:
        │  └─ 🔗 URL-ONLY MODE
        │     content['body'] = URL string
        │     # No downloading, no extraction
        │
        └─ ELIF send_url_directly=False:
           └─ 📥 SKIP-SCRAPING MODE
              ├─ Download HTML with Selenium
              ├─ Extract text (5000 chars max)
              └─ content['body'] = extracted text
else:
    # Standard scraping (existing code)
    Use scrape_from_sources()
```

---

## Admin Checkbox Layout

In Django Admin for ContentSource:

```
[ ] is_active                    ← Enable/disable source
[ ] skip_scraping                ← Mode 2: Download content
[ ] send_url_directly            ← Mode 3: URL only (takes precedence)
```

---

## Use Case Examples

### When to use Standard Scraping
- Scraping news websites (gktoday.in)
- Multiple articles on same page
- High quality extraction needed

### When to use Skip-Scraping
- Generic web pages with varying structure
- Don't need intelligent article detection
- Just want all page text to LLM

### When to use URL-Only
- Testing LLM capability with URLs
- When LLM has internet access (custom model)
- Benchmarking LLM's web understanding
- Simple quick tests

---

## Migration Applied ✓

```
Applying genai.0012_auto_20260127_0500... OK
```

Both fields:
- `skip_scraping` (for Mode 2)
- `send_url_directly` (for Mode 3)

Added to ContentSource model with `default=False` for backward compatibility.
