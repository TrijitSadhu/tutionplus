# use_playwright Parameter - Complete Troubleshooting Checklist

## ✅ What Was Fixed

### 1. Database Migration
- ✅ Created migration: `0014_processinglog_use_playwright.py`
- ✅ Applied migration: Field added to `genai_processinglog` table
- ✅ ProcessingLog model now has the `use_playwright` field

### 2. Enhanced Logging Throughout Pipeline
- ✅ Entry point logging: `fetch_and_process_current_affairs()`
- ✅ Pipeline logging: `run_complete_pipeline()`
- ✅ Routing decision logging: Clear indication of which pipeline is chosen
- ✅ Playwright method logging: `run_playwright()`
- ✅ Logger integration: All steps logged to Python logger

### 3. Parameter Type Verification
- ✅ Parameter types are now shown (bool, str, etc.)
- ✅ Value is shown both when True and False
- ✅ Clear distinction between different pipeline modes

## 🔍 How to Verify the Fix is Working

### Option A: Check Logs in Console/Terminal
When you run your process with `use_playwright=True`, look for:

```
🎯 fetch_and_process_current_affairs() ENTRY POINT
   ✅ Parameters received:
      - use_playwright: True (type: bool)  ⭐ SHOULD SEE THIS

📥 [ENTRY] run_complete_pipeline() called with:
   - use_playwright: True (TYPE: bool)  ⭐ SHOULD SEE THIS

🎯 USE_PLAYWRIGHT=True (True), routing to Playwright pipeline...  ⭐ SHOULD SEE THIS

🚀 PLAYWRIGHT PIPELINE START - Content Type: currentaffairs_mcq
   - Pipeline Mode: PLAYWRIGHT (use_playwright=True)  ⭐ SHOULD SEE THIS
```

### Option B: Check Database
```python
# In Django shell
python manage.py shell

from genai.models import ProcessingLog

# Check if the field exists
print(ProcessingLog._meta.get_fields())

# Check if you can create a log with use_playwright
log = ProcessingLog.objects.create(
    task_type='currentaffairs_mcq_fetch',
    status='pending',
    use_playwright=True
)
print(f"✅ Created ProcessingLog with use_playwright={log.use_playwright}")
```

### Option C: Check Django Admin
1. Go to: `/admin/genai/processinglog/`
2. Click "+ Add Processing Log"
3. You should now see a checkbox for "use_playwright" (no more database error!)
4. Set it to True/False and save

## 📋 Pre-Implementation Checklist (Before Calling Function)

### From Admin/Form:
- [ ] Verify that the checkbox for `use_playwright` is on the admin form
- [ ] Verify that when checked, the value gets posted to your view
- [ ] Verify that your view extracts the checkbox value correctly

### From Direct Function Call:
```python
# ✅ CORRECT:
result = fetch_and_process_current_affairs(
    content_type='currentaffairs_mcq',
    use_playwright=True  # Boolean type
)

# ❌ WRONG:
result = fetch_and_process_current_affairs(
    content_type='currentaffairs_mcq',
    use_playwright='True'  # String instead of boolean
)

# ❌ WRONG:
result = fetch_and_process_current_affairs(
    content_type='currentaffairs_mcq',
    use_playwright=1  # Integer instead of boolean
)
```

## 🐛 If Still Not Working - Debugging Steps

### Step 1: Verify Parameter is Boolean Type
Add this test to your view/function:
```python
from genai.tasks.current_affairs import fetch_and_process_current_affairs

# Debug: Print parameter info before calling
use_playwright = request.POST.get('use_playwright', False)
print(f"DEBUG: use_playwright = {use_playwright}")
print(f"DEBUG: type = {type(use_playwright).__name__}")
print(f"DEBUG: bool value = {bool(use_playwright)}")

# Convert string to boolean if needed
if isinstance(use_playwright, str):
    use_playwright = use_playwright.lower() in ['true', '1', 'on']

result = fetch_and_process_current_affairs(
    content_type='currentaffairs_mcq',
    use_playwright=use_playwright
)
```

### Step 2: Check If Logs Are Being Output
Look for any of these patterns in your console/log file:
- Search for: "🎯 fetch_and_process_current_affairs"
- Search for: "📥 [ENTRY] run_complete_pipeline"
- Search for: "USE_PLAYWRIGHT"
- Search for: "PLAYWRIGHT PIPELINE"

If you don't see these, the function might not be getting called at all.

### Step 3: Verify Admin Form Field Exists
In your admin.py:
```python
class ProcessingLogAdmin(admin.ModelAdmin):
    list_display = ['task_type', 'status', 'use_playwright']  # Add this
    
    # Make sure the field is not read_only or excluded
    fields = [
        'task_type', 'status', 'use_playwright',  # ✅ INCLUDE IT
        'skip_scraping', 'send_url_directly',
        # ... other fields
    ]
```

### Step 4: Capture Full Output
Enable verbose logging to see everything:
```python
# In Django settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'current_affairs_debug.log',
        },
    },
    'loggers': {
        'genai.tasks.current_affairs': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
```

## 📊 Expected Behavior Differences

### When use_playwright=False (Standard Pipeline)
```
Pipeline uses: Selenium/Requests to download content
Time: Faster (already downloaded before LLM)
Content: Extracted/truncated by scraper
LLM Input: Processed content (up to 5000 chars)
```

### When use_playwright=True (Playwright Pipeline)
```
Pipeline uses: Playwright for browser automation
Time: Slower (full page load in headless browser)
Content: Extracted from full page load
LLM Input: Full page content (no limit)
Best For: JavaScript-heavy websites
```

## ✨ Files Modified

1. **[genai/migrations/0014_processinglog_use_playwright.py](genai/migrations/0014_processinglog_use_playwright.py)** - NEW
   - Creates the database column

2. **[genai/tasks/current_affairs.py](genai/tasks/current_affairs.py)** - MODIFIED
   - Enhanced logging in `fetch_and_process_current_affairs()`
   - Enhanced logging in `run_complete_pipeline()`
   - Enhanced logging in `run_playwright()`

3. **[USE_PLAYWRIGHT_DEBUG_SUMMARY.md](USE_PLAYWRIGHT_DEBUG_SUMMARY.md)** - NEW
   - Comprehensive documentation

4. **[USE_PLAYWRIGHT_LOGGING_FLOW.md](USE_PLAYWRIGHT_LOGGING_FLOW.md)** - NEW
   - Visual flow diagram and logging points

## 🎯 Quick Reference

| Component | Location | Change | Status |
|-----------|----------|--------|--------|
| Database Field | ProcessingLog model | Added via migration 0014 | ✅ Applied |
| Entry Point Logging | fetch_and_process_current_affairs() | Enhanced parameter logging | ✅ Complete |
| Pipeline Logging | run_complete_pipeline() | Added full parameter audit | ✅ Complete |
| Routing Logging | if use_playwright check | Clear route indication | ✅ Complete |
| Playwright Logging | run_playwright() | Confirmed mode in output | ✅ Complete |

## 🚀 Ready to Test?

1. ✅ Migration applied? Run: `python manage.py migrate`
2. ✅ Code changes in place? File is: [genai/tasks/current_affairs.py](genai/tasks/current_affairs.py)
3. ✅ Admin page accessible? Visit: `/admin/genai/processinglog/add/`
4. ✅ Set use_playwright=True and observe logs in console

**Success Indicator**: When you see "🎯 USE_PLAYWRIGHT=True (True), routing to Playwright pipeline..." in your logs, the parameter is passing correctly!
