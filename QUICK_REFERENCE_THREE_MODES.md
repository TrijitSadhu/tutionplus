# Quick Reference: Three Processing Modes

## Admin Checkbox Behavior

```
SETTING 1: skip_scraping = ☐/☑
SETTING 2: send_url_directly = ☐/☑

Combinations:

1) ☐ skip_scraping, ☐ send_url_directly  →  STANDARD SCRAPING
   URL → Article detection → Content extraction → LLM

2) ☑ skip_scraping, ☐ send_url_directly  →  SKIP-SCRAPING MODE
   URL → Download HTML → Text extraction → LLM

3) ☑ send_url_directly (skip_scraping ignored)  →  URL-ONLY MODE
   URL → Send URL string → LLM
```

---

## What Each Mode Does

### 1️⃣ Standard Scraping
- **When:** Both flags OFF (default)
- **What:** Intelligent article/section detection
- **Download:** ✓ Yes (parser)
- **Extraction:** ✓ Smart (per-article)
- **LLM Gets:** Article content
- **Speed:** Medium
- **Quality:** Best
- **Best For:** News sites, article pages

### 2️⃣ Skip-Scraping
- **When:** skip_scraping=True, send_url_directly=False
- **What:** Generic HTML-to-text conversion
- **Download:** ✓ Yes (Selenium)
- **Extraction:** ✓ Full page text (5000 chars max)
- **LLM Gets:** Extracted page text
- **Speed:** Fast
- **Quality:** Good
- **Best For:** Generic web pages, any content

### 3️⃣ URL-Only (NEW)
- **When:** send_url_directly=True
- **What:** No processing, send URL directly
- **Download:** ✗ No
- **Extraction:** ✗ No
- **LLM Gets:** URL string
- **Speed:** Fastest
- **Quality:** Depends on LLM
- **Best For:** Testing, custom models, benchmarking

---

## Change Priority

If BOTH `skip_scraping` and `send_url_directly` are checked:
```
send_url_directly = TRUE
  ↓
✓ Use URL-only mode
✗ Ignore skip_scraping
```

---

## Console Output = Mode Indicator

See this in output? | Mode Active
---|---
`[STEP 1] SCRAPING...` | Standard Scraping ①
`📥 SKIP-MODE: Downloading page content...` | Skip-Scraping ②
`🔗 URL-ONLY MODE: Sending URL directly to LLM` | URL-Only ③

---

## Code Implementation

```python
# In current_affairs.py, line 995:

if skip_scraping:
    # Check priority flag
    send_url_only = source.send_url_directly
    
    if send_url_only:
        # ③ URL-ONLY MODE
        content['body'] = source_url
    else:
        # ② SKIP-SCRAPING MODE
        html = download()
        content['body'] = extract_text(html)
else:
    # ① STANDARD SCRAPING
    content_list = scrape_articles()
```

---

## Database Schema

```
ContentSource table:
├── url (URLField)
├── is_active (Boolean)          ← Enable/disable
├── skip_scraping (Boolean)      ← Mode 2 flag
└── send_url_directly (Boolean)  ← Mode 3 flag (takes priority)
```

---

## Admin Checklist

To set up URL-only mode for a source:

```
☑ is_active           (source is active)
☑ skip_scraping       (doesn't matter, will be ignored)
☑ send_url_directly   (ENABLES URL-ONLY MODE)

Result: URL is sent directly to LLM
```

To use skip-scraping mode:

```
☑ is_active           (source is active)
☑ skip_scraping       (ENABLES SKIP-SCRAPING MODE)
☐ send_url_directly   (NOT checked)

Result: Page downloaded, content extracted, sent to LLM
```

To use standard scraping:

```
☑ is_active           (source is active)
☐ skip_scraping       (NOT checked)
☐ send_url_directly   (NOT checked)

Result: Articles detected, each sent to LLM
```

---

## Migration Status

✅ Applied: `genai.0012_auto_20260127_0500`

Fields added:
- `skip_scraping` on ContentSource
- `send_url_directly` on ContentSource

Both default to `False` (backward compatible)

---

## Key Point: Priority Logic

```python
send_url_directly = True
    ↓
"I don't care about skip_scraping setting,
 send URL directly to LLM"
    ↓
skip_scraping is IGNORED
```

This allows URL-only mode to override skip-scraping behavior.

---

## Files Modified

1. `genai/models.py` - Added 2 fields to ContentSource
2. `genai/tasks/current_affairs.py` - Added URL-only logic
3. `genai/migrations/0012_auto_20260127_0500.py` - Migration

All changes minimal, focused, backward compatible.
