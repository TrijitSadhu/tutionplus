# use_playwright Parameter Debug & Logging Enhancement

## Problem Identified
When `use_playwright=True` was selected, the value wasn't being clearly shown/logged in the method execution, making it hard to verify if the parameter was actually being passed through the call chain.

## Solution Implemented

### 1. Enhanced Parameter Logging in Entry Point
**File:** [genai/tasks/current_affairs.py](genai/tasks/current_affairs.py#L1227)

Added comprehensive logging at the entry point function `fetch_and_process_current_affairs()`:
```python
print("="*70)
print(f"🎯 fetch_and_process_current_affairs() ENTRY POINT")
print(f"   ✅ Parameters received:")
print(f"      - content_type: {content_type}")
print(f"      - skip_scraping: {skip_scraping} (type: {type(skip_scraping).__name__})")
print(f"      - send_url_directly: {send_url_directly} (type: {type(send_url_directly).__name__})")
print(f"      - use_playwright: {use_playwright} (type: {type(use_playwright).__name__})")
```

This ensures all parameters are logged with their types when the function is called.

### 2. Enhanced Parameter Logging in Pipeline Method
**File:** [genai/tasks/current_affairs.py](genai/tasks/current_affairs.py#L912)

Added detailed logging at the start of `run_complete_pipeline()`:
```python
print(f"\n{'='*70}")
print(f"📥 [ENTRY] run_complete_pipeline() called with:")
print(f"   - content_type: {content_type}")
print(f"   - skip_scraping: {skip_scraping}")
print(f"   - send_url_directly: {send_url_directly}")
print(f"   - use_playwright: {use_playwright} (TYPE: {type(use_playwright).__name__})")
print(f"{'='*70}")
logger.info(f"run_complete_pipeline() called with: content_type={content_type}, skip_scraping={skip_scraping}, send_url_directly={send_url_directly}, use_playwright={use_playwright}")
```

### 3. Clear Route Logging for Playwright Mode
**File:** [genai/tasks/current_affairs.py](genai/tasks/current_affairs.py#L940)

When `use_playwright=True`, added explicit logging:
```python
if use_playwright:
    print(f"\n{'='*70}")
    print(f"🎯 USE_PLAYWRIGHT=True ({use_playwright}), routing to Playwright pipeline...")
    print(f"{'='*70}")
    logger.info(f"Routing to Playwright pipeline (use_playwright={use_playwright})")
    return self.run_playwright(content_type, skip_scraping, send_url_directly)
else:
    print(f"\n{'='*70}")
    print(f"🚀 PIPELINE START - Content Type: {content_type}")
    print(f"   use_playwright={use_playwright} (Standard pipeline)")
```

### 4. Enhanced Playwright Method Logging
**File:** [genai/tasks/current_affairs.py](genai/tasks/current_affairs.py#L1097)

Updated `run_playwright()` method logging:
```python
print(f"\n{'='*70}")
print(f"🚀 PLAYWRIGHT PIPELINE START - Content Type: {content_type}")
print(f"   Parameters:")
print(f"   - skip_scraping: {skip_scraping}")
print(f"   - send_url_directly: {send_url_directly}")
print(f"   - Pipeline Mode: PLAYWRIGHT (use_playwright=True)")
print(f"{'='*70}")
logger.info(f"Playwright pipeline started: content_type={content_type}, skip_scraping={skip_scraping}, send_url_directly={send_url_directly}")
```

## Expected Output When use_playwright=True

When you run the function with `use_playwright=True`, you should now see:

```
======================================================================
🎯 fetch_and_process_current_affairs() ENTRY POINT
   ✅ Parameters received:
      - content_type: currentaffairs_mcq
      - skip_scraping: False (type: bool)
      - send_url_directly: False (type: bool)
      - use_playwright: True (type: bool)
======================================================================

======================================================================
📥 [ENTRY] run_complete_pipeline() called with:
   - content_type: currentaffairs_mcq
   - skip_scraping: False
   - send_url_directly: False
   - use_playwright: True (TYPE: bool)
======================================================================

======================================================================
🎯 USE_PLAYWRIGHT=True (True), routing to Playwright pipeline...
======================================================================

======================================================================
🚀 PLAYWRIGHT PIPELINE START - Content Type: currentaffairs_mcq
   Parameters:
   - skip_scraping: False
   - send_url_directly: False
   - Pipeline Mode: PLAYWRIGHT (use_playwright=True)
======================================================================
```

## Debugging Checklist

✅ **Parameter Type Checking**: All parameters now show their Python type (bool, str, etc.)
✅ **Value Visibility**: Whether `use_playwright` is `True` or `False`, it's now explicitly shown
✅ **Routing Confirmation**: Clear indication of which pipeline (Standard vs Playwright) is being executed
✅ **Logger Integration**: All major decision points logged to Python logger for file-based debugging
✅ **Call Chain Tracking**: Complete visibility from entry point through pipeline method

## If use_playwright is Still Not Working

1. **Check the Admin Form**: Verify that the checkbox is actually being submitted with the form
2. **Check Your View/API**: Ensure the parameter is being passed from the request to `fetch_and_process_current_affairs()`
3. **Example Call**:
   ```python
   from genai.tasks.current_affairs import fetch_and_process_current_affairs
   
   result = fetch_and_process_current_affairs(
       content_type='currentaffairs_mcq',
       skip_scraping=False,
       send_url_directly=False,
       use_playwright=True  # This must be explicitly True
   )
   ```

4. **Check ProcessingLog Model**: Verify that your ProcessingLog model has the `use_playwright` field (migration 0014 was applied)

## Related Database Changes

- **Migration**: `0014_processinglog_use_playwright.py` - Added the `use_playwright` BooleanField to ProcessingLog model
- The migration has been applied: `Applying genai.0014_processinglog_use_playwright... OK`

## Summary

The enhanced logging now provides **complete visibility** into:
- Whether parameters are being passed correctly
- Whether the parameter type is correct (bool vs string)
- Which pipeline is being executed
- Clear routing decisions at each step

This makes debugging parameter passing issues much easier.
