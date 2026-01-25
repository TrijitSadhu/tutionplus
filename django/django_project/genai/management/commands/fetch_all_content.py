"""
Management command to fetch and process MCQ and Current Affairs
Usage: 
    python manage.py fetch_all_content --type=both
    python manage.py fetch_all_content --type=mcq
    python manage.py fetch_all_content --type=current_affairs
    python manage.py fetch_all_content --type=both --schedule="14:30"
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from genai.models import ProcessingLog, ContentSource
from genai.tasks.current_affairs import fetch_and_process_current_affairs
import json
import logging
from datetime import datetime, time

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch and process MCQ and Current Affairs content'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='both',
            choices=['currentaffairs_mcq', 'currentaffairs_descriptive', 'both'],
            help='Content type to fetch: currentaffairs_mcq, currentaffairs_descriptive, or both'
        )
        parser.add_argument(
            '--schedule',
            type=str,
            default=None,
            help='Schedule for daily run (format: HH:MM, e.g., 14:30)'
        )
        parser.add_argument(
            '--log-id',
            type=int,
            default=None,
            help='Optional ProcessingLog ID to update instead of creating new'
        )
    
    def handle(self, *args, **options):
        content_type = options['type']
        schedule_time = options.get('schedule')
        log_id = options.get('log_id')
        
        print("\n" + "="*70)
        print(f"📋 MANAGEMENT COMMAND STARTED: fetch_all_content")
        print(f"   Content Type: {content_type}")
        print(f"   Schedule Time: {schedule_time}")
        print(f"   Log ID: {log_id}")
        print("="*70)
        
        # Use existing log entry if log_id provided, otherwise create new one
        if log_id:
            try:
                log_entry = ProcessingLog.objects.get(id=log_id)
                print(f"  ✅ Using existing ProcessingLog entry (ID: {log_entry.id})")
            except ProcessingLog.DoesNotExist:
                print(f"  ❌ ProcessingLog with ID {log_id} not found, creating new entry")
                log_entry = ProcessingLog.objects.create(
                    task_type='both' if content_type == 'both' else f'{content_type}_fetch',
                    status='running',
                    started_at=timezone.now(),
                    is_scheduled=bool(schedule_time),
                    scheduled_time=self._parse_schedule(schedule_time) if schedule_time else None
                )
        else:
            # Create new processing log entry
            log_entry = ProcessingLog.objects.create(
                task_type='both' if content_type == 'both' else f'{content_type}_fetch',
                status='running',
                started_at=timezone.now(),
                is_scheduled=bool(schedule_time),
                scheduled_time=self._parse_schedule(schedule_time) if schedule_time else None
            )
            print(f"  ✅ Created new ProcessingLog entry (ID: {log_entry.id})")
        
        self.stdout.write(
            self.style.SUCCESS(f'🚀 Starting fetch task (ID: {log_entry.id})...')
        )
        
        try:
            results = {}
            log_data = {}
            
            # Fetch Current Affairs MCQ
            if content_type in ['currentaffairs_mcq', 'both']:
                self.stdout.write('📖 Fetching Current Affairs MCQ content...')
                print(f"  📞 Calling fetch_and_process_current_affairs('currentaffairs_mcq')...")
                try:
                    mcq_result = fetch_and_process_current_affairs('currentaffairs_mcq')
                    print(f"  ✅ MCQ processing completed, result: {mcq_result}")
                    results['currentaffairs_mcq'] = mcq_result
                    log_entry.mcq_status = '✓ Completed'
                    processed_count = len(mcq_result.get('processed_items', []))
                    log_entry.success_count += processed_count
                    log_data['currentaffairs_mcq'] = mcq_result
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ MCQ: {processed_count} items processed')
                    )
                except Exception as e:
                    print(f"  ❌ ERROR in MCQ fetch: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    log_entry.mcq_status = f'✗ Failed: {str(e)}'
                    log_entry.error_count += 1
                    logger.error(f"MCQ fetch error: {e}")
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ MCQ Error: {str(e)}')
                    )
            
            # Fetch Current Affairs Descriptive
            if content_type in ['currentaffairs_descriptive', 'both']:
                self.stdout.write('📰 Fetching Current Affairs Descriptive content...')
                print(f"  📞 Calling fetch_and_process_current_affairs('currentaffairs_descriptive')...")
                try:
                    ca_result = fetch_and_process_current_affairs('currentaffairs_descriptive')
                    print(f"  ✅ Descriptive processing completed, result: {ca_result}")
                    results['currentaffairs_descriptive'] = ca_result
                    log_entry.current_affairs_status = '✓ Completed'
                    processed_count = len(ca_result.get('processed_items', []))
                    log_entry.success_count += processed_count
                    log_data['currentaffairs_descriptive'] = ca_result
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Current Affairs: {processed_count} items processed')
                    )
                except Exception as e:
                    print(f"  ❌ ERROR in Descriptive fetch: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    log_entry.current_affairs_status = f'✗ Failed: {str(e)}'
                    log_entry.error_count += 1
                    logger.error(f"Current Affairs fetch error: {e}")
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Current Affairs Error: {str(e)}')
                    )
            
            # Update log entry
            log_entry.status = 'completed'
            log_entry.completed_at = timezone.now()
            log_entry.log_details = json.dumps(log_data, default=str)
            log_entry.processed_items = log_entry.success_count
            log_entry.save()
            
            duration = (log_entry.completed_at - log_entry.started_at).total_seconds()
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Task completed in {duration:.2f}s')
            )
            self.stdout.write(
                self.style.SUCCESS(f'   Success: {log_entry.success_count} | Errors: {log_entry.error_count}')
            )
            
        except Exception as e:
            print(f"\n❌ OUTER EXCEPTION in fetch_all_content: {str(e)}")
            import traceback
            traceback.print_exc()
            log_entry.status = 'failed'
            log_entry.error_message = str(e)
            log_entry.completed_at = timezone.now()
            log_entry.save()
            
            logger.error(f"Task failed: {e}")
            self.stdout.write(
                self.style.ERROR(f'\n❌ Task failed: {str(e)}')
            )
    
    def _parse_schedule(self, schedule_str):
        """Parse schedule string (HH:MM) into datetime object"""
        if not schedule_str:
            return None
        try:
            hour, minute = map(int, schedule_str.split(':'))
            today = timezone.now().date()
            return timezone.make_aware(
                datetime.combine(today, time(hour, minute))
            )
        except (ValueError, TypeError):
            self.stdout.write(
                self.style.WARNING(f'Invalid schedule format: {schedule_str}. Use HH:MM')
            )
            return None
    
    def get_active_sources(self, source_type):
        """Get active content sources from database"""
        sources = ContentSource.objects.filter(
            source_type=source_type,
            is_active=True
        ).values_list('url', flat=True)
        
        if not sources:
            self.stdout.write(
                self.style.WARNING(f'No active {source_type} sources found in database')
            )
            return []
        
        return list(sources)
