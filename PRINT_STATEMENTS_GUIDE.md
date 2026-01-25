# Print Statements Debug Guide

## Overview
Comprehensive print statements have been added throughout the genai/tasks/current_affairs.py workflow to trace execution flow and debug the LLM prompt management system.

---

## Execution Flow with Print Statements

### 1. PIPELINE START
```
🚀 PIPELINE START - Content Type: mcq
[STEP 1] SCRAPING...
```

### 2. SCRAPER PHASE
```
📋 [SCRAPER] scrape_from_sources() - Starting scrape for content_type: mcq
  ✓ Found X active sources in ContentSource
  🔄 [1/3] Fetching from: https://example.com
    ✓ HTML fetched, extracting content...
    ✓ Extracted Y items
  🔄 [2/3] Fetching from: https://example2.com
    ...
📋 [SCRAPER] Total content extracted: N items
```

### 3. CONTENT PROCESSING
```
✅ [STEP 1] Scraped N articles
[STEP 2] PROCESSING & SAVING...

  [1/N] Processing article: Article Title...
    Source URL: https://example.com
    
    📋 [PROMPT_GEN] generate_mcq_prompt() - Source: https://example.c...
      ✓ Using DATABASE prompt for MCQ generation
      ✓ Prompt formatted successfully (length: 1234 chars)
    
    📋 [PROMPT] get_prompt_from_database() - Type: mcq, Source: https://example.c...
      ✓ Found SITE-SPECIFIC prompt for https://example.c...
    
    📋 [PROCESSOR] process_mcq_content() - Starting MCQ generation
      📤 Sending to LLM...
      ✓ LLM response received: <class 'dict'>
    
    📋 [SAVER] save_mcq_to_database() - Type: currentaffairs_mcq
      📥 Saving 3 questions...
      [1] ✓ Saved MCQ ID: 123
      [2] ✓ Saved MCQ ID: 124
      [3] ✓ Saved MCQ ID: 125
      ✓ Total saved: 3 MCQs
```

---

## Method-by-Method Print Output

### `scrape_from_sources()` - Lines 99-149
**Purpose**: Fetch and extract content from configured sources

**Print Sequence**:
1. **Entry Point** (Line 100):
   ```
   📋 [SCRAPER] scrape_from_sources() - Starting scrape for content_type: mcq
   ```

2. **Source Loading** (Line 127-128):
   ```
   ✓ Found 3 active sources in ContentSource
   Source 1: https://example.com
   ```

3. **Per-URL Fetching** (Line 137):
   ```
   🔄 [1/3] Fetching from: https://example.com/current-affairs
   ✓ HTML fetched, extracting content...
   ✓ Extracted 5 items
   ```

4. **Completion** (Line 149):
   ```
   📋 [SCRAPER] Total content extracted: 15 items
   ```

---

### `get_prompt_from_database()` - Lines 152-197
**Purpose**: Lookup source-specific or default LLM prompts from database

**Print Sequence**:
1. **Entry Point** (Line 172):
   ```
   📋 [PROMPT] get_prompt_from_database() - Type: mcq, Source: https://example.com
   ```

2. **Site-Specific Match** (Line 183):
   ```
   ✓ Found SITE-SPECIFIC prompt for https://example.c...
   ```
   OR **Fallback to Default** (Line 193):
   ```
   ⚠️  No site-specific prompt found, trying default...
   ✓ Using DEFAULT prompt for type 'mcq'
   ```
   OR **No Match** (Line 196):
   ```
   ✗ NO PROMPT FOUND for type 'mcq'
   ```

3. **Error Handling** (Line 198):
   ```
   ❌ ERROR: Database connection failed
   ```

---

### `generate_mcq_prompt()` - Lines 201-237
**Purpose**: Format the LLM prompt with article content

**Print Sequence**:
1. **Entry Point** (Line 203):
   ```
   📋 [PROMPT_GEN] generate_mcq_prompt() - Source: https://example.c...
   ```

2. **Prompt Source Selection**:
   - **Database Prompt** (Line 209):
     ```
     ✓ Using DATABASE prompt for MCQ generation
     ✓ Prompt formatted successfully (length: 1234 chars)
     ```
   - **Manual Substitution** (Line 216):
     ```
     ⚠️  Used manual substitution for prompt (length: 1234 chars)
     ```
   - **Hardcoded Default** (Line 220):
     ```
     ✓ Using HARDCODED prompt template for MCQ generation
     ```

---

### `generate_descriptive_prompt()` - Lines 239-275
**Purpose**: Format the LLM prompt for descriptive content generation

**Print Sequence** (Similar to `generate_mcq_prompt()`):
```
📋 [PROMPT_GEN] generate_descriptive_prompt() - Source: https://example.c...
  ✓ Using DATABASE prompt for descriptive generation
  ✓ Prompt formatted successfully (length: 1234 chars)
```

---

### `process_mcq_content()` - Lines 277-307
**Purpose**: Send prompt to LLM and receive MCQ generation response

**Print Sequence**:
1. **Entry Point** (Line 298):
   ```
   📋 [PROCESSOR] process_mcq_content() - Starting MCQ generation
   ```

2. **LLM Interaction** (Line 301):
   ```
   📤 Sending to LLM...
   ✓ LLM response received: <class 'dict'>
   ```

3. **Error Handling** (Line 306):
   ```
   ❌ ERROR: API rate limit exceeded
   ```

---

### `process_descriptive_content()` - Lines 309-333
**Purpose**: Send prompt to LLM for descriptive content generation

**Print Sequence** (Similar to `process_mcq_content()`):
```
📋 [PROCESSOR] process_descriptive_content() - Starting descriptive generation
  📤 Sending to LLM...
  ✓ LLM response received: <class 'dict'>
```

---

### `save_mcq_to_database()` - Lines 335-377
**Purpose**: Persist generated MCQs to database

**Print Sequence**:
1. **Entry Point** (Line 347):
   ```
   📋 [SAVER] save_mcq_to_database() - Type: currentaffairs_mcq
   ```

2. **Saving Progress** (Line 350):
   ```
   📥 Saving 3 questions...
   ```

3. **Per-Item Saves** (Line 373):
   ```
   [1] ✓ Saved MCQ ID: 123
   [2] ✓ Saved MCQ ID: 124
   [3] ✓ Saved MCQ ID: 125
   ```

4. **Completion** (Line 376):
   ```
   ✓ Total saved: 3 MCQs
   ```

5. **Error Handling**:
   ```
   ❌ ERROR saving to database: Duplicate entry
   ```

---

### `run_complete_pipeline()` - Lines 379-437
**Purpose**: Orchestrate entire scraping and processing workflow

**Print Sequence**:
1. **Pipeline Start** (Lines 386-388):
   ```
   ══════════════════════════════════════════════════════════════════
   🚀 PIPELINE START - Content Type: mcq
   ══════════════════════════════════════════════════════════════════
   ```

2. **Step 1: Scraping** (Lines 399-401):
   ```
   [STEP 1] SCRAPING...
   ✅ [STEP 1] Scraped 15 articles
   ```

3. **Step 2: Processing Loop** (Lines 412-429):
   ```
   [STEP 2] PROCESSING & SAVING...
   
   [1/15] Processing article: Article Title...
     Source URL: https://example.com
   
   [2/15] Processing article: Another Title...
     Source URL: https://example.com
   ```

4. **Pipeline Complete** (Lines 434-437):
   ```
   ✅ PIPELINE COMPLETE
   Total Processed: 15
   Errors: 0
   ```

---

## How to Use These Print Statements

### 1. **Real-Time Monitoring**
   Run the scraper from Django management command terminal:
   ```bash
   python manage.py scrape_current_affairs
   ```
   Watch the complete execution trace in your terminal.

### 2. **Debugging Workflow**
   If scraper gets stuck or errors occur:
   - Check which method printed last
   - Look for ❌ ERROR messages
   - Check database state if "SAVER" messages stop

### 3. **Performance Analysis**
   Use print statements to identify bottlenecks:
   - If scraper is slow: Look at `[SCRAPER]` timing
   - If LLM calls are slow: Check `[PROCESSOR]` timing
   - If saves are slow: Monitor `[SAVER]` progress

### 4. **Prompt Source Verification**
   Verify correct prompt is being used:
   - Look for "SITE-SPECIFIC", "DEFAULT", or "HARDCODED" indicators
   - Check URL matching against LLMPrompt database records

---

## Print Statement Legend

| Symbol | Meaning | Action |
|--------|---------|--------|
| 📋 | Method start/process info | Informational - watch flow |
| ✓ | Success/completion | Normal execution |
| ⚠️ | Warning/fallback | Something didn't match, fallback used |
| ❌ | Error/failure | Exception occurred, check logs |
| 📤 | Data sent/upload | External API call initiated |
| 📥 | Data received/saved | Database operation |
| 🔄 | Loop iteration | Processing item N of M |
| ✅ | Step complete | Phase successfully finished |
| 🚀 | Pipeline start | Entire workflow starting |

---

## Troubleshooting with Prints

### Issue: "No articles are being saved"
**Check prints for**:
1. Does `[SCRAPER]` show articles extracted?
2. Does `[PROCESSOR]` show LLM responses received?
3. Does `[SAVER]` show "Saved MCQ ID"?

If prints stop at `[PROCESSOR]`, LLM error occurred (check error print).
If no `[SAVER]` prints, processing failed silently.

### Issue: "Wrong prompt is being used"
**Check prints for**:
1. `[PROMPT]` line shows source_url being looked up
2. Is it showing "SITE-SPECIFIC", "DEFAULT", or "HARDCODED"?
3. Verify source_url in article matches LLMPrompt database entries

### Issue: "Slow execution"
**Use prints to locate bottleneck**:
1. Note timestamps between print statements
2. `[SCRAPER]` slow? → Check network/HTML extraction
3. `[PROCESSOR]` slow? → Check LLM API response time
4. `[SAVER]` slow? → Check database indexes

---

## Advanced: Modifying Print Detail Level

To reduce print verbosity, modify these regexes in current_affairs.py:
- Remove per-item prints (lines like `[{idx}] ✓ Saved...`) for fewer messages
- Keep method entry/exit prints for flow tracking
- Modify emoji styles for different visual preference

To increase verbosity:
- Add `print(f"  Details: {variable}")` after key operations
- Add `pprint(response)` to show full LLM responses
- Add timing info: `import time; start = time.time()` at method starts

---

## Complete Execution Example

```
🚀 PIPELINE START - Content Type: mcq

[STEP 1] SCRAPING...
📋 [SCRAPER] scrape_from_sources() - Starting scrape for content_type: mcq
  ✓ Found 2 active sources in ContentSource
  🔄 [1/2] Fetching from: https://www.thehindu.com
    ✓ HTML fetched, extracting content...
    ✓ Extracted 5 items
  🔄 [2/2] Fetching from: https://www.bbc.com/news
    ✓ HTML fetched, extracting content...
    ✓ Extracted 4 items
📋 [SCRAPER] Total content extracted: 9 items

✅ [STEP 1] Scraped 9 articles

[STEP 2] PROCESSING & SAVING...

  [1/9] Processing article: Supreme Court ruling on...
    Source URL: https://www.thehindu.com
    📋 [PROMPT_GEN] generate_mcq_prompt() - Source: https://www.thehindu.c
      ✓ Using DATABASE prompt for MCQ generation
      ✓ Prompt formatted successfully (length: 2145 chars)
    📋 [PROCESSOR] process_mcq_content() - Starting MCQ generation
      📤 Sending to LLM...
      ✓ LLM response received: <class 'dict'>
    📋 [SAVER] save_mcq_to_database() - Type: currentaffairs_mcq
      📥 Saving 4 questions...
      [1] ✓ Saved MCQ ID: 156
      [2] ✓ Saved MCQ ID: 157
      [3] ✓ Saved MCQ ID: 158
      [4] ✓ Saved MCQ ID: 159
      ✓ Total saved: 4 MCQs

  [2/9] Processing article: Bitcoin hits record high...
    Source URL: https://www.bbc.com/news
    📋 [PROMPT_GEN] generate_mcq_prompt() - Source: https://www.bbc.com/
      ✓ Using DATABASE prompt for MCQ generation
      ✓ Prompt formatted successfully (length: 2156 chars)
    ...
    ✓ Total saved: 3 MCQs

  [3/9] Processing article: ...
    ...

✅ PIPELINE COMPLETE
  Total Processed: 9
  Errors: 0
```

---

## Summary

All 8 core methods now have comprehensive print statements:
1. ✅ `scrape_from_sources()` - Source discovery and content extraction
2. ✅ `get_prompt_from_database()` - Prompt lookup and fallback logic
3. ✅ `generate_mcq_prompt()` - Prompt formatting for MCQ
4. ✅ `generate_descriptive_prompt()` - Prompt formatting for descriptive
5. ✅ `process_mcq_content()` - LLM MCQ generation
6. ✅ `process_descriptive_content()` - LLM descriptive generation
7. ✅ `save_mcq_to_database()` - Database persistence
8. ✅ `run_complete_pipeline()` - Pipeline orchestration

**Next Step**: Run a test scrape and monitor the terminal output to see the complete workflow trace!
