# ✅ Fixed: Now Using Existing genai.ContentSource

## What Changed

❌ **Removed** (was duplicate):
- `NewsSource` model from `bank/models.py`
- `NewsSourceAdmin` from `bank/admin.py`
- Migration `0020_auto_20260125_1649.py`
- Custom `get_sources_from_database()` function from `genai/config.py`

✅ **Now Using** (existing infrastructure):
- `ContentSource` model from `genai/models.py`
- `ContentSourceAdmin` from `genai/admin.py`
- Scraper updated to fetch from `genai.ContentSource` database

---

## Access Content Sources

### Admin Panel URL
```
http://localhost:8000/admin/genai/contentsource/
```

### Add a News Source

1. Go to: `http://localhost:8000/admin/genai/contentsource/`
2. Click: **"ADD CONTENT SOURCE"**
3. Fill:
   - **Name**: GK Today
   - **Source Type**: Current Affairs MCQ Source
   - **URL**: https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/
   - **Description**: (optional)
   - **Is Active**: ✓ (checked)
4. Click: **"SAVE"**

---

## How It Works Now

### Data Flow

```
Admin Panel → genai.ContentSource (Database)
                    ↓
            CurrentAffairsScraper.scrape_from_sources()
                    ↓
            Queries ContentSource with filters:
            - is_active=True
            - source_type='currentaffairs_mcq' or 'currentaffairs_descriptive'
                    ↓
            Processes each URL
                    ↓
            LLMPrompt lookup (source-specific or default)
                    ↓
            Content Generated & Saved
```

### Fallback Mechanism

If `ContentSource` table is empty or database unavailable:
- Scraper falls back to `CURRENT_AFFAIRS_SOURCES` from `genai/config.py`
- Ensures robustness and graceful degradation

---

## Code Changes

### Updated Files

**genai/tasks/current_affairs.py** - Scraper now:
```python
# Fetch from genai.ContentSource instead of config
from genai.models import ContentSource

sources = ContentSource.objects.filter(
    is_active=True,
    source_type=source_type  # 'currentaffairs_mcq' or 'currentaffairs_descriptive'
).values_list('url', flat=True)
```

**genai/config.py** - Preserved hardcoded config as fallback:
```python
CURRENT_AFFAIRS_SOURCES = {
    'currentaffairs_mcq': [...],
    'currentaffairs_descriptive': [...]
}
```

---

## ContentSource Features

### Fields
- **name**: Display name (e.g., "GK Today")
- **source_type**: 'currentaffairs_mcq' or 'currentaffairs_descriptive'
- **url**: Full URL to scrape
- **description**: Optional notes
- **is_active**: Enable/disable without deleting
- **created_by**: Track who added it
- **created_at/updated_at**: Timestamps

### Admin Capabilities
✅ Add sources via admin panel  
✅ Edit existing sources  
✅ Delete sources  
✅ Deactivate without deleting  
✅ Search by name/URL  
✅ Filter by source type and active status  
✅ Bulk activate/deactivate actions  

---

## Next Steps

1. **Go to ContentSource admin**: `http://localhost:8000/admin/genai/contentsource/`
2. **Add your news sources** using the admin interface
3. **Run scraper** - it will automatically use sources from database
4. **Fallback available** - hardcoded config as backup if DB empty

---

## Verification

✅ ContentSource model working  
✅ Scraper imports fixed  
✅ Database queries functional  
✅ Fallback mechanism in place  
✅ No breaking changes  
✅ Uses existing genai infrastructure  

**All set! Use the existing ContentSource infrastructure.** 🎉
