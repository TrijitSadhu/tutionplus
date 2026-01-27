"""
Management command to process pending PDF tasks
Usage: python manage.py process_pdf_tasks
"""

from django.core.management.base import BaseCommand
from genai.tasks.task_router import process_pending_tasks
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Process pending PDF processing tasks'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting PDF task processing...'))
        
        results = process_pending_tasks()
        
        success_count = sum(1 for r in results if r.get('success'))
        failed_count = len(results) - success_count
        
        self.stdout.write(
            self.style.SUCCESS(f'✓ Completed: {success_count} tasks')
        )
        if failed_count > 0:
            self.stdout.write(
                self.style.ERROR(f'✗ Failed: {failed_count} tasks')
            )
