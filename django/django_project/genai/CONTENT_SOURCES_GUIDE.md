# Content Sources Management Guide

## Overview

The system now allows you to manage and configure content sources (URLs) directly from the Django admin panel. No code changes required!

## What Changed?

Instead of hardcoding URLs in `config.py`, you can now:
- Add multiple MCQ sources
- Add multiple Current Affairs sources
- Enable/disable sources without restarting
- Manage everything from Django admin

## How to Add Content Sources

### Step 1: Go to Admin Panel
```
http://localhost:8000/admin/genai/contentsource/
```

### Step 2: Click "Add Content Source"
You'll see a form with these fields:

| Field | Description | Example |
|-------|-------------|---------|
| **Name** | Display name for the source | "MCQ Bank - India Today" |
| **Source Type** | Choose: MCQ Source or Current Affairs | MCQ Source |
| **URL** | Full URL to fetch content from | https://example.com/api/mcq |
| **Description** | Optional notes about the source | "Daily updated MCQs" |
| **Active** | Enable/disable this source | ✓ Checked |

### Step 3: Save and Use

Once saved, the system will automatically use these sources when you trigger a fetch from the admin panel.

---

## Example Workflow

### Adding MCQ Source
1. Go to: `http://localhost:8000/admin/genai/contentsource/`
2. Click "Add Content Source"
3. Fill in:
   - **Name:** `Daily MCQ Updates`
   - **Source Type:** `MCQ Source`
   - **URL:** `https://your-mcq-provider.com/api/questions`
   - **Description:** `Updated daily with new questions`
   - **Active:** ✓ Checked
4. Click "Save"

### Adding Current Affairs Source
1. Go to: `http://localhost:8000/admin/genai/contentsource/`
2. Click "Add Content Source"
3. Fill in:
   - **Name:** `Current Affairs Daily`
   - **Source Type:** `Current Affairs Source`
   - **URL:** `https://news-api.example.com/current-affairs`
   - **Description:** `Daily updated current affairs`
   - **Active:** ✓ Checked
4. Click "Save"

### Then Trigger Fetch
1. Go to: `http://localhost:8000/admin/genai/processinglog/`
2. Click any checkbox
3. Select "🚀 Fetch Both (MCQ & Current Affairs)"
4. Click "Go"
5. The system will fetch from ALL active sources you added!

---

## Managing Sources

### View All Sources
```
http://localhost:8000/admin/genai/contentsource/
```

### Disable a Source (without deleting)
1. Click on the source name
2. Uncheck "Active"
3. Click "Save"

The source won't be used in fetches until you re-enable it.

### Delete a Source
1. Click on the source name
2. Click "Delete" button
3. Confirm deletion

### Bulk Actions
From the sources list, you can:
- ✅ Activate selected sources
- ❌ Deactivate selected sources

---

## How Fetching Works Now

### Old Way (Hardcoded)
```python
# config.py - Had to edit code
CURRENT_AFFAIRS_SOURCES = {
    'mcq': ['https://url1.com', 'https://url2.com'],
    'current_affairs': ['https://url3.com']
}
```

### New Way (Database)
```
Admin Panel → Content Sources → Add/Edit/Delete URLs
↓
System reads from database automatically
↓
Fetch process uses active sources
```

---

## Management Command Integration

When you trigger a fetch from admin, the system:

1. **Reads** all active sources from database
2. **Fetches** from each URL
3. **Processes** the content
4. **Saves** to database
5. **Logs** everything in ProcessingLog

### Command Line (Optional)
You can still use the command manually:
```bash
python manage.py fetch_all_content --type=both
```

It will automatically use sources from database.

---

## Best Practices

✅ **DO:**
- Add at least one source before triggering fetch
- Keep sources active/inactive based on needs
- Test new sources before relying on them
- Add descriptive names for easy identification
- Monitor logs after fetching

❌ **DON'T:**
- Leave invalid URLs (they'll cause errors)
- Add too many sources (can slow down fetching)
- Delete sources you might need later (deactivate instead)
- Share sensitive API URLs in description

---

## Troubleshooting

### Issue: No sources appearing in fetch
**Solution:** 
- Go to admin → Content Sources
- Verify you have active sources added
- Check "Active" checkbox is enabled

### Issue: Fetch fails with error
**Solution:**
- Go to admin → Processing Log
- Check the error message
- Verify the URL is correct and accessible
- Test URL in browser first

### Issue: Want to use old config.py URLs
**Solution:**
- Deactivate all sources in admin
- Add your URLs from config.py as new sources
- Sources in admin take priority over config.py

---

## Quick Start Example

**Add these sources to get started:**

### MCQ Source
- Name: `Sample MCQ`
- Type: `MCQ Source`
- URL: `https://api.example.com/mcq`
- Active: ✓

### Current Affairs Source
- Name: `Sample Current Affairs`
- Type: `Current Affairs Source`
- URL: `https://api.example.com/news`
- Active: ✓

Then go to `/admin/genai/processinglog/` and click the fetch buttons!

---

## Admin Interface Features

### Source List View Shows:
- 📖 MCQ Source / 📰 Current Affairs Source (with icons)
- Source name
- URL (clickable, opens in new tab)
- Status (✅ Active or ❌ Inactive)
- Created date

### Sorting & Filtering:
- Filter by source type
- Filter by active status
- Filter by date
- Search by name, URL, or description

### Bulk Operations:
- Select multiple sources
- Activate/deactivate in bulk
- Delete multiple sources at once

---

## API Integration

If your sources are API endpoints, make sure they:
- Return valid JSON
- Have proper CORS headers (if accessed from browser)
- Handle rate limiting appropriately
- Return data in expected format

Example API response format:
```json
{
  "questions": [
    {
      "title": "Question text",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }
  ]
}
```

---

## Next Steps

1. **Go to Admin:** http://localhost:8000/admin/genai/contentsource/
2. **Add Sources:** Click "Add Content Source" and fill in your URLs
3. **Activate Them:** Make sure "Active" is checked
4. **Trigger Fetch:** Go to `/admin/genai/processinglog/` and click fetch buttons
5. **Monitor Progress:** Watch the status updates in real-time

That's it! Your system is now using sources from the admin panel.
