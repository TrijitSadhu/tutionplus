# Skip Scraping Mode - Updated Behavior

## How It Works Now

When you enable **skip_scraping** mode, the system:

1. **Gets URLs** from ContentSource database
2. **Sends URLs directly to LLM** with a prompt
3. **No fetching, no scraping, no HTML extraction**

## Processing Flow

### Standard Mode (skip_scraping=False)
```
ContentSource URL
    ↓
Selenium/requests fetch HTML
    ↓
BeautifulSoup extract text
    ↓
LLM receives: "Here is the extracted content: [text...]"
    ↓
LLM generates MCQs
    ↓
Save to database
```

### Skip-Scraping Mode (skip_scraping=True) - NEW
```
ContentSource URL
    ↓
LLM receives URL directly
    ↓
LLM understands it's a URL and processes it
    ↓
LLM generates MCQs based on URL
    ↓
Save to database
```

## Why This Is Useful

✓ **No web fetching** - Faster, fewer network calls
✓ **No scraping** - Works even if websites block scrapers
✓ **Direct to LLM** - LLM can handle URL understanding
✓ **Simpler** - Skip all intermediate processing steps

## Example Usage

### Step 1: Create ProcessingLog in Admin
1. Go to: `http://localhost:8000/admin/genai/processinglog/`
2. Click "Add Processing Log"
3. **Check "Skip web scraping"** checkbox
4. Fill other fields and save
5. Note the ID (e.g., 42)

### Step 2: Run Command
```bash
python manage.py fetch_all_content --type=currentaffairs_mcq --log-id=42
```

### Step 3: Results
- Pipeline reads URLs from ContentSource
- Sends each URL directly to LLM
- LLM processes the URL and generates MCQs
- Results saved to database

## What Gets Sent to LLM in Skip Mode

In skip-scraping mode, the LLM receives:
```
Content title: [ContentSource title or "Direct-to-LLM: [URL]"]
Content body: [The URL itself]
```

The LLM prompt instructs it to:
- Understand this is a URL
- Generate MCQs from the content at that URL
- Return properly formatted MCQs

## Key Differences

| Aspect | Standard Mode | Skip-Scraping Mode |
|--------|---------------|-------------------|
| Fetches Content | ✅ Yes | ❌ No |
| Scrapes HTML | ✅ Yes | ❌ No |
| Extracts Text | ✅ Yes | ❌ No |
| Network Calls | Multiple | Minimal |
| Speed | Slower | Faster |
| Success Rate | Depends on HTML | Depends on LLM URL understanding |

## Configuration

**Field**: `ProcessingLog.skip_scraping`
**Type**: BooleanField
**Default**: False
**Location**: Admin interface under "Processing Options"

## Implementation Details

**Files Updated:**
- `genai/models.py` - Added skip_scraping field
- `genai/admin.py` - Updated ProcessingLogAdmin
- `genai/tasks/current_affairs.py` - Updated pipeline logic
- `genai/management/commands/fetch_all_content.py` - Reads flag and passes to pipeline

**Method Signature:**
```python
def run_complete_pipeline(
    self, 
    content_type: str = 'mcq', 
    skip_scraping: bool = False
):
```

**Result Tracking:**
- Results include `'mode'` key:
  - `'direct-to-llm'` when skip_scraping=True
  - `'standard'` when skip_scraping=False

## Flow Diagram

```
ProcessingLog.skip_scraping = True
                ↓
fetch_all_content command reads flag
                ↓
Passes skip_scraping=True to processor
                ↓
run_complete_pipeline() checks flag
                ↓
skip_scraping=True branch:
  - Get URLs from ContentSource
  - For each URL:
    - Send URL directly to LLM
    - LLM generates MCQs
    - Save results
                ↓
Results include mode='direct-to-llm'
```

## Notes

- URLs are sent as plain text to the LLM
- LLM is responsible for understanding they are URLs
- Faster than scraping but relies on LLM capabilities
- Works best with URLs that have clear, readable content
- No fallback to scraping if this mode fails

## Future Enhancements

1. Add error handling if LLM doesn't recognize URL
2. Add prompt customization for URL processing
3. Add metrics comparing both modes
4. Add automatic mode selection based on URL type
