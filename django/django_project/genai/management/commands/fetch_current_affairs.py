"""
Management command to fetch and process current affairs
Usage: python manage.py fetch_current_affairs --type=mcq
"""

from django.core.management.base import BaseCommand
from genai.tasks.current_affairs import fetch_and_process_current_affairs


class Command(BaseCommand):
    help = 'Fetch and process current affairs from configured sources'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='currentaffairs_mcq',
            help='Content type: mcq or descriptive'
        )
    
    def handle(self, *args, **options):
        content_type = options['type']
        
        self.stdout.write(self.style.SUCCESS(f'Fetching current affairs ({content_type})...'))
        
        try:
            result = fetch_and_process_current_affairs(content_type)
            
            self.stdout.write(self.style.SUCCESS(f'✓ Processed {len(result.get("processed_items", []))} items'))
            self.stdout.write(f'Articles scraped: {result.get("articles_scraped", 0)}')
            
            if result.get('errors'):
                self.stdout.write(self.style.WARNING(f'Errors: {len(result["errors"])}'))
                for error in result['errors'][:3]:
                    self.stdout.write(f'  - {error}')
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error: {str(e)}'))
