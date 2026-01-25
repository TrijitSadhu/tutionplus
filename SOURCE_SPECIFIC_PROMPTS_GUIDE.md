# Using Different Prompts for Different URL Sources

## YES - It Works! ✅

The system **fully supports different prompts for different URL sources**. Here's how:

## How It Works

### 1. **Source Detection**
When the scraper fetches articles from a URL, it now **automatically tracks the source URL**:
```
Website: https://timesofindia.indiatimes.com/news
         └─> Article is tagged with this source URL
```

### 2. **Prompt Lookup Order**
When processing an article, the system:
1. Checks if a **source-specific prompt** exists for that URL
2. If not found, uses the **default prompt**
3. Falls back to **hardcoded prompt** if database is empty

### 3. **Example Flow**
```
Article from Times of India
  ↓
Check: Is there a prompt for "https://timesofindia.indiatimes.com/news"?
  ↓
YES → Use Times of India MCQ prompt
  ↓
NO → Use default MCQ prompt
  ↓
If neither exists → Use hardcoded fallback
```

## Practical Examples

### Example 1: Different Prompts for Different News Sources

**Scenario:** You have 3 news sources with different styles:
- Times of India (Indian politics focused)
- BBC (International affairs focused)
- Financial Times (Finance focused)

**Solution:** Create 3 different MCQ prompts

```
Times of India MCQ Prompt:
  Source URL: https://timesofindia.indiatimes.com/news
  Type: MCQ
  Content: "Focus on Indian politics and current affairs..."
  
BBC MCQ Prompt:
  Source URL: https://www.bbc.com/news
  Type: MCQ
  Content: "Focus on international relations..."
  
Financial Times MCQ Prompt:
  Source URL: https://www.ft.com
  Type: MCQ
  Content: "Focus on economics and finance..."
```

### Example 2: Mix Global Default with Source-Specific

**Scenario:** You have a global MCQ prompt but want special prompts for finance news

**Setup:**
```
Global MCQ Prompt (Default):
  Source URL: (leave empty)
  Type: MCQ
  Is Default: YES
  Content: "Generic MCQ prompt..."

Finance News MCQ Prompt (Specific):
  Source URL: https://economictimes.com/news
  Type: MCQ
  Is Default: NO
  Content: "Focus on economic terms, stock market..."
```

**Result:**
- Articles from Economic Times → Uses finance-specific prompt
- Articles from other sources → Uses global default prompt

## How to Set Up Source-Specific Prompts

### Method 1: Via Admin Panel

1. Go to: `http://127.0.0.1:8000/admin/bank/llmprompt/`
2. Click **"Add LLM Prompt"**
3. Fill in:
   - **Source URL**: `https://timesofindia.indiatimes.com/news`
   - **Prompt Type**: `MCQ`
   - **Prompt Text**: Your custom prompt
   - **Is Default**: Unchecked (since it's source-specific)
   - **Is Active**: Checked
4. Click **Save**

### Method 2: Programmatically

Use the provided script to create multiple prompts at once:

```bash
python create_source_specific_prompts.py
```

This creates:
- Times of India MCQ prompt
- NDTV Descriptive prompt
- BBC MCQ prompt

### Method 3: Django Shell

```python
python manage.py shell

from bank.models import LLMPrompt

LLMPrompt.objects.create(
    source_url='https://mysite.com/news',
    prompt_type='mcq',
    prompt_text='Your custom prompt with {title} and {content}',
    is_default=False,
    is_active=True
)
```

## Important Notes

### 1. **Source URL Matching**
- The scraper extracts source URLs from the sources being scraped
- It matches based on **exact URL or URL prefix matching**
- Example:
  ```
  Scraping from: https://timesofindia.indiatimes.com/news
  Prompt stored for: https://timesofindia.indiatimes.com/news
  ✅ Will match and use this prompt
  
  But if you scrape from:
  https://timesofindia.indiatimes.com/news/india
  ✅ Still matches (same base URL)
  ```

### 2. **Default Prompts**
- Always keep at least one default for each prompt type (MCQ and Descriptive)
- Default prompts are used when no source-specific match is found
- Only ONE default per prompt type can be active

### 3. **Empty Source URL**
- Leave source_url empty for **global/default prompts**
- These become the fallback for any source without specific prompt

### 4. **Active/Inactive Toggle**
- Mark prompts as Inactive to disable without deleting
- Useful for testing before full rollout
- Deactivated prompts won't be used but remain in database for history

## Current Setup (As of Now)

You have 5 prompts configured:

```
[DEFAULT] Global MCQ Prompt
[DEFAULT] Global Descriptive Prompt
         Times of India MCQ Prompt
         NDTV Descriptive Prompt
         BBC MCQ Prompt
```

### How They're Used:

| Source | Content Type | Prompt Used |
|--------|--------------|-------------|
| Times of India | MCQ | Times of India specific |
| Times of India | Descriptive | Default descriptive |
| NDTV | MCQ | Default MCQ |
| NDTV | Descriptive | NDTV specific |
| BBC | MCQ | BBC specific |
| BBC | Descriptive | Default descriptive |
| Any other | MCQ | Default MCQ |
| Any other | Descriptive | Default descriptive |

## Advanced Use Cases

### 1. **Regional Prompts**
```
Create different prompts for:
- Indian news (Times of India, NDTV)
- International news (BBC, Reuters)
- Finance news (Financial Times, Bloomberg)
- Tech news (TechCrunch, Wired)
```

### 2. **Exam-Specific Prompts**
```
Create different prompts for:
- Banking exams (IBPS, SBI)
- General knowledge exams
- Current affairs exams
- Finance exams
```

### 3. **Quality Control**
```
- Use strict prompts for important sources
- Use lenient prompts for casual content
- A/B test different prompt styles
- Track which prompts produce best results
```

## Troubleshooting

### Q: Why isn't my source-specific prompt being used?

**Checklist:**
1. ✅ Is the prompt marked as **Active**?
2. ✅ Does the source URL **exactly match**?
3. ✅ Is the prompt **type correct** (MCQ vs Descriptive)?
4. ✅ Are you **actually scraping from that source**?

### Q: How do I test source-specific prompts?

**Option 1: Manual Testing**
```python
from genai.tasks.current_affairs import CurrentAffairsProcessor

processor = CurrentAffairsProcessor()

# Test source-specific lookup
prompt = processor.get_prompt_from_database(
    prompt_type='mcq',
    source_url='https://timesofindia.indiatimes.com/news'
)
print(prompt)  # Should show Times of India prompt
```

**Option 2: Check Admin Panel**
- Go to `/admin/bank/llmprompt/`
- Verify all prompts are there
- Check source URLs and types

### Q: Can I have multiple prompts for the same source?

**No, only one per (source_url, prompt_type) combination.**

But you can have:
- One MCQ prompt for Times of India
- One Descriptive prompt for Times of India
- Both would be active simultaneously

## Summary

✅ **YES - Different prompts for different URL sources works!**

The system:
1. ✅ Tracks source URLs during scraping
2. ✅ Looks up source-specific prompts first
3. ✅ Falls back to defaults if not found
4. ✅ Can be managed entirely from admin panel
5. ✅ Supports unlimited source-specific prompts

You're all set to create custom prompts for different sources!
