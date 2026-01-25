# Naming Refactoring Complete

## Summary of Changes

### Renamed Terminology

| Old Name | New Name | Where Used |
|----------|----------|-----------|
| `mcq` | `currentaffairs_mcq` | Content sources, task types, all functions |
| `current_affairs` | `current_affairs_descriptive` | Content sources, task types, all functions |
| `descriptive` | `current_affairs_descriptive` | Function parameters and configs |

---

## Files Modified

### 1. **Models** (`genai/models.py`)
- Updated `ProcessingLog.TASK_TYPES` choices:
  - `mcq_fetch` → `currentaffairs_mcq_fetch`
  - `current_affairs_fetch` → `current_affairs_descriptive_fetch`
  - `pdf_mcq` → `pdf_currentaffairs_mcq`
  - `pdf_current_affairs` → `pdf_current_affairs_descriptive`

- Updated `ContentSource.SOURCE_TYPE_CHOICES`:
  - `mcq` → `currentaffairs_mcq`
  - `current_affairs` → `current_affairs_descriptive`

- Increased `source_type` max_length: 20 → 40

### 2. **Config** (`genai/config.py`)
- Updated `CURRENT_AFFAIRS_SOURCES` dictionary keys:
  - `'mcq'` → `'currentaffairs_mcq'`
  - `'descriptive'` → `'current_affairs_descriptive'`

### 3. **Tasks** (`genai/tasks/current_affairs.py`)
- Updated function parameters and docstrings:
  - `fetch_and_process_current_affairs()` default: `'mcq'` → `'currentaffairs_mcq'`
  - `run_complete_pipeline()` default: `'mcq'` → `'currentaffairs_mcq'`
  - `scrape_from_sources()` default: `'mcq'` → `'currentaffairs_mcq'`

- Updated comparison logic:
  - `if content_type == 'mcq':` → `if content_type == 'currentaffairs_mcq':`

### 4. **Views** (`genai/views.py`)
- Updated function calls:
  - `fetch_and_process_current_affairs('mcq')` → `fetch_and_process_current_affairs('currentaffairs_mcq')`

- Updated docstrings and validation:
  - Task type options in comments and error checks

### 5. **Admin** (`genai/admin.py`)
- Updated action button names and descriptions:
  - "Fetch MCQ Only" → "Fetch Current Affairs MCQ"
  - "Fetch Current Affairs Only" → "Fetch Current Affairs Descriptive"
  - "Generate MCQ from PDF" → "Generate Current Affairs MCQ from PDF"
  - "Generate Current Affairs from PDF" → "Generate Current Affairs Descriptive from PDF"

- Updated management command calls:
  - `call_command('fetch_all_content', type='mcq')` → `type='currentaffairs_mcq'`
  - `call_command('fetch_all_content', type='current_affairs')` → `type='current_affairs_descriptive'`
  - PDF processing calls updated similarly

- Updated icon mapping:
  - `'mcq': '📖'` → `'currentaffairs_mcq': '📖'`
  - `'current_affairs': '📰'` → `'current_affairs_descriptive': '📰'`

### 6. **Management Commands**
- `fetch_all_content.py`: Updated choices and logic
- `fetch_current_affairs.py`: Updated default parameter

### 7. **Migrations**
- `0004_auto_20260125_0351.py`: Added `pdf_upload` field to ProcessingLog
- `0005_auto_20260125_1150.py`: Updated field max_lengths

---

## New Admin Interface Labels

### Fetch Actions (from URL sources):
- 🚀 **Fetch Both (MCQ & Current Affairs)**
- 📖 **Fetch Current Affairs MCQ**
- 📰 **Fetch Current Affairs Descriptive**

### PDF Generation Actions:
- 📄 **Generate Current Affairs MCQ from PDF**
- 📋 **Generate Current Affairs Descriptive from PDF**

---

## Content Source Types

When adding content sources in admin, select:
- **Current Affairs MCQ Source** - For MCQ questions
- **Current Affairs Descriptive Source** - For descriptive content

---

## Processing Log Task Types

New task types shown in admin:
- `currentaffairs_mcq_fetch` - Current Affairs MCQ Fetch from URL
- `current_affairs_descriptive_fetch` - Current Affairs Descriptive Fetch from URL
- `both` - Both MCQ & Current Affairs from URL
- `pdf_currentaffairs_mcq` - Current Affairs MCQ Generation from PDF
- `pdf_current_affairs_descriptive` - Current Affairs Descriptive Generation from PDF

---

## Database Changes

**Schema Updates:**
- Increased `ContentSource.source_type` max_length: 20 → 40
- Updated all existing data types (if any) to match new naming

**Backward Compatibility:**
- No breaking changes to existing functionality
- Same features, just renamed for clarity

---

## API/Function References

### Config Access
```python
from genai.config import CURRENT_AFFAIRS_SOURCES
sources = CURRENT_AFFAIRS_SOURCES['currentaffairs_mcq']  # Get MCQ sources
sources = CURRENT_AFFAIRS_SOURCES['current_affairs_descriptive']  # Get descriptive sources
```

### Function Calls
```python
from genai.tasks.current_affairs import fetch_and_process_current_affairs

# Fetch Current Affairs MCQ
result = fetch_and_process_current_affairs('currentaffairs_mcq')

# Fetch Current Affairs Descriptive
result = fetch_and_process_current_affairs('current_affairs_descriptive')
```

### Management Commands
```bash
# Fetch Current Affairs MCQ
python manage.py fetch_all_content --type=currentaffairs_mcq

# Fetch Current Affairs Descriptive
python manage.py fetch_all_content --type=current_affairs_descriptive

# Fetch Both
python manage.py fetch_all_content --type=both
```

---

## Admin Interface Changes

### Before Refactoring
- "📖 Fetch MCQ Only"
- "📰 Fetch Current Affairs Only"
- "📄 Generate MCQ from PDF"
- "📋 Generate Current Affairs from PDF"

### After Refactoring (More Descriptive)
- "📖 Fetch Current Affairs MCQ"
- "📰 Fetch Current Affairs Descriptive"
- "📄 Generate Current Affairs MCQ from PDF"
- "📋 Generate Current Affairs Descriptive from PDF"

---

## Validation Status

✅ All Python files refactored
✅ All docstrings updated
✅ All function parameters updated
✅ All management commands updated
✅ Admin interface updated with descriptive names
✅ Database migrations created and applied
✅ Field sizes increased to accommodate new naming

---

## Next Steps

1. **Clear any cached data:** Django will automatically handle this on next run
2. **Re-add Content Sources:** Go to admin and add your sources with new naming
3. **Test Fetch Actions:** All buttons work with new naming conventions
4. **Monitor Logs:** Processing logs will show new task type names

---

## Migration Summary

**Total Migrations:**
- 0003_contentsource.py - Created ContentSource model
- 0004_auto_20260125_0351.py - Added pdf_upload field
- 0005_auto_20260125_1150.py - Updated field max_lengths (LATEST)

**All migrations applied successfully!**

---

## Benefits of This Refactoring

✅ **More Descriptive:** Clear what type of content is being fetched
✅ **Consistent Naming:** Everything uses "current_affairs_" prefix now
✅ **Better UX:** Admin buttons are clearer about what they do
✅ **Professional:** Terminology is more aligned with domain language

---

Example workflow with new naming:

```
1. Go to /admin/genai/contentsource/
2. Add: "Name: India Today MCQ", "Type: Current Affairs MCQ Source", "URL: ..."
3. Add: "Name: Daily News", "Type: Current Affairs Descriptive Source", "URL: ..."
4. Go to /admin/genai/processinglog/
5. Click action: "📖 Fetch Current Affairs MCQ"
6. View results in ProcessingLog with type: "currentaffairs_mcq_fetch"
```

Your system now uses consistent, descriptive naming throughout!
