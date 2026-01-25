# Admin-Based News Source Management

This guide explains how to manage news sources through the Django admin panel instead of editing Python files.

## Overview

Previously, you had to edit `genai/config.py` to add news sources. Now you can manage them entirely from the Django admin interface:

**Admin URL:** `/admin/bank/newssource/`

## Adding a News Source via Admin Panel

### Step 1: Login to Django Admin
1. Go to: `http://localhost:8000/admin/`
2. Login with your admin credentials

### Step 2: Navigate to News Sources
1. Click on "News Sources" under the "Bank" section
2. Or directly visit: `http://localhost:8000/admin/bank/newssource/`

### Step 3: Add a New Source
1. Click the **"ADD NEWS SOURCE"** button (top right)
2. Fill in the form fields:
   - **Name**: Enter a friendly name (e.g., "GK Today")
   - **URL**: Enter the full URL to scrape (e.g., `https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/`)
   - **Content Type**: Select either:
     - **Current Affairs MCQ** - for MCQ content
     - **Current Affairs Descriptive** - for descriptive content
   - **Is Active**: Check the box to enable scraping (uncheck to disable)
   - **Description** (Optional): Add notes about this source

3. Click **"SAVE"** button

## Example: Adding GK Today

| Field | Value |
|-------|-------|
| Name | GK Today |
| URL | https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/ |
| Content Type | Current Affairs MCQ |
| Is Active | ✓ (checked) |
| Description | Daily current affairs MCQs |

## Managing Existing Sources

### View All Sources
- Go to `/admin/bank/newssource/`
- You'll see a list of all sources with:
  - Name
  - URL (truncated for readability)
  - Content Type (MCQ or Descriptive)
  - Is Active status
  - Created date

### Edit a Source
1. Click on the source name in the list
2. Make your changes
3. Click "SAVE"

### Deactivate a Source
1. Click on the source name
2. Uncheck the **"Is Active"** checkbox
3. Click "SAVE"

The scraper will skip inactive sources.

### Delete a Source
1. Click on the source name
2. Click the **"DELETE"** button at the bottom
3. Confirm deletion

## How It Works

### Scraper Flow

```
1. Scraper starts MCQ generation
2. Calls: get_sources_from_database('mcq')
3. Fetches all active NewsSource objects with content_type='mcq'
4. Scrapes each URL with BeautifulSoup
5. Generates MCQ using LLMPrompt (database-driven)
6. Saves to currentaffairs_mcq model
```

### Fallback Behavior

If the database is unavailable (during initial setup), the system falls back to:
- Hardcoded sources in `genai/config.py` → `CURRENT_AFFAIRS_SOURCES`
- This ensures scraping doesn't fail if database has issues

## Adding Initial Sources

### Option 1: Admin Panel (Recommended)
1. Login to `/admin/`
2. Go to News Sources
3. Add each source manually using the form

### Option 2: Python Script
Run this script to add sources from code:

```bash
cd django/django_project
python manage.py shell < genai/scripts/add_news_sources.py
```

Edit `genai/scripts/add_news_sources.py` to add more sources before running.

## Filtering and Searching

In the News Sources admin list, you can:

### Filter by Content Type
- Click "Current Affairs MCQ" or "Current Affairs Descriptive" in the right sidebar

### Filter by Active Status
- Click "Is Active" in the right sidebar to show only active/inactive sources

### Search by Name or URL
- Use the search box at the top to find sources by name or URL

### Sort by Date Created
- Click the "Created At" column header to sort

## Prompt Management

News sources work with **LLM Prompts** for maximum flexibility:

- Go to `/admin/bank/llmprompt/` to manage prompts
- You can create **source-specific prompts** that target specific URLs
- When scraping from GK Today, it uses the prompt for GK Today's URL
- If no source-specific prompt exists, it uses the default prompt

### Creating a Source-Specific Prompt

1. Go to `/admin/bank/llmprompt/`
2. Click "ADD LLM PROMPT"
3. Fill in:
   - **Source URL**: `https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/`
   - **Prompt Type**: Select "MCQ" or "Descriptive"
   - **Prompt Text**: Your custom prompt (use `{title}` and `{body}` placeholders)
   - **Is Default**: Leave unchecked if source-specific
   - **Is Active**: Check to enable
4. Click "SAVE"

Now when scraping GK Today, it will use your custom prompt!

## Troubleshooting

### Source isn't being scraped

**Possible causes:**
1. **Is Active** checkbox is unchecked
   - Solution: Go to admin, click the source, check "Is Active", save

2. Source URL is incorrect or unreachable
   - Solution: Test the URL in your browser first

3. Database connection issue
   - Solution: Check Django logs for errors

### All sources show "not active"

- Check the admin panel: `/admin/bank/newssource/`
- Make sure at least one source has the "Is Active" checkbox checked

### Getting "permission denied" errors

- Ensure your admin user has permission to edit News Sources
- Ask your Django admin to grant "Change news source" permission

## Best Practices

1. **Use descriptive names**: Instead of "Source 1", use "GK Today"
2. **Test URLs first**: Make sure you can access the URL before adding it
3. **Set appropriate content types**: MCQ vs Descriptive affects the prompt used
4. **Keep URLs current**: If a site changes their article URL structure, update in admin
5. **Create source-specific prompts**: For best results, customize prompts per source
6. **Deactivate instead of delete**: Deactivate sources you might need later instead of deleting

## API Integration

### For Developers

To fetch sources programmatically:

```python
from genai.config import get_sources_from_database

# Get MCQ sources
mcq_sources = get_sources_from_database('mcq')

# Get descriptive sources  
desc_sources = get_sources_from_database('descriptive')
```

### To add a source from code:

```python
from bank.models import NewsSource

NewsSource.objects.create(
    name='Example Site',
    url='https://example.com/article',
    content_type='mcq',
    description='Optional description',
    is_active=True
)
```

## Summary

| Action | Where | How |
|--------|-------|-----|
| Add source | `/admin/bank/newssource/` | Click "Add News Source" |
| Edit source | `/admin/bank/newssource/` | Click on source name |
| Deactivate | `/admin/bank/newssource/` | Uncheck "Is Active" |
| Delete source | `/admin/bank/newssource/` | Click "Delete" button |
| View all | `/admin/bank/newssource/` | See list view |
| Create custom prompt | `/admin/bank/llmprompt/` | Click "Add LLM Prompt" |

---

**Note**: All changes take effect immediately. The scraper will use updated sources on the next run.
