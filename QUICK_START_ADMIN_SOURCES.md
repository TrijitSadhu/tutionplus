# Quick Start: Adding GK Today URL from Admin Panel

## 🎯 What You Can Now Do

Instead of editing `genai/config.py`, you can add news sources directly from the Django admin panel!

## ✅ Steps to Add GK Today URL

### 1. Start Django Server
```bash
cd django/django_project
python manage.py runserver
```

### 2. Go to Admin Panel
- Open: `http://localhost:8000/admin/`
- Login with your admin credentials

### 3. Add News Source
1. In the left sidebar, look for **"BANK"** section
2. Click **"News sources"** (or go directly to: http://localhost:8000/admin/bank/newssource/)
3. Click **"ADD NEWS SOURCE"** button (top right, blue button)

### 4. Fill the Form

**Field: Name**
```
GK Today
```

**Field: URL**
```
https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/
```

**Field: Content Type**
```
Select: "Current Affairs MCQ"
```

**Field: Is Active**
```
✓ Check the box
```

**Field: Description** (Optional)
```
Daily current affairs quiz from GK Today
```

### 5. Save
- Click **"SAVE"** button at the bottom right

### ✅ Done!

The URL is now in the database. Next time the scraper runs:
- It will fetch from the database instead of hardcoded config
- It will scrape this GK Today URL
- It will generate MCQs using the LLM prompt

## 🎯 To Manage More Sources

Use the same admin panel to:
- **Add more URLs**: Click "ADD NEWS SOURCE"
- **Edit existing**: Click on the source name in the list
- **Deactivate**: Uncheck "Is Active" checkbox (disables scraping)
- **Delete**: Click the source name, then "DELETE" button

## 📋 Complete Admin Flow

```
Admin Panel
├── Django Admin Home (/admin/)
│   └── BANK section
│       └── "News sources" link
│           ├── List view (all sources)
│           ├── ADD NEWS SOURCE (new source form)
│           ├── Edit (click any source name)
│           └── Delete (in edit view)
```

## 💡 Pro Tips

1. **Test URL first**: Make sure the URL works in your browser before adding
2. **Content Type matters**: Choose "MCQ" or "Descriptive" based on content
3. **Is Active field**: Uncheck to pause scraping without deleting
4. **Create custom prompts**: Go to `/admin/bank/llmprompt/` to create source-specific prompts
5. **Search & filter**: Use search box to find sources by name/URL

## 🔗 Admin Links

| Page | URL |
|------|-----|
| Admin Home | `http://localhost:8000/admin/` |
| News Sources | `http://localhost:8000/admin/bank/newssource/` |
| LLM Prompts | `http://localhost:8000/admin/bank/llmprompt/` |

## ⚙️ How It Works Behind the Scenes

When you add a source in admin:
1. It's saved in database as a **NewsSource** record
2. Scraper calls `get_sources_from_database()` function
3. Function fetches **active** sources from database
4. Scraper processes each URL
5. LLMPrompt is fetched (source-specific or default)
6. Content is generated and saved

## ✨ Features

✅ Add/Edit/Delete sources via admin (no coding needed)  
✅ Enable/disable sources without deleting  
✅ Filter by content type (MCQ or Descriptive)  
✅ Search by name or URL  
✅ Database tracks creation date  
✅ Falls back to hardcoded config if database unavailable  
✅ Works with source-specific LLM prompts  

## 📚 For More Details

See: `ADMIN_NEWS_SOURCES_GUIDE.md` for comprehensive documentation

---

**You're all set!** 🚀 Manage your news sources from the admin panel now.
