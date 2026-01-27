# use_playwright Parameter - Logging Flow Diagram

## Execution Flow with Logging Points

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ENTRY POINT                                 │
│              fetch_and_process_current_affairs()                    │
│                      (genai/tasks/current_affairs.py:1227)          │
└────────┬────────────────────────────────────────────────────────────┘
         │
         │  🎯 LOGS PARAMETERS:
         │     - content_type
         │     - skip_scraping (type: bool)
         │     - send_url_directly (type: bool)
         │     - use_playwright (type: bool) ⭐ VISIBLE HERE
         │
         ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  CurrentAffairsProcessor()                          │
│                 runs run_complete_pipeline()                        │
│                      (genai/tasks/current_affairs.py:912)           │
└────────┬────────────────────────────────────────────────────────────┘
         │
         │  📥 LOGS PARAMETERS AGAIN:
         │     - content_type
         │     - skip_scraping
         │     - send_url_directly
         │     - use_playwright (TYPE: bool) ⭐ VISIBLE HERE
         │
         ↓
         │
    ┌────▼───────────────────────────────┐
    │  if use_playwright == True?         │
    └────┬─────────────────────────────────┘
         │
    ┌────┴─────────────────────────────────┐
    │                                       │
    │ YES: use_playwright=True              │ NO: use_playwright=False
    │                                       │
    ↓                                       ↓
┌──────────────────────────────────┐  ┌──────────────────────────────┐
│ 🎯 PLAYWRIGHT ROUTE              │  │ 🚀 STANDARD ROUTE            │
│ Logs:                            │  │ Logs:                        │
│ "USE_PLAYWRIGHT=True (True)"     │  │ "Standard pipeline"          │
│ Routes to run_playwright()       │  │ use_playwright=False (False) │
│      (genai/tasks/current_       │  │ Proceeds with scraping       │
│       affairs.py:1087)           │  │ pipeline                     │
└────────┬──────────────────────────┘  └──────────────┬───────────────┘
         │                                           │
         │ 🚀 PLAYWRIGHT PIPELINE                     │ 🚀 STANDARD PIPELINE
         │ START                                     │ START
         │ Logs:                                     │ Logs:
         │ - Content Type                            │ - Mode (URL-Only/
         │ - skip_scraping (False/True)              │   Skip-Scraping/
         │ - send_url_directly (False/True)          │   Standard Scraping)
         │ - Pipeline Mode: PLAYWRIGHT               │ - skip_scraping value
         │   (use_playwright=True) ⭐                │ - send_url_directly
         │                                           │
         ↓                                           ↓
    [PROCESSING]                                 [PROCESSING]
    Uses Playwright for                         Uses Selenium/Requests
    browser automation                          for content fetching
         │                                           │
         └───────────────────┬───────────────────────┘
                             │
                             ↓
                    [RESULTS RETURNED]
```

## Logging Points in Detail

### 1️⃣ ENTRY POINT - fetch_and_process_current_affairs()
**Location**: [genai/tasks/current_affairs.py:1227](genai/tasks/current_affairs.py#L1227)

```
======================================================================
🎯 fetch_and_process_current_affairs() ENTRY POINT
   ✅ Parameters received:
      - content_type: currentaffairs_mcq
      - skip_scraping: False (type: bool)
      - send_url_directly: False (type: bool)
      - use_playwright: True (type: bool)  ⭐ SEE HERE
======================================================================
```

### 2️⃣ PIPELINE METHOD - run_complete_pipeline()
**Location**: [genai/tasks/current_affairs.py:912](genai/tasks/current_affairs.py#L912)

```
======================================================================
📥 [ENTRY] run_complete_pipeline() called with:
   - content_type: currentaffairs_mcq
   - skip_scraping: False
   - send_url_directly: False
   - use_playwright: True (TYPE: bool)  ⭐ SEE HERE
======================================================================
```

### 3️⃣ ROUTING DECISION - if use_playwright:
**Location**: [genai/tasks/current_affairs.py:940](genai/tasks/current_affairs.py#L940)

**If TRUE:**
```
======================================================================
🎯 USE_PLAYWRIGHT=True (True), routing to Playwright pipeline...
======================================================================
```

**If FALSE:**
```
======================================================================
🚀 PIPELINE START - Content Type: currentaffairs_mcq
   use_playwright=False (Standard pipeline)
⚡ MODE: Standard Scraping
======================================================================
```

### 4️⃣ PLAYWRIGHT METHOD - run_playwright()
**Location**: [genai/tasks/current_affairs.py:1097](genai/tasks/current_affairs.py#L1097)

```
======================================================================
🚀 PLAYWRIGHT PIPELINE START - Content Type: currentaffairs_mcq
   Parameters:
   - skip_scraping: False
   - send_url_directly: False
   - Pipeline Mode: PLAYWRIGHT (use_playwright=True)  ⭐ CONFIRMED
======================================================================
```

## How to Check If Parameter is Passing

### Test Case 1: use_playwright=True
Expected output pattern:
- Entry logs show: `use_playwright: True (type: bool)`
- Pipeline logs show: `use_playwright: True (TYPE: bool)`
- Routing shows: `🎯 USE_PLAYWRIGHT=True (True), routing to Playwright pipeline...`
- Final logs show: `Pipeline Mode: PLAYWRIGHT (use_playwright=True)`

### Test Case 2: use_playwright=False
Expected output pattern:
- Entry logs show: `use_playwright: False (type: bool)`
- Pipeline logs show: `use_playwright: False (TYPE: bool)`
- Routing shows: `use_playwright=False (Standard pipeline)`
- Proceeds with standard scraping pipeline

## Common Issues & Solutions

| Issue | Indicator | Solution |
|-------|-----------|----------|
| Parameter not passed from form | Logs show `use_playwright: False` even when checked | Check admin form - verify checkbox is in POST data |
| Parameter passed as string instead of bool | Logs show `(type: str)` instead of `(type: bool)` | Convert string to boolean in view: `bool(request.POST.get('use_playwright'))` |
| Wrong pipeline running | Logs show Standard pipeline but wanted Playwright | Verify value is actual `True`, not string `'True'` |
| No logs appearing at all | No output visible | Check if stdout is being captured; verify print() statements are executing |

## Database Field Status

✅ **ProcessingLog.use_playwright** - Field exists in database
- Migration: `0014_processinglog_use_playwright.py`
- Status: Applied successfully
- Type: `BooleanField(default=False)`

## Log File Locations

- **Console Output**: Appears in your terminal/console where Django runs
- **Django Logs**: Also logged via `logger.info()` to your configured log handlers
- **File Logs**: Check your Django `LOGGING` configuration for file output paths

## Quick Test Command

```python
from genai.tasks.current_affairs import fetch_and_process_current_affairs

# This should show all logging points with use_playwright=True
result = fetch_and_process_current_affairs(
    content_type='currentaffairs_mcq',
    use_playwright=True  # ⭐ Set to True to test
)
```

**Look for**: "🎯 USE_PLAYWRIGHT=True (True)" in the output to confirm routing is working.
