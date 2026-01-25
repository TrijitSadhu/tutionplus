#!/usr/bin/env python
"""
Quick Start Guide for GenAI Processing Dashboard

Usage Examples:
    # Start Django server
    python manage.py runserver

    # Access dashboard at:
    http://127.0.0.1:8000/genai/admin/dashboard/

    # One-command fetches:
    python manage.py fetch_all_content --type=both
    python manage.py fetch_all_content --type=mcq
    python manage.py fetch_all_content --type=current_affairs

    # Setup daily scheduled fetch at 2:30 PM:
    python manage.py fetch_all_content --type=both --schedule="14:30"
"""

# QUICK REFERENCE

DASHBOARD_URL = "http://localhost:8000/genai/admin/dashboard/"
ADMIN_LOGS_URL = "http://localhost:8000/admin/genai/processinglog/"

COMMAND_BOTH = "python manage.py fetch_all_content --type=both"
COMMAND_MCQ = "python manage.py fetch_all_content --type=mcq"
COMMAND_CA = "python manage.py fetch_all_content --type=current_affairs"

# STATUS VALUES
STATUSES = {
    'pending': 'Waiting to start',
    'running': 'Currently executing', 
    'completed': 'Successfully finished',
    'failed': 'Encountered error',
}

# TASK TYPES
TASK_TYPES = {
    'mcq_fetch': 'MCQ content fetch',
    'current_affairs_fetch': 'Current Affairs fetch',
    'both': 'Both MCQ & Current Affairs',
}

# FIELDS TO MONITOR
PROGRESS_FIELDS = [
    'processed_items',      # How many items done
    'total_items',          # How many items total
    'success_count',        # Successful items
    'error_count',          # Failed items
    'duration',             # Seconds elapsed
    'mcq_status',          # MCQ operation status
    'current_affairs_status',  # CA operation status
]

# CRON SCHEDULE EXAMPLES
CRON_EXAMPLES = """
# Daily at 2:30 PM (Linux/Mac)
30 14 * * * cd /path/to/project && python manage.py fetch_all_content --type=both

# Twice daily - 8:00 AM and 2:30 PM
0 8,14 * * * cd /path/to/project && python manage.py fetch_all_content --type=both

# Every weekday at 9:00 AM
0 9 * * 1-5 cd /path/to/project && python manage.py fetch_all_content --type=both

# Every 6 hours
0 */6 * * * cd /path/to/project && python manage.py fetch_all_content --type=both
"""

# WINDOWS TASK SCHEDULER
WINDOWS_TASK = """
Program: C:\\path\\to\\python.exe
Arguments: manage.py fetch_all_content --type=both
Working Directory: C:\\path\\to\\project\\django\\django_project
Schedule: Daily at 14:30 (2:30 PM)
"""

if __name__ == '__main__':
    print(__doc__)
    print("\n" + "="*60)
    print("AVAILABLE COMMANDS")
    print("="*60)
    print(f"\n✓ Fetch both: {COMMAND_BOTH}")
    print(f"✓ Fetch MCQ only: {COMMAND_MCQ}")
    print(f"✓ Fetch CA only: {COMMAND_CA}")
    print(f"\n" + "="*60)
    print("DASHBOARD & ADMIN")
    print("="*60)
    print(f"✓ Dashboard: {DASHBOARD_URL}")
    print(f"✓ Admin Logs: {ADMIN_LOGS_URL}")
    print(f"\n" + "="*60)
    print("CRON EXAMPLES (Linux/Mac)")
    print("="*60)
    print(CRON_EXAMPLES)
    print("\n" + "="*60)
    print("WINDOWS TASK SCHEDULER")
    print("="*60)
    print(WINDOWS_TASK)
