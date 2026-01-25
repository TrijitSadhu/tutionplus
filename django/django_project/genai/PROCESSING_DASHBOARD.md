# GenAI Processing Dashboard - Daily Fetch Task Management

## Overview
A comprehensive Django admin interface for triggering, tracking, and managing automated MCQ and Current Affairs content fetching tasks with real-time status monitoring.

## Features

### 1. **One-Click Fetch Trigger**
- Fetch MCQ content only
- Fetch Current Affairs only
- Fetch both simultaneously
- Real-time progress tracking

### 2. **Processing Status Dashboard**
- Visual status badges (pending, running, completed, failed)
- Progress bars with percentage
- Success/Error counters
- Task duration tracking
- Statistics overview

### 3. **Task Scheduling**
- Schedule daily runs at specific times
- Built-in task tracking model
- Automated logging of all operations

### 4. **Admin Integration**
- Custom ProcessingLog model with advanced admin interface
- Colored status badges
- Progress visualization
- Detailed task history
- Quick actions for task management

## Architecture

### Components

#### 1. Models (`genai/models.py`)
```python
ProcessingLog:
  - task_type: 'mcq_fetch', 'current_affairs_fetch', 'both'
  - status: 'pending', 'running', 'completed', 'failed'
  - progress tracking fields
  - timing fields (started_at, completed_at)
  - error handling
```

#### 2. Management Command (`genai/management/commands/fetch_all_content.py`)
Handles the actual fetching logic:
- Fetches MCQ content
- Fetches Current Affairs content
- Updates progress in real-time
- Logs detailed output
- Supports scheduling

#### 3. Views (`genai/views.py`)
Three main view functions:
- `processing_dashboard()`: Displays the dashboard
- `trigger_fetch()`: POST endpoint to start fetch task
- `task_status()`: JSON endpoint to get task status

#### 4. Admin Interface (`genai/admin.py`)
`ProcessingLogAdmin` class with:
- Color-coded status badges
- Progress bars
- Detailed field display
- Quick action buttons
- Custom filtering and search

#### 5. Dashboard Template (`genai/templates/genai/admin/processing_dashboard.html`)
Beautiful, responsive admin interface with:
- Statistics cards
- Action buttons
- Latest task display
- Recent tasks table
- Auto-refresh for running tasks
- Real-time progress updates

#### 6. URLs (`genai/urls.py`)
Three new admin endpoints:
- `/genai/admin/dashboard/`: Main dashboard
- `/genai/admin/trigger-fetch/`: Fetch trigger (POST)
- `/genai/admin/task-status/<id>/`: Task status (JSON)

## Usage

### Method 1: Dashboard Click (Easiest)
1. Login to Django Admin
2. Click "Processing Dashboard" link
3. Choose action button:
   - 🚀 Fetch Both
   - 📖 Fetch MCQ Only
   - 📰 Fetch Current Affairs Only
4. Monitor progress in real-time

### Method 2: Admin Panel
1. Go to `/admin/genai/processinglog/`
2. View all tasks with status
3. Click "View Status" for detailed info
4. Use admin actions to manage tasks

### Method 3: Command Line (For Scheduled Tasks)
```bash
# Fetch both MCQ and Current Affairs
python manage.py fetch_all_content --type=both

# Fetch MCQ only
python manage.py fetch_all_content --type=mcq

# Fetch Current Affairs only
python manage.py fetch_all_content --type=current_affairs

# Schedule for daily run at 2:30 PM
python manage.py fetch_all_content --type=both --schedule="14:30"
```

### Method 4: Scheduled Task (Production)
Set up a cron job or system scheduler:

**Linux/Mac (crontab):**
```bash
# Daily at 2:30 PM
30 14 * * * cd /path/to/project && python manage.py fetch_all_content --type=both
```

**Windows (Task Scheduler):**
```
Program: python.exe
Arguments: manage.py fetch_all_content --type=both
Working Directory: C:\path\to\project
Schedule: Daily at 14:30
```

**Using APScheduler (Alternative):**
Create `genai/schedulers.py`:
```python
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: call_command('fetch_all_content', type='both'),
        'cron',
        hour=14,
        minute=30
    )
    scheduler.start()
```

## Database Schema

### ProcessingLog Model Fields

| Field | Type | Purpose |
|-------|------|---------|
| task_type | CharField | Type of fetch task |
| status | CharField | Current task status |
| started_at | DateTime | When task began |
| completed_at | DateTime | When task finished |
| total_items | IntegerField | Total items to process |
| processed_items | IntegerField | Items completed |
| success_count | IntegerField | Successful items |
| error_count | IntegerField | Failed items |
| mcq_status | CharField | MCQ fetch status message |
| current_affairs_status | CharField | CA fetch status message |
| error_message | TextField | Error details |
| log_details | TextField | JSON log data |
| scheduled_time | DateTime | Scheduled run time |
| is_scheduled | BooleanField | Is this scheduled? |
| created_at | DateTime | Record creation time |
| updated_at | DateTime | Last update time |
| created_by | ForeignKey | User who triggered task |

## Admin Interface Features

### Status Badges
- 🟠 **Pending**: Waiting to start
- 🔴 **Running**: Currently executing
- 🟢 **Completed**: Finished successfully
- 🔴 **Failed**: Task encountered error

### Progress Indicators
- Progress bar showing percentage complete
- Processed items / Total items counter
- Real-time updates (auto-refresh every 3s for running tasks)

### Actions
- Mark as Completed
- Mark as Failed
- Clear Error Messages
- View Full Status

### Statistics
- Total Tasks Count
- Completed Tasks
- Running Tasks
- Failed Tasks
- Pending Tasks

## API Reference

### trigger_fetch (POST)
**Endpoint:** `/genai/admin/trigger-fetch/`

**Parameters:**
```json
{
  "task_type": "both|mcq|current_affairs"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Fetch task completed",
  "task_id": 123,
  "output": "Task output...",
  "error": ""
}
```

### task_status (GET)
**Endpoint:** `/genai/admin/task-status/<task_id>/`

**Response:**
```json
{
  "id": 123,
  "status": "completed|running|pending|failed",
  "task_type": "MCQ Fetch",
  "progress": 75,
  "processed": 75,
  "total": 100,
  "success_count": 72,
  "error_count": 3,
  "mcq_status": "✓ Completed",
  "current_affairs_status": "✓ Completed",
  "duration": 45.23,
  "created_at": "2026-01-25T14:30:00Z",
  "completed_at": "2026-01-25T14:31:00Z",
  "error_message": ""
}
```

## Error Handling

### Task Failures
- Logged in ProcessingLog with error_message field
- Visible in admin interface with alert boxes
- Detailed error tracking for debugging

### Timeout Handling
- Default 5-minute timeout per task
- Returns 408 error if exceeded
- Task marked as failed with error message

### Log Details
- JSON stored in log_details field
- Includes detailed fetch results
- Available for debugging and analytics

## Dashboard Auto-Refresh

The dashboard automatically refreshes every 3 seconds while a task is running, giving real-time progress updates without manual refresh.

## Customization

### Add New Task Types
1. Update `ProcessingLog.TASK_TYPES`
2. Add handler in `update_mcq_info_on_save()`
3. Add UI button in template

### Modify Progress Tracking
1. Update `progress_percentage` calculation
2. Modify progress bar visualization
3. Add additional metrics

### Change Refresh Rate
In template, line ~350:
```javascript
setTimeout(() => location.reload(), 3000); // Change 3000ms
```

## Performance Considerations

### Optimizations
- Database indexes on `status` and `created_at`
- Pagination in recent tasks table (20 items)
- JSON compression for log details
- Async task execution

### Monitoring
- Success/Error ratio tracking
- Duration metrics
- Progress percentage calculation
- Real-time status updates

## Security

### Access Control
- Staff-only views (login_required + is_staff check)
- CSRF protection on POST endpoints
- User tracking (created_by field)

### Logging
- All operations logged
- Error messages preserved
- Audit trail maintained

## Troubleshooting

### Task Hangs/Timeout
- Check system resources
- Verify fetch sources are accessible
- Increase timeout in views.py

### Migration Issues
```bash
python manage.py showmigrations genai
python manage.py migrate genai
```

### Admin Not Loading
- Clear browser cache
- Check Django system checks
- Verify template path
- Check for import errors

## Future Enhancements

1. Email notifications on completion
2. Slack/Discord integration
3. Bulk scheduling interface
4. Advanced filtering and analytics
5. Task retry logic
6. Parallel task execution
7. Database cleanup (archive old logs)
8. Export task history as CSV/JSON

## Support

For issues or questions:
1. Check Django logs in console
2. Review ProcessingLog entries
3. Verify migration applied
4. Test management command directly
