# use_playwright Parameter - Missing Argument Fix

## Root Cause Identified

The `use_playwright` parameter from the ProcessingLog was **NOT being passed** to the `fetch_and_process_current_affairs()` function in the management command.

### Issue Flow:
```
1. Admin Form (ProcessingLog)
   └─ Selected: use_playwright=True ✅

2. Admin Action: trigger_fetch_mcq() 
   └─ Calls management command with log_id ✅

3. Management Command: fetch_all_content.py
   └─ Retrieved log_entry.use_playwright from database ✅
   └─ BUT NOT PASSED to function call ❌

4. fetch_and_process_current_affairs()
   └─ Received: use_playwright=False (default) ❌
```

## Solution Applied

### File: [genai/management/commands/fetch_all_content.py](genai/management/commands/fetch_all_content.py)

#### Change 1: MCQ Fetch Call (Line 93-98)
**Before:**
```python
print(f"  📞 Calling fetch_and_process_current_affairs('currentaffairs_mcq', skip_scraping={log_entry.skip_scraping}, send_url_directly={log_entry.send_url_directly})...")
try:
    mcq_result = fetch_and_process_current_affairs(
        'currentaffairs_mcq',
        skip_scraping=log_entry.skip_scraping,
        send_url_directly=log_entry.send_url_directly
    )
```

**After:**
```python
print(f"  📞 Calling fetch_and_process_current_affairs('currentaffairs_mcq', skip_scraping={log_entry.skip_scraping}, send_url_directly={log_entry.send_url_directly}, use_playwright={log_entry.use_playwright})...")
try:
    mcq_result = fetch_and_process_current_affairs(
        'currentaffairs_mcq',
        skip_scraping=log_entry.skip_scraping,
        send_url_directly=log_entry.send_url_directly,
        use_playwright=log_entry.use_playwright  # ✅ ADDED
    )
```

#### Change 2: Descriptive Content Fetch Call (Line 128-133)
**Before:**
```python
print(f"  📞 Calling fetch_and_process_current_affairs('currentaffairs_descriptive', skip_scraping={log_entry.skip_scraping}, send_url_directly={log_entry.send_url_directly})...")
try:
    ca_result = fetch_and_process_current_affairs(
        'currentaffairs_descriptive',
        skip_scraping=log_entry.skip_scraping,
        send_url_directly=log_entry.send_url_directly
    )
```

**After:**
```python
print(f"  📞 Calling fetch_and_process_current_affairs('currentaffairs_descriptive', skip_scraping={log_entry.skip_scraping}, send_url_directly={log_entry.send_url_directly}, use_playwright={log_entry.use_playwright})...")
try:
    ca_result = fetch_and_process_current_affairs(
        'currentaffairs_descriptive',
        skip_scraping=log_entry.skip_scraping,
        send_url_directly=log_entry.send_url_directly,
        use_playwright=log_entry.use_playwright  # ✅ ADDED
    )
```

## Expected Behavior After Fix

### When You Select use_playwright=True in Admin:

1. **Admin Form** → Click checkbox for `use_playwright` → Click "trigger_fetch_mcq"
2. **Admin Action** → Saves `use_playwright=True` to ProcessingLog
3. **Management Command** → Retrieves `log_entry.use_playwright=True` from database
4. **Function Call** → Now passes `use_playwright=True` to `fetch_and_process_current_affairs()`
5. **Pipeline** → Routes to Playwright pipeline instead of Standard pipeline

### Expected Log Output:

```
🎯 fetch_and_process_current_affairs() ENTRY POINT
   ✅ Parameters received:
      - content_type: currentaffairs_mcq
      - skip_scraping: False (type: bool)
      - send_url_directly: False (type: bool)
      - use_playwright: True (type: bool)  ✅ NOW SHOWS TRUE!

📥 [ENTRY] run_complete_pipeline() called with:
   - use_playwright: True (TYPE: bool)  ✅ NOW SHOWS TRUE!

🎯 USE_PLAYWRIGHT=True (True), routing to Playwright pipeline...  ✅ ROUTING CORRECT!

🚀 PLAYWRIGHT PIPELINE START - Content Type: currentaffairs_mcq
   - Pipeline Mode: PLAYWRIGHT (use_playwright=True)  ✅ CONFIRMED!
```

## Testing Steps

### Step 1: Create a ProcessingLog Entry
1. Go to: `/admin/genai/processinglog/`
2. Click "+ Add Processing Log"
3. Fill in:
   - Task Type: "Current Affairs MCQ Fetch from URL"
   - Status: "Pending"
   - **Check the checkbox for "use_playwright"** ✅
4. Click Save

### Step 2: Trigger the Action
1. Go back to ProcessingLog list
2. Select your newly created entry
3. Choose action: "📖 Fetch Current Affairs MCQ"
4. Click "Go"

### Step 3: Verify in Logs
Look for these messages in your console:
- ✅ `use_playwright: True (type: bool)` in entry point logs
- ✅ `USE_PLAYWRIGHT=True (True), routing to Playwright pipeline...` in routing logs
- ✅ `Pipeline Mode: PLAYWRIGHT (use_playwright=True)` in Playwright method logs

## Files Modified

| File | Changes | Status |
|------|---------|--------|
| [genai/management/commands/fetch_all_content.py](genai/management/commands/fetch_all_content.py) | Added `use_playwright` parameter to both MCQ and Descriptive fetch calls | ✅ Complete |
| [genai/tasks/current_affairs.py](genai/tasks/current_affairs.py) | Already had enhanced logging (from previous fix) | ✅ Complete |

## Summary

The issue was a simple **missing parameter** in the management command. The ProcessingLog database had the `use_playwright` field and the value was being saved correctly, but it wasn't being passed to the task function.

**Now fixed:** The management command retrieves `log_entry.use_playwright` and passes it to `fetch_and_process_current_affairs()` in both MCQ and Descriptive content fetch calls.

When you select `use_playwright=True` in the admin form and click "trigger_fetch_mcq", the Playwright pipeline should now be executed correctly! 🎯
