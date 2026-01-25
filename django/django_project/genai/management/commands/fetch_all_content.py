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
            choices=['mcq', 'current_affairs', 'both'],
            help='Content type to fetch: mcq, current_affairs, or both'
        )
        parser.add_argument(
            '--schedule',
            type=str,
            default=None,
            help='Schedule for daily run (format: HH:MM, e.g., 14:30)'
        )
    
    def handle(self, *args, **options):
        content_type = options['type']
        schedule_time = options.get('schedule')
        
        # Create processing log entry
        log_entry = ProcessingLog.objects.create(
            task_type='both' if content_type == 'both' else f'{content_type}_fetch',
            status='running',
            started_at=timezone.now(),
            is_scheduled=bool(schedule_time),
            scheduled_time=self._parse_schedule(schedule_time) if schedule_time else None
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'🚀 Starting fetch task (ID: {log_entry.id})...')
        )
        
        try:
            results = {}
            log_data = {}
            
            # Fetch MCQ
            if content_type in ['mcq', 'both']:
                self.stdout.write('📖 Fetching MCQ content...')
                try:
                    mcq_result = fetch_and_process_current_affairs('mcq')
                    results['mcq'] = mcq_result
                    log_entry.mcq_status = '✓ Completed'
                    log_entry.success_count += mcq_result.get('processed_count', 0)
                    log_data['mcq'] = mcq_result
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ MCQ: {mcq_result.get("processed_count", 0)} items processed')
                    )
                except Exception as e:
                    log_entry.mcq_status = f'✗ Failed: {str(e)}'
                    log_entry.error_count += 1
                    logger.error(f"MCQ fetch error: {e}")
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ MCQ Error: {str(e)}')
                    )
            
            # Fetch Current Affairs
            if content_type in ['current_affairs', 'both']:
                self.stdout.write('📰 Fetching Current Affairs content...')
                try:
                    ca_result = fetch_and_process_current_affairs('descriptive')
                    results['current_affairs'] = ca_result
                    log_entry.current_affairs_status = '✓ Completed'
                    log_entry.success_count += ca_result.get('processed_count', 0)
                    log_data['current_affairs'] = ca_result
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Current Affairs: {ca_result.get("processed_count", 0)} items processed')
                    )
                except Exception as e:
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
