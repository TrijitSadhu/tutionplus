# Visual Guide: Admin Panel News Source Management

## Step-by-Step Screenshots (Text Version)

### Step 1: Login to Django Admin
```
Browser URL: http://localhost:8000/admin/

┌─────────────────────────────────────┐
│        Django Administration        │
├─────────────────────────────────────┤
│                                     │
│  Username: [________________]       │
│  Password: [________________]       │
│                                     │
│          [Log in]                   │
│                                     │
└─────────────────────────────────────┘
```

### Step 2: Django Admin Home
```
┌────────────────────────────────────────┐
│    Django Administration - Home        │
├────────────────────────────────────────┤
│                                        │
│ Site Administration                    │
│                                        │
│ BANK                                   │
│  □ News sources           [+ Add]      │
│  □ LLM prompts            [+ Add]      │
│  □ Current affairs MCQs   [+ Add]      │
│  □ ... (other models)                  │
│                                        │
│ AUTHENTICATION AND AUTHORIZATION       │
│  □ Groups                              │
│  □ Users                               │
│                                        │
└────────────────────────────────────────┘
```

### Step 3: News Sources List (Empty)
```
URL: http://localhost:8000/admin/bank/newssource/

┌────────────────────────────────────────────────────┐
│ News sources / Select news source to change        │
├────────────────────────────────────────────────────┤
│ [Search] [Filter]              [+ ADD NEWS SOURCE] │
├────────────────────────────────────────────────────┤
│                                                    │
│ No news sources yet. Add one?                      │
│                                                    │
│ To add a new record, click [+ ADD NEWS SOURCE]     │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Step 4: Add News Source Form
```
┌─────────────────────────────────────────────────────────┐
│ Add news source                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ News Source Information                                 │
│                                                         │
│  Name: [GK Today                    ]                   │
│                                                         │
│  URL:  [https://www.gktoday.in/daily-...]             │
│                                                         │
│  Content Type: ○ Current Affairs MCQ ✓                │
│               ○ Current Affairs Descriptive            │
│                                                         │
│ Status                                                  │
│                                                         │
│  Is Active: [✓] (checked)                              │
│                                                         │
│ Details                                                 │
│                                                         │
│  Description:                                           │
│  ┌─────────────────────────────────────┐              │
│  │ Daily current affairs quiz from GK  │              │
│  └─────────────────────────────────────┘              │
│                                                         │
│ Metadata                                                │
│                                                         │
│  Created At: [automatically filled]                     │
│  Updated At: [automatically filled]                     │
│                                                         │
│                     [SAVE] [SAVE AND ADD ANOTHER]     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Step 5: News Sources List (Populated)
```
┌──────────────────────────────────────────────────────────┐
│ News sources (1)                                         │
├──────────────────────────────────────────────────────────┤
│ [Search: ________] [Filters: ▼]    [+ ADD NEWS SOURCE]  │
├──────────────────────────────────────────────────────────┤
│ Name     │ URL                        │ Type  │ Active   │
├──────────┼────────────────────────────┼───────┼──────────┤
│ GK Today │ https://www.gktoday.in/... │  MCQ  │    ✓     │
│          │ [Created: 2026-01-25]      │       │          │
└──────────────────────────────────────────────────────────┘
```

### Step 6: Edit Existing Source
```
Click on "GK Today" to edit:

┌─────────────────────────────────────────────────────────┐
│ Change news source                                      │
├─────────────────────────────────────────────────────────┤
│ [GK Today]                                              │
│                                                         │
│ News Source Information                                 │
│                                                         │
│  Name: [GK Today                    ]                   │
│                                                         │
│  URL:  [https://www.gktoday.in/...  ]                 │
│                                                         │
│  Content Type: ○ Current Affairs MCQ ✓                │
│               ○ Current Affairs Descriptive            │
│                                                         │
│ Status                                                  │
│                                                         │
│  Is Active: [✓] (checked)                              │
│             To disable scraping, uncheck this box      │
│                                                         │
│ Details                                                 │
│                                                         │
│  Description:                                           │
│  ┌─────────────────────────────────────┐              │
│  │ Daily current affairs quiz          │              │
│  └─────────────────────────────────────┘              │
│                                                         │
│                     [SAVE]  [DELETE]  [HISTORY]        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Step 7: Delete Confirmation
```
┌─────────────────────────────────────────┐
│ Confirm deletion                        │
├─────────────────────────────────────────┤
│                                         │
│ Are you sure you want to delete         │
│ "GK Today"?                             │
│                                         │
│ This action cannot be undone.          │
│                                         │
│    [Cancel]            [Yes, I'm sure]  │
│                                         │
└─────────────────────────────────────────┘
```

### Step 8: Search & Filter
```
┌──────────────────────────────────────────────────────────┐
│ News sources (3)                                         │
├──────────────────────────────────────────────────────────┤
│ [Search: "gk"  [Search]] [▼ Filters ↑]   [+ ADD]         │
│                                                          │
│ FILTERS                                                  │
│  Content Type:                                           │
│   ○ Current Affairs MCQ (2)                             │
│   ○ Current Affairs Descriptive (1)                     │
│                                                          │
│  Is Active:                                              │
│   ○ Yes (3)                                             │
│   ○ No (0)                                              │
│                                                          │
│  Created At:                                             │
│   ○ Any time                                            │
│   ○ Today                                               │
│   ○ This week                                           │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Name     │ URL                        │ Type  │ Active   │
├──────────┼────────────────────────────┼───────┼──────────┤
│ GK Today │ https://www.gktoday.in/... │  MCQ  │    ✓     │
└──────────────────────────────────────────────────────────┘
```

## Key Admin Panel Features

### 1️⃣ Add News Source
- Click **[+ ADD NEWS SOURCE]** button
- Fill all required fields (Name, URL, Content Type)
- Optionally add Description
- Check "Is Active" to enable
- Click **[SAVE]**

### 2️⃣ Edit News Source
- Click the source name in the list
- Modify any field
- Click **[SAVE]** to update

### 3️⃣ Disable News Source
- Click the source name
- Uncheck **"Is Active"** checkbox
- Click **[SAVE]**
- Scraper will skip this URL

### 4️⃣ Delete News Source
- Click the source name
- Click **[DELETE]** button at bottom
- Confirm deletion

### 5️⃣ Search Sources
- Type in search box at top
- Searches by Name or URL
- Results update in real-time

### 6️⃣ Filter Sources
- Click **[Filters]** option
- Filter by:
  - Content Type (MCQ or Descriptive)
  - Is Active (Yes or No)
  - Created At (Today, This week, etc.)

## Field Reference

### Name
- **Required**: Yes
- **Type**: Text (max 200 characters)
- **Example**: "GK Today"
- **Help**: Friendly name for identification

### URL
- **Required**: Yes
- **Type**: URL (must be valid)
- **Example**: `https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/`
- **Help**: Full URL to scrape content from
- **Note**: Must be unique (no duplicates)

### Content Type
- **Required**: Yes
- **Type**: Dropdown (2 options)
- **Options**:
  - `Current Affairs MCQ` - for MCQ content
  - `Current Affairs Descriptive` - for descriptive content
- **Help**: Type affects which prompt template is used

### Is Active
- **Required**: No (default: checked)
- **Type**: Checkbox
- **Default**: ✓ (enabled)
- **Help**: Controls whether scraper processes this URL
- **Tip**: Uncheck to pause without deleting

### Description
- **Required**: No
- **Type**: Text (unlimited)
- **Example**: "Daily current affairs quiz"
- **Help**: Optional notes about the source

### Created At / Updated At
- **Type**: Date & Time (read-only)
- **Help**: Automatically set by system
- **Visible in**: Metadata section (collapsed by default)

## Workflow Example

### Complete Workflow: Add GK Today + Create Custom Prompt

#### Part 1: Add Source (5 minutes)

1. Go to `/admin/bank/newssource/`
2. Click [+ ADD NEWS SOURCE]
3. Fill:
   - Name: `GK Today`
   - URL: `https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/`
   - Content Type: `Current Affairs MCQ`
   - Is Active: ✓
4. Click [SAVE]

#### Part 2: Create Source-Specific Prompt (5 minutes)

1. Go to `/admin/bank/llmprompt/`
2. Click [+ ADD LLM PROMPT]
3. Fill:
   - Source URL: `https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/`
   - Prompt Type: `MCQ`
   - Prompt Text: `Your custom MCQ prompt here...`
   - Is Default: ☐ (unchecked)
   - Is Active: ✓
4. Click [SAVE]

#### Part 3: Run Scraper

- Scraper automatically fetches sources from database
- Uses the custom prompt you created
- Generates MCQs using LLM
- Saves to database

## Status Indicators

### Content Type Display
- **MCQ**: Shows as "Current Affairs MCQ"
- **Descriptive**: Shows as "Current Affairs Descriptive"

### Active Status
- **✓**: Active (will be scraped)
- **☐**: Inactive (will be skipped)

### Timestamps Format
- **Example**: "January 25, 2026 at 4:49 PM"
- **Location**: Metadata section

## Tips & Tricks

1. **Bulk Import**:
   - Use `genai/scripts/add_news_sources.py` to add multiple sources at once

2. **Prevent Duplicates**:
   - System prevents duplicate URLs automatically
   - Try to add same URL twice? You'll get an error

3. **Sort by Date**:
   - Click "Created At" column header to sort by date
   - Click again to reverse sort

4. **URL Preview**:
   - URLs longer than 60 characters are truncated with "..."
   - Hover over or click to see full URL

5. **Pagination**:
   - Admin shows 100 items per page
   - Navigate between pages at bottom

## Common Tasks

| Task | Steps |
|------|-------|
| Add 1 source | Click [+ ADD], fill form, [SAVE] |
| Add 5 sources | Use `add_news_sources.py` script |
| Find a source | Type name/URL in search box |
| Temporarily stop scraping | Uncheck "Is Active", [SAVE] |
| Delete old source | Click source, [DELETE], confirm |
| Edit URL | Click source, change URL, [SAVE] |

---

**All changes take effect immediately!** The scraper picks up new sources on the next run.
