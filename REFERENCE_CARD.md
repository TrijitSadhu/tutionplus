# GenAI Processing Dashboard - Reference Card

## 🚀 Quick Access

| Item | Link/Command |
|------|--------------|
| **Dashboard** | http://localhost:8000/genai/admin/dashboard/ |
| **Admin Logs** | http://localhost:8000/admin/genai/processinglog/ |
| **Django Admin** | http://localhost:8000/admin/ |
| **Full Docs** | `genai/PROCESSING_DASHBOARD.md` |
| **Quick Start** | `genai/QUICK_START.py` |

## 🎯 Commands

### Start Django Server
```bash
python manage.py runserver
```

### Fetch Now (Command Line)
```bash
# Both MCQ and Current Affairs
python manage.py fetch_all_content --type=both

# MCQ only
python manage.py fetch_all_content --type=mcq

# Current Affairs only
python manage.py fetch_all_content --type=current_affairs

# With help
python manage.py fetch_all_content --help
```

## 📊 Status Values

| Status | Meaning |
|--------|---------|
| 🔳 pending | Waiting to start |
| ⚙️ running | Currently executing |
| ✅ completed | Finished successfully |
| ❌ failed | Encountered error |

## 📈 Progress Tracking

**Visible Fields:**
- `processed_items` - How many done
- `total_items` - How many total
- `success_count` - Successful
- `error_count` - Failed
- `duration` - Elapsed time
- `progress_percentage` - % complete

## 🔐 Access

**Who can access:**
- Staff users only (is_staff=True)
- Must be logged in

**How to grant access:**
1. Go to `/admin/auth/user/`
2. Select user
3. Check "Staff status"
4. Save

## 📅 Schedule for Daily Run

### Linux/Mac (Crontab)
```bash
# Edit crontab
crontab -e

# Add this line for 2:30 PM daily
30 14 * * * cd /path/to/django/django_project && python manage.py fetch_all_content --type=both
```

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Set name: "Daily MCQ & Current Affairs Fetch"
4. Set trigger: Daily at 14:30
5. Set action:
   - Program: `C:\path\to\python.exe`
   - Arguments: `manage.py fetch_all_content --type=both`
   - Working: `C:\path\to\django_project`

### Alternative (APScheduler)
```python
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

scheduler = BackgroundScheduler()
scheduler.add_job(
    lambda: call_command('fetch_all_content', type='both'),
    'cron',
    hour=14,
    minute=30
)
scheduler.start()
```

## 🛠️ How It Works

```
Dashboard (UI)
    ↓
    → Click "Fetch Both" button
    ↓
trigger_fetch() view (AJAX)
    ↓
    → Call management command
    ↓
fetch_all_content command
    ↓
    → Fetch MCQ content
    → Fetch Current Affairs content
    → Update ProcessingLog
    ↓
processing_dashboard shows results
```

## 📱 Dashboard Features

| Feature | Details |
|---------|---------|
| **Stats Cards** | Total, Completed, Running, Failed, Pending |
| **Action Buttons** | Fetch Both, Fetch MCQ, Fetch CA |
| **Latest Task** | Shows current/most recent task |
| **Progress Bar** | Visual progress with percentage |
| **Recent Tasks** | Table of last 20 tasks |
| **Auto-Refresh** | Updates every 3s while running |
| **Error Display** | Shows error details if failed |

## 📊 Admin Interface

Go to `/admin/genai/processinglog/`

**Features:**
- Color-coded status badges
- Progress bars
- Detailed information
- Search and filter
- Bulk actions
- Quick view status

**Actions Available:**
- Mark as completed
- Mark as failed
- Clear error messages
- View full status details

## 🔍 Monitor Progress

### In Dashboard
1. Click action button
2. See progress bar update
3. Watch success/error counts
4. See final result

### In Admin
1. Go to ProcessingLog
2. Click task ID
3. View all details
4. See detailed status

### From Command Line
```bash
python manage.py fetch_all_content --type=both
# Watch console output in real-time
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Dashboard 404 | Check URLs in genai/urls.py |
| Import error | Run: `python manage.py check` |
| No ProcessingLog | Run: `python manage.py migrate genai` |
| Staff access denied | Set is_staff=True for user |
| Task times out | Check data sources, increase timeout |

## 📝 What Gets Logged

Each task records:
```
- Task ID
- Task type (both/mcq/current_affairs)
- Status (pending/running/completed/failed)
- Start & end times
- Items processed
- Success & error counts
- Error messages
- Detailed JSON logs
- Who triggered it (user)
```

## 🎨 Dashboard Look

**Color Scheme:**
- 🟠 Pending - Orange (#FFA500)
- 🔴 Running - Red (#FF6B6B)
- 🟢 Completed - Green (#51CF66)
- 🔴 Failed - Dark Red (#C92A2A)

## 📚 Database

**Table:** `genai_processinglog`

**Key Fields:**
- `id` - Task ID
- `task_type` - Type of fetch
- `status` - Current status
- `started_at` - Start time
- `completed_at` - End time
- `processed_items` - Items done
- `success_count` - Successful
- `error_count` - Failed
- `mcq_status` - MCQ details
- `current_affairs_status` - CA details
- `error_message` - Error info
- `log_details` - JSON logs

## 🔗 API Endpoints

### Trigger Fetch
**POST** `/genai/admin/trigger-fetch/`
```json
{
  "task_type": "both"
}
```

### Get Status
**GET** `/genai/admin/task-status/<id>/`
```json
{
  "id": 1,
  "status": "completed",
  "progress": 100,
  "success_count": 50,
  "error_count": 0
}
```

## 💡 Tips

1. **First Run:** Start with `--type=mcq` to test
2. **Schedule:** Set for off-peak hours (e.g., 2:30 AM)
3. **Monitor:** Check dashboard daily for status
4. **Archive:** Cleanup old logs monthly
5. **Backup:** Export ProcessingLog before cleanup

## 🎓 Learning Resources

See these files for more details:
- `genai/PROCESSING_DASHBOARD.md` - Complete guide
- `genai/QUICK_START.py` - Quick examples
- `genai/models.py` - Model structure
- `genai/views.py` - View implementation
- `genai/admin.py` - Admin customization
