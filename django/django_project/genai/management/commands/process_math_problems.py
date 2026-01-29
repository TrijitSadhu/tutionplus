"""
Management command to process pending math problems
Usage: python manage.py process_math_problems
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from genai.models import MathProblemGeneration
from genai.tasks.math_processor import MathMCQGenerator, LaTeXConverter
import json


class Command(BaseCommand):
    help = 'Process pending math problems (LaTeX conversion and MCQ generation)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['latex', 'mcq', 'both'],
            default='both',
            help='Action to perform: latex (LaTeX conversion only), mcq (full MCQ generation), both (default)'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maximum number of items to process (default: 10)'
        )
        parser.add_argument(
            '--status',
            type=str,
            choices=['pending', 'processing', 'failed'],
            default='pending',
            help='Status of items to process (default: pending)'
        )

    def handle(self, *args, **options):
        action = options['action']
        limit = options['limit']
        status_filter = options['status']
        
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write(f"[MATH PROCESSOR] Starting batch processing")
        self.stdout.write(f"Action: {action.upper()}")
        self.stdout.write(f"Status Filter: {status_filter}")
        self.stdout.write(f"Limit: {limit}")
        self.stdout.write(f"{'='*80}\n")
        
        # Get pending items
        queryset = MathProblemGeneration.objects.filter(status=status_filter).order_by('created_at')[:limit]
        
        if not queryset.exists():
            self.stdout.write(self.style.WARNING(f"No {status_filter} math problems found"))
            return
        
        self.stdout.write(f"Found {queryset.count()} item(s) to process\n")
        
        # Initialize processors
        latex_converter = LaTeXConverter()
        mcq_generator = MathMCQGenerator()
        
        success_count = 0
        error_count = 0
        
        for item in queryset:
            try:
                # Validate expression
                if not item.expression or not item.expression.strip():
                    self.stdout.write(self.style.ERROR(f"[{item.id}] No expression provided - SKIPPED"))
                    item.status = 'failed'
                    item.error_message = 'No expression provided'
                    item.processed_at = timezone.now()
                    item.save()
                    error_count += 1
                    continue
                
                # Update status
                item.status = 'processing'
                item.save()
                
                self.stdout.write(f"\n[{item.id}] Processing: {item.expression[:60]}...")
                
                if action == 'latex':
                    # LaTeX conversion only
                    result = latex_converter.convert_to_latex(item.expression)
                    
                    if 'error' in result:
                        item.status = 'failed'
                        item.error_message = f"LaTeX error: {result['error']}"
                        item.processed_at = timezone.now()
                        self.stdout.write(self.style.ERROR(f"  ✗ Failed: {result['error']}"))
                        error_count += 1
                    else:
                        item.latex_output = result.get('latex', '')
                        item.status = 'completed'
                        item.error_message = None
                        item.processed_at = timezone.now()
                        self.stdout.write(self.style.SUCCESS(f"  ✓ LaTeX: {item.latex_output[:50]}..."))
                        success_count += 1
                
                elif action in ['mcq', 'both']:
                    # Full MCQ generation (includes LaTeX)
                    result = mcq_generator.process_math_problem(
                        problem=item.expression,
                        difficulty=item.difficulty
                    )
                    
                    if 'error' in result:
                        item.status = 'failed'
                        item.error_message = f"MCQ error: {result['error']}"
                        item.processed_at = timezone.now()
                        self.stdout.write(self.style.ERROR(f"  ✗ Failed: {result['error']}"))
                        error_count += 1
                    else:
                        # Store LaTeX
                        latex_conversion = result.get('latex_conversion', {})
                        item.latex_output = latex_conversion.get('latex', '')
                        
                        # Store MCQ
                        mcq_data = {
                            'problem_latex': result.get('problem_latex', ''),
                            'question': result.get('question', ''),
                            'option_a': result.get('option_a', ''),
                            'option_b': result.get('option_b', ''),
                            'option_c': result.get('option_c', ''),
                            'option_d': result.get('option_d', ''),
                            'correct_answer': result.get('correct_answer', ''),
                            'explanation': result.get('explanation', ''),
                            'difficulty': result.get('difficulty', item.difficulty),
                            'concepts_tested': result.get('concepts_tested', [])
                        }
                        item.generated_mcqs = json.dumps(mcq_data, indent=2)
                        
                        item.status = 'completed'
                        item.error_message = None
                        item.processed_at = timezone.now()
                        
                        self.stdout.write(self.style.SUCCESS(f"  ✓ LaTeX: {item.latex_output[:40]}..."))
                        self.stdout.write(self.style.SUCCESS(f"  ✓ MCQ: {mcq_data['question'][:40]}..."))
                        success_count += 1
                
                item.save()
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[{item.id}] Unexpected error: {str(e)}"))
                item.status = 'failed'
                item.error_message = f"Unexpected error: {str(e)}"
                item.processed_at = timezone.now()
                item.save()
                error_count += 1
        
        # Summary
        self.stdout.write(f"\n{'='*80}")
        self.stdout.write(self.style.SUCCESS(f"✓ Processed successfully: {success_count}"))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f"✗ Failed: {error_count}"))
        self.stdout.write(f"{'='*80}\n")
