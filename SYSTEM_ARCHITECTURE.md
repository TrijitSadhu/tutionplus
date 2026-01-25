# GenAI Processing Dashboard - System Architecture

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Django Admin Interface                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ProcessingLog Admin (genai/admin.py)                  │   │
│  │  ✓ Color-coded status badges                          │   │
│  │  ✓ Progress bars                                      │   │
│  │  ✓ Bulk actions                                       │   │
│  │  ✓ Search & filter                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Processing Dashboard (genai/views.py)                 │   │
│  │  URL: /genai/admin/dashboard/                          │   │
│  │  ✓ Statistics cards                                    │   │
│  │  ✓ One-click fetch buttons                             │   │
│  │  ✓ Latest task display                                 │   │
│  │  ✓ Recent tasks table                                  │   │
│  │  ✓ Auto-refresh (3s)                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                    AJAX Request (POST)
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│             Backend Views (genai/views.py)                      │
│                                                                 │
│  trigger_fetch() ─────→ Start management command              │
│      ↓                                                          │
│  task_status() ───────→ Return JSON status                     │
│                                                                │
│  Staff-only access                                             │
│  CSRF protection                                               │
│  Error handling                                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
         Calls Django Management Command
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  Management Command: fetch_all_content.py                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ Fetch MCQ Content (fetch_and_process_current_affairs)│     │
│  │  - Parse sources                                     │     │
│  │  - Extract data                                      │     │
│  │  - Update database                                   │     │
│  │  - Track success/errors                              │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ Fetch Current Affairs (fetch_and_process_current...)│     │
│  │  - Parse sources                                     │     │
│  │  - Extract data                                      │     │
│  │  - Update database                                   │     │
│  │  - Track success/errors                              │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                 │
│  └──→ Update ProcessingLog with results                       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
              Updates Database ProcessingLog
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│               Database (PostgreSQL)                              │
│                                                                 │
│  genai_processinglog                                            │
│  ├─ id                                                          │
│  ├─ task_type ('both', 'mcq_fetch', 'current_affairs_fetch')  │
│  ├─ status ('pending', 'running', 'completed', 'failed')      │
│  ├─ started_at                                                 │
│  ├─ completed_at                                               │
│  ├─ processed_items                                            │
│  ├─ total_items                                                │
│  ├─ success_count                                              │
│  ├─ error_count                                                │
│  ├─ mcq_status                                                 │
│  ├─ current_affairs_status                                     │
│  ├─ error_message                                              │
│  ├─ log_details (JSON)                                         │
│  ├─ created_by (User FK)                                       │
│  └─ Timestamps                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
        Dashboard Auto-Refreshes Every 3 Seconds
                            ↓
            User Sees Real-Time Progress Update
```

## Data Flow

### Scenario 1: Click "Fetch Both"

```
User clicks "Fetch Both"
    ↓
JavaScript triggerFetch('both')
    ↓
POST /genai/admin/trigger-fetch/
    ├─ Method: trigger_fetch()
    ├─ Create ProcessingLog (status=pending)
    ├─ Call management command
    └─ Return task_id
    ↓
JavaScript shows confirmation
    ↓
Dashboard auto-refreshes every 3s
    ↓
GET /genai/admin/task-status/123/
    ├─ Method: task_status()
    ├─ Return JSON with current status
    └─ Parse and display in UI
    ↓
Progress bar updates
    ├─ Shows % complete
    ├─ Shows items processed
    ├─ Shows success/error counts
    └─ Updates status messages
    ↓
Task completes
    ├─ Status changes to 'completed'
    ├─ Final counts displayed
    └─ Auto-refresh stops
```

### Scenario 2: Run from Command Line

```
$ python manage.py fetch_all_content --type=both
    ↓
ProcessingLog created (status=running)
    ↓
MCQ Fetch
    ├─ Fetch data from sources
    ├─ Process items
    ├─ Update database
    └─ Track progress
    ↓
Current Affairs Fetch
    ├─ Fetch data from sources
    ├─ Process items
    ├─ Update database
    └─ Track progress
    ↓
ProcessingLog updated
    ├─ Status = 'completed'
    ├─ Set all counts
    ├─ Log details stored as JSON
    └─ Duration calculated
    ↓
Console output displayed
    ↓
✅ Task complete
```

### Scenario 3: Scheduled Daily Run

```
Cron Job Triggers (2:30 PM)
    ↓
$ python manage.py fetch_all_content --type=both
    ↓
[Same as Scenario 2]
    ↓
ProcessingLog saved to database
    ↓
Admin can review anytime
    ↓
Dashboard shows in "Recent Tasks"
```

## File Organization

```
genai/
├── models.py
│   └── ProcessingLog (new)
│
├── views.py
│   ├── processing_dashboard() (new)
│   ├── trigger_fetch() (new)
│   └── task_status() (new)
│
├── urls.py
│   ├── /genai/admin/dashboard/ (new)
│   ├── /genai/admin/trigger-fetch/ (new)
│   └── /genai/admin/task-status/<id>/ (new)
│
├── admin.py
│   └── ProcessingLogAdmin (new)
│
├── management/
│   └── commands/
│       └── fetch_all_content.py (new)
│
├── templates/
│   └── genai/admin/
│       └── processing_dashboard.html (new)
│
├── PROCESSING_DASHBOARD.md (new)
├── QUICK_START.py (new)
│
└── migrations/
    └── 0002_auto_20260125_0329.py (new)

Root:
├── GENAI_IMPLEMENTATION_SUMMARY.md (new)
└── REFERENCE_CARD.md (new)
```

## URL Routes

```
GET  /genai/admin/dashboard/        → processing_dashboard()
POST /genai/admin/trigger-fetch/    → trigger_fetch()
GET  /genai/admin/task-status/123/  → task_status(123)
```

## Database Schema

```
ProcessingLog Table
├─ id (PK) - Auto-increment
├─ task_type - Enum (mcq_fetch, current_affairs_fetch, both)
├─ status - Enum (pending, running, completed, failed)
├─ started_at - DateTime
├─ completed_at - DateTime
├─ total_items - Integer
├─ processed_items - Integer
├─ success_count - Integer
├─ error_count - Integer
├─ mcq_status - Text (status message)
├─ current_affairs_status - Text (status message)
├─ error_message - Text (error details)
├─ log_details - Text (JSON formatted)
├─ scheduled_time - DateTime
├─ is_scheduled - Boolean
├─ created_at - DateTime (auto)
├─ updated_at - DateTime (auto)
└─ created_by - FK to User

Indexes:
├─ (-created_at) for recent queries
└─ (status, -created_at) for filtering
```

## Status Flow Diagram

```
                    ┌─────────┐
                    │ PENDING │
                    └────┬────┘
                         ↓
                    ┌─────────┐
                    │ RUNNING │
                    └────┬────┘
                         ↓
                    ┌──────────┐
                    │ COMPLETED│
                    └──────────┘
                    
                         ↗
                    ┌─────────┐
            ───────│ FAILED  │
            ↑      └─────────┘
            │
         Can retry
```

## Performance Optimizations

```
Database
├─ Index on (-created_at)
├─ Index on (status, -created_at)
└─ Pagination (20 items per page)

Views
├─ Staff-only check (early exit)
├─ CSRF protection
└─ Timeout handling (5 minutes)

Template
├─ Auto-refresh (only when running)
├─ Minimal DOM updates
└─ CSS animations for progress

Command
├─ Efficient batch processing
├─ Progress tracking per item
└─ Error handling without blocking
```

## Integration Points

```
Django Admin
    ↓
ProcessingLogAdmin
    ├─ List view
    ├─ Detail view
    ├─ Change view
    └─ Custom actions

Custom Dashboard
    ├─ Statistics
    ├─ Action buttons
    ├─ Progress display
    └─ Task history

API Endpoints
    ├─ AJAX trigger
    ├─ Status polling
    └─ Error handling

Management Command
    ├─ CLI interface
    ├─ Cron compatible
    └─ Detailed logging
```

## Security Model

```
Access Control
├─ Login required (is_authenticated)
├─ Staff only (is_staff=True)
└─ CSRF protection (POST)

Logging
├─ User tracking (created_by)
├─ Audit trail (timestamps)
├─ Error recording (error_message)
└─ Full JSON logs (log_details)

Validation
├─ Task type validation
├─ Status validation
├─ Error handling
└─ Timeout protection
```

## Message Queue Alternative (Future)

```
Current (Synchronous):
User → Dashboard → trigger_fetch() → Command runs → Result

Future (Asynchronous):
User → Dashboard → Queue Task → Celery Worker → Database Update
                  ↓
            Real-time Status via WebSocket or AJAX
```
