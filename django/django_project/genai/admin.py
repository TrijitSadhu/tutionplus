import json
import logging
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import reverse, path
from django.db.models import Q
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from bank.admin import admin_site
from .models import PDFUpload, CurrentAffairsGeneration, MathProblemGeneration, ProcessingTask, ProcessingLog, ContentSource, LLMPrompt, JobFetch, JsonImport
from .bulk_import import BulkImporter
from genai.tasks.job_scraper import run_job_fetch


logger = logging.getLogger(__name__)


class ProcessPDFForm(forms.Form):
    """Form for selecting chapter, difficulty, and other options before processing PDF"""
    
    CHAPTER_CHOICES = [
        ('', '-- Select Chapter --'),
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
        ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
        ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'),
        ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'),
        ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'),
        ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'),
        ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'),
        ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'),
        ('41', '41'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('', '-- Select Difficulty --'),
        ('easy', 'Easy (Simple, straightforward questions)'),
        ('medium', 'Medium (Standard difficulty)'),
        ('hard', 'Hard (UPSC Civil Services level)'),
    ]
    
    chapter = forms.ChoiceField(
        choices=CHAPTER_CHOICES,
        required=False,
        label='Chapter (Optional)',
        help_text='Leave blank to not filter by chapter'
    )
    
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        label='Difficulty Level (Required)',
        help_text='Select difficulty level - Easy, Medium, or Hard'
    )
    
    extract_all = forms.BooleanField(
        required=False,
        initial=False,
        label='Extract ALL MCQs from PDF',
        help_text='Check this to extract ALL MCQs from the PDF (ignores Number of MCQs field)'
    )
    
    num_items = forms.IntegerField(
        initial=5,
        min_value=1,
        required=False,
        label='Number of MCQs to Generate',
        help_text='Enter any number of MCQs to generate (ignored if "Extract ALL" is checked)'
    )
    
    page_from = forms.IntegerField(
        initial=0,
        min_value=0,
        required=False,
        label='Page From (Optional)',
        help_text='Start page number (0 for beginning). Leave blank for full PDF',
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '0'})
    )
    
    page_to = forms.IntegerField(
        initial=None,
        min_value=0,
        required=False,
        label='Page To (Optional)',
        help_text='End page number (inclusive). Leave blank for end of PDF',
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '0'})
    )
    
    # NEW: Processing type selector (Subject-based, CA MCQ, or CA Descriptive)
    processing_type = forms.ChoiceField(
        choices=[
            ('subject_mcq', 'Subject-based MCQ (Polity, Economics, etc.)'),
            ('ca_mcq', 'Current Affairs MCQ'),
            ('ca_descriptive', 'Current Affairs Descriptive'),
        ],
        initial='subject_mcq',
        label='Processing Type',
        help_text='Choose what type of content to generate',
        widget=forms.RadioSelect()
    )
    
    # Current Affairs specific fields
    ca_date = forms.DateField(
        required=False,
        label='Date (Optional - leave blank for today)',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Only used for Current Affairs'
    )
    
    ca_year = forms.ChoiceField(
        choices=[('', '-- Select Year --'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028')],
        required=False,
        label='Year',
        help_text='Only used for Current Affairs'
    )
    
    ca_auto_date = forms.BooleanField(
        required=False,
        initial=False,
        label='Let LLM Decide Date and Year',
        help_text='If checked, LLM will extract/decide date and year from content'
    )
    
    def clean(self):
        """Custom validation to handle page_to value properly"""
        cleaned_data = super().clean()
        
        # Debug: Print POST data to see what was actually submitted
        print(f"[FORM CLEAN] Raw POST data keys: {list(self.data.keys())}")
        print(f"[FORM CLEAN] page_to in POST: {'page_to' in self.data}")
        if 'page_to' in self.data:
            print(f"[FORM CLEAN] page_to POST value: '{self.data.get('page_to')}'")
            print(f"[FORM CLEAN] page_to POST value type: {type(self.data.get('page_to'))}")
        
        # Handle page_to: if empty or None, set it to page_from (single page extraction)
        page_from = cleaned_data.get('page_from')
        page_to = cleaned_data.get('page_to')
        
        # If page_to is None (empty), default it to page_from for single page extraction
        if page_to is None:
            cleaned_data['page_to'] = page_from
            print(f"[FORM CLEAN] page_to was None, set to page_from: {page_from}")
        
        return cleaned_data

class PDFUploadAdmin(admin.ModelAdmin):
    """Admin interface for PDF uploads with processing actions"""
    
    list_display = ('title', 'subject', 'status_badge', 'total_pages', 'uploaded_at', 'uploaded_by')
    list_filter = ('subject', 'status', 'uploaded_at')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at', 'total_pages', 'extracted_text')
    
    fieldsets = (
        ('PDF Information', {
            'fields': ('title', 'subject', 'pdf_file', 'description', 'uploaded_by')
        }),
        ('Processing Details', {
            'fields': ('status', 'total_pages', 'extracted_text')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['process_pdf_bulk']
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'uploaded': '#FFA500',
            'processing': '#FF6B6B',
            'completed': '#51CF66',
            'failed': '#C92A2A',
        }
        color = colors.get(obj.status, '#999999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def process_pdf_bulk(self, request, queryset):
        """Show form to select processing options (mode, date, year, etc.)"""
        
        if queryset.count() == 0:
            self.message_user(request, "Please select at least one PDF", level='error')
            return
        
        # Store selected PDF IDs in session
        request.session['pdf_ids'] = list(queryset.values_list('id', flat=True))
        request.session['process_type'] = 'bulk'
        
        # Redirect to form where user selects processing mode
        return redirect('/genai/process-pdf-form/')
    
    process_pdf_bulk.short_description = "⚙️ Process (Bulk) - Choose Type & Options"


class CurrentAffairsGenerationAdmin(admin.ModelAdmin):
    """Admin interface for current affairs generation"""
    
    list_display = ('topic', 'status_badge', 'created_at', 'has_mcq', 'has_descriptive')
    list_filter = ('status', 'created_at')
    search_fields = ('topic', 'source_url')
    readonly_fields = ('created_at', 'processed_at')
    
    fieldsets = (
        ('Input Information', {
            'fields': ('topic', 'source_url')
        }),
        ('Processing Status', {
            'fields': ('status', 'created_at', 'processed_at', 'error_message')
        }),
        ('Generated Content', {
            'fields': ('generated_mcq', 'generated_descriptive'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['generate_mcq', 'generate_descriptive']
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'processing': '#FF6B6B',
            'completed': '#51CF66',
            'failed': '#C92A2A',
        }
        color = colors.get(obj.status, '#999999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def has_mcq(self, obj):
        return '✓' if obj.generated_mcq else '✗'
    has_mcq.short_description = 'MCQ Generated'
    
    def has_descriptive(self, obj):
        return '✓' if obj.generated_descriptive else '✗'
    has_descriptive.short_description = 'Descriptive Generated'
    
    def generate_mcq(self, request, queryset):
        for item in queryset:
            item.status = 'processing'
            item.save()
        self.message_user(request, f"Started MCQ generation for {queryset.count()} item(s)")
    generate_mcq.short_description = "Generate MCQ for selected items"
    
    def generate_descriptive(self, request, queryset):
        for item in queryset:
            item.status = 'processing'
            item.save()
        self.message_user(request, f"Started descriptive generation for {queryset.count()} item(s)")
    generate_descriptive.short_description = "Generate descriptive for selected items"


class MathProblemGenerationAdmin(admin.ModelAdmin):
    """Admin interface for math problem generation"""
    
    list_display = ('expression_preview', 'chapter', 'difficulty', 'status_badge', 'has_pdf', 'has_latex', 'has_mcqs', 'processed_at', 'go_button', 'created_at')
    list_filter = ('difficulty', 'status', 'created_at', 'chapter')
    search_fields = ('expression', 'chapter', 'error_message')
    readonly_fields = ('created_at', 'processed_at', 'latex_output', 'generated_mcqs')
    
    fieldsets = (
        ('Math Input', {
            'fields': ('expression', 'difficulty', 'chapter', 'pdf_file')
        }),
        ('Processing Status', {
            'fields': ('status', 'created_at', 'processed_at', 'error_message')
        }),
        ('Generated Output', {
            'fields': ('latex_output', 'generated_mcqs'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['convert_to_latex', 'generate_math_mcqs']
    
    def get_form(self, request, obj=None, **kwargs):
        """Dynamically populate chapter choices"""
        form = super().get_form(request, obj, **kwargs)
        if 'chapter' in form.base_fields:
            from genai.models import MathProblemGeneration
            chapter_choices = MathProblemGeneration.get_chapter_choices()
            form.base_fields['chapter'].widget = forms.Select(choices=[('', '-------')] + chapter_choices)
        return form
    
    def expression_preview(self, obj):
        if not obj.expression:
            return '(No expression)'
        preview = obj.expression[:50] + '...' if len(obj.expression) > 50 else obj.expression
        return preview
    expression_preview.short_description = 'Expression'
    
    def has_pdf(self, obj):
        if obj.pdf_file:
            return format_html('<span style="color: green;">✓ PDF</span>')
        return format_html('<span style="color: gray;">✗</span>')
    has_pdf.short_description = 'PDF'
    
    def has_mcqs(self, obj):
        if obj.generated_mcqs:
            return format_html('<span style="color: green;">✓ MCQs</span>')
        return format_html('<span style="color: gray;">✗</span>')
    has_mcqs.short_description = 'MCQs'
    
    def go_button(self, obj):
        """Per-row GO button with dropdown menu for actions"""
        from django.urls import reverse
        from django.utils.safestring import mark_safe
        
        # URL for Generate MCQ (PDF Processing Form)
        mcq_url = reverse('genai:math_pdf_processing_form', args=[obj.pk])
        
        # URL for Convert to LaTeX (also uses math_pdf_processing_form)
        latex_url = reverse('genai:math_pdf_processing_form', args=[obj.pk])
        
        # Create dropdown button using string concatenation
        html = (
            '<div class="dropdown" style="position: relative; display: inline-block;">'
            '<button class="button" style="background: #417690; color: white; padding: 5px 15px; '
            'text-decoration: none; border-radius: 3px; cursor: pointer; border: none;" '
            'onclick="event.preventDefault(); this.nextElementSibling.style.display = this.nextElementSibling.style.display === \'block\' ? \'none\' : \'block\';">'
            'GO ▼'
            '</button>'
            '<div style="display: none; position: absolute; background: white; min-width: 200px; '
            'box-shadow: 0px 8px 16px rgba(0,0,0,0.2); z-index: 1000; border-radius: 3px; margin-top: 2px;">'
            '<a href="' + mcq_url + '" style="color: black; padding: 12px 16px; text-decoration: none; '
            'display: block; border-bottom: 1px solid #eee;" '
            'onmouseover="this.style.backgroundColor=\'#f1f1f1\'" '
            'onmouseout="this.style.backgroundColor=\'white\'">'
            '📝 Generate MCQ'
            '</a>'
            '<a href="' + latex_url + '" '
            'style="color: black; padding: 12px 16px; text-decoration: none; display: block;" '
            'onmouseover="this.style.backgroundColor=\'#f1f1f1\'" '
            'onmouseout="this.style.backgroundColor=\'white\'">'
            '🔤 Convert to LaTeX'
            '</a>'
            '</div>'
            '</div>'
            '<script>'
            'document.addEventListener("click", function(e) {'
            'var dropdowns = document.querySelectorAll(".dropdown > div");'
            'dropdowns.forEach(function(dropdown) {'
            'if (!dropdown.previousElementSibling.contains(e.target) && !dropdown.contains(e.target)) {'
            'dropdown.style.display = "none";'
            '}'
            '});'
            '});'
            '</script>'
        )
        
        return mark_safe(html)
    go_button.short_description = 'Action'
    go_button.allow_tags = True
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'processing': '#FF6B6B',
            'completed': '#51CF66',
            'failed': '#C92A2A',
        }
        color = colors.get(obj.status, '#999999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def has_latex(self, obj):
        return '✓' if obj.latex_output else '✗'
    has_latex.short_description = 'LaTeX Done'
    
    def convert_to_latex(self, request, queryset):
        """Convert math expressions to LaTeX format"""
        from genai.tasks.math_processor import LaTeXConverter
        from django.utils import timezone
        import json
        
        converter = LaTeXConverter()
        success_count = 0
        error_count = 0
        
        for item in queryset:
            try:
                # Validate expression exists
                if not item.expression or not item.expression.strip():
                    item.status = 'failed'
                    item.error_message = 'No expression provided for conversion'
                    item.save()
                    error_count += 1
                    continue
                
                # Update status to processing
                item.status = 'processing'
                item.save()
                
                print(f"\n{'='*80}")
                print(f"[LATEX CONVERSION] Processing: {item.expression[:50]}...")
                print(f"{'='*80}")
                
                # Perform conversion
                result = converter.convert_to_latex(item.expression)
                
                if 'error' in result:
                    # Conversion failed
                    item.status = 'failed'
                    item.error_message = f"LaTeX conversion error: {result['error']}"
                    item.processed_at = timezone.now()
                    print(f"❌ Conversion failed: {result['error']}")
                    error_count += 1
                else:
                    # Conversion succeeded
                    item.latex_output = result.get('latex', '')
                    item.status = 'completed'
                    item.error_message = None
                    item.processed_at = timezone.now()
                    print(f"✅ Conversion successful: {item.latex_output[:50]}...")
                    success_count += 1
                
                item.save()
                print(f"{'='*80}\n")
                
            except Exception as e:
                # Handle unexpected errors
                item.status = 'failed'
                item.error_message = f"Unexpected error: {str(e)}"
                item.processed_at = timezone.now()
                item.save()
                error_count += 1
                print(f"❌ Unexpected error processing {item.id}: {str(e)}\n")
        
        # Show summary message
        if success_count > 0 and error_count == 0:
            self.message_user(request, f"✅ Successfully converted {success_count} item(s) to LaTeX", level='SUCCESS')
        elif success_count > 0 and error_count > 0:
            self.message_user(request, f"⚠️ Converted {success_count} item(s), {error_count} failed", level='WARNING')
        else:
            self.message_user(request, f"❌ All {error_count} conversion(s) failed", level='ERROR')
    
    convert_to_latex.short_description = "Convert to LaTeX"
    
    def generate_math_mcqs(self, request, queryset):
        """Generate MCQs from math problems (includes LaTeX conversion if needed)"""
        from genai.tasks.math_processor import MathMCQGenerator
        from django.utils import timezone
        import json
        
        generator = MathMCQGenerator()
        success_count = 0
        error_count = 0
        
        for item in queryset:
            try:
                # Validate expression exists
                if not item.expression or not item.expression.strip():
                    item.status = 'failed'
                    item.error_message = 'No expression provided for MCQ generation'
                    item.save()
                    error_count += 1
                    continue
                
                # Update status to processing
                item.status = 'processing'
                item.save()
                
                print(f"\n{'='*80}")
                print(f"[MCQ GENERATION] Processing: {item.expression[:50]}...")
                print(f"Difficulty: {item.difficulty}")
                print(f"{'='*80}")
                
                # Process problem (includes LaTeX conversion + MCQ generation)
                result = generator.process_math_problem(
                    problem=item.expression,
                    difficulty=item.difficulty
                )
                
                if 'error' in result:
                    # Generation failed
                    item.status = 'failed'
                    item.error_message = f"MCQ generation error: {result['error']}"
                    item.processed_at = timezone.now()
                    print(f"❌ Generation failed: {result['error']}")
                    error_count += 1
                else:
                    # Generation succeeded
                    # Store LaTeX output
                    latex_conversion = result.get('latex_conversion', {})
                    item.latex_output = latex_conversion.get('latex', '')
                    
                    # Store MCQ data as JSON
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
                    
                    print(f"✅ MCQ generated successfully")
                    print(f"   LaTeX: {item.latex_output[:50]}...")
                    print(f"   Question: {mcq_data['question'][:50]}...")
                    success_count += 1
                
                item.save()
                print(f"{'='*80}\n")
                
            except Exception as e:
                # Handle unexpected errors
                item.status = 'failed'
                item.error_message = f"Unexpected error: {str(e)}"
                item.processed_at = timezone.now()
                item.save()
                error_count += 1
                print(f"❌ Unexpected error processing {item.id}: {str(e)}\n")
        
        # Show summary message
        if success_count > 0 and error_count == 0:
            self.message_user(request, f"✅ Successfully generated {success_count} MCQ(s)", level='SUCCESS')
        elif success_count > 0 and error_count > 0:
            self.message_user(request, f"⚠️ Generated {success_count} MCQ(s), {error_count} failed", level='WARNING')
        else:
            self.message_user(request, f"❌ All {error_count} generation(s) failed", level='ERROR')
    
    generate_math_mcqs.short_description = "Generate MCQs for selected items"


class ProcessingTaskAdmin(admin.ModelAdmin):
    """Admin interface for processing tasks"""
    
    list_display = ('task_type_display', 'status_badge', 'created_at', 'completed_at', 'duration')
    list_filter = ('task_type', 'status', 'created_at')
    search_fields = ('task_type',)
    readonly_fields = ('created_at', 'started_at', 'completed_at')
    
    fieldsets = (
        ('Task Information', {
            'fields': ('task_type', 'status', 'pdf_upload', 'created_by')
        }),
        ('Timing', {
            'fields': ('created_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('input_data', 'output_data', 'error_message'),
            'classes': ('collapse',)
        }),
    )
    
    def task_type_display(self, obj):
        return obj.get_task_type_display()
    task_type_display.short_description = 'Task Type'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'processing': '#FF6B6B',
            'completed': '#51CF66',
            'failed': '#C92A2A',
        }
        color = colors.get(obj.status, '#999999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def duration(self, obj):
        if obj.started_at and obj.completed_at:
            delta = obj.completed_at - obj.started_at
            return f"{delta.total_seconds():.2f}s"
        return "—"
    duration.short_description = 'Duration'


class ProcessingLogAdmin(admin.ModelAdmin):
    """Admin interface for Processing Logs with status tracking and task routing"""
    
    list_display = ('id', 'task_type_display', 'subject_display', 'status_badge', 'difficulty_display', 'num_items', 'duration_display', 'created_at')
    list_filter = ('status', 'task_type', 'subject', 'difficulty_level', 'created_at', 'skip_scraping', 'send_url_directly', 'use_playwright')
    search_fields = ('id', 'mcq_status', 'current_affairs_status')
    readonly_fields = ('id', 'created_at', 'updated_at', 'started_at', 'completed_at', 'duration_display', 'progress_percentage_display', 'log_details_formatted')
    
    fieldsets = (
        ('Task Information', {
            'fields': ('id', 'task_type', 'status', 'created_by', 'pdf_upload')
        }),
        ('Subject Routing (NEW)', {
            'fields': ('subject', 'difficulty_level', 'output_format', 'num_items'),
            'description': 'Controls how the task is routed and processed'
        }),
        ('PDF Processing Options', {
            'fields': ('start_page', 'end_page'),
            'description': 'Optional: Process specific page range'
        }),
        ('Timing', {
            'fields': ('created_at', 'updated_at', 'started_at', 'completed_at', 'duration_display'),
            'classes': ('collapse',)
        }),
        ('Progress Tracking', {
            'fields': ('total_items', 'processed_items', 'success_count', 'error_count', 'progress_percentage_display')
        }),
        ('Status Details', {
            'fields': ('mcq_status', 'current_affairs_status', 'error_message')
        }),
        ('Processing Options', {
            'fields': ('skip_scraping', 'send_url_directly', 'use_playwright'),
            'description': 'skip_scraping: Download content before sending to LLM | send_url_directly: Send URL only (takes precedence) | use_playwright: It\'s a separate download engine'
        }),
        ('Scheduling', {
            'fields': ('is_scheduled', 'scheduled_time'),
            'classes': ('collapse',)
        }),
        ('Log Details', {
            'fields': ('log_details_formatted',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_completed', 'mark_failed', 'clear_error', 'trigger_fetch_both', 'trigger_fetch_mcq', 'trigger_fetch_ca', 'generate_mcq_from_pdf', 'generate_ca_from_pdf']
    
    def task_type_display(self, obj):
        return obj.get_task_type_display()
    task_type_display.short_description = 'Task Type'
    
    def subject_display(self, obj):
        if obj.subject:
            return obj.get_subject_display() if hasattr(obj, 'get_subject_display') else obj.subject
        return '-'
    subject_display.short_description = 'Subject'
    
    def difficulty_display(self, obj):
        if obj.difficulty_level:
            return f"⭐ {obj.difficulty_level}"
        return '-'
    difficulty_display.short_description = 'Difficulty'
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'pending': '#FFA500',
            'running': '#FF6B6B',
            'completed': '#51CF66',
            'failed': '#C92A2A',
        }
        color = colors.get(obj.status, '#999999')
        emoji = {'pending': '⏳', 'running': '⚙️', 'completed': '✅', 'failed': '❌'}.get(obj.status, '❓')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{} {}</span>',
            color,
            emoji,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def progress_bar(self, obj):
        """Display progress as HTML bar"""
        if obj.total_items == 0:
            percentage = 0
        else:
            percentage = obj.progress_percentage
        
        bar_color = '#51CF66' if percentage == 100 else '#4DABF7' if percentage > 50 else '#FFD43B'
        
        return format_html(
            '<div style="width: 100%; background-color: #e0e0e0; border-radius: 3px; height: 20px; position: relative;">'
            '<div style="width: {}%; background-color: {}; height: 20px; border-radius: 3px; display: flex; align-items: center; justify-content: center;">'
            '<span style="color: white; font-size: 12px; font-weight: bold;">{}/{}' 
            '</span></div></div>',
            percentage,
            bar_color,
            obj.processed_items,
            obj.total_items
        )
    progress_bar.short_description = 'Progress'
    
    def duration_display(self, obj):
        """Display task duration"""
        if obj.duration is None:
            return "-"
        minutes, seconds = divmod(int(obj.duration), 60)
        if minutes > 0:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"
    duration_display.short_description = 'Duration'
    
    def progress_percentage_display(self, obj):
        """Display progress percentage"""
        return f"{obj.progress_percentage}%"
    progress_percentage_display.short_description = 'Progress %'
    
    def log_details_formatted(self, obj):
        """Display log details as formatted JSON"""
        if not obj.log_details:
            return "No log details available"
        try:
            import json
            formatted = json.dumps(json.loads(obj.log_details), indent=2)
            return format_html('<pre style="background-color: #f5f5f5; padding: 10px; border-radius: 3px; overflow: auto;">{}</pre>', formatted)
        except:
            return obj.log_details
    log_details_formatted.short_description = 'Log Details'
    
    def admin_action_buttons(self, obj):
        """Show quick action buttons in list view"""
        status_url = reverse('genai:task_status', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">View Status</a>',
            status_url
        )
    admin_action_buttons.short_description = 'Actions'
    
    def mark_completed(self, request, queryset):
        """Mark selected tasks as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f"✅ Marked {updated} task(s) as completed")
    mark_completed.short_description = "✅ Mark selected as completed"
    
    def mark_failed(self, request, queryset):
        """Mark selected tasks as failed"""
        updated = queryset.update(status='failed')
        self.message_user(request, f"❌ Marked {updated} task(s) as failed")
    mark_failed.short_description = "❌ Mark selected as failed"
    
    def clear_error(self, request, queryset):
        """Clear error messages"""
        updated = queryset.update(error_message='')
        self.message_user(request, f"✓ Cleared errors for {updated} task(s)")
    clear_error.short_description = "✓ Clear error messages"
    
    def trigger_fetch_both(self, request, queryset):
        """Trigger fetch for both MCQ and Current Affairs"""
        print("\n" + "="*70)
        print("🎬 ADMIN ACTION TRIGGERED: trigger_fetch_both()")
        print(f"   Selected ProcessingLog entries: {queryset.count()}")
        print("="*70)
        
        # Update all selected ProcessingLog entries to 'running' status
        for log_entry in queryset:
            print(f"  📝 Updating ProcessingLog ID {log_entry.id} to 'running' status")
            log_entry.status = 'running'
            log_entry.started_at = timezone.now()
            log_entry.save()
        
        try:
            print(f"  📞 Calling management command: fetch_all_content (type='both')")
            call_command('fetch_all_content', type='both', log_id=queryset.first().id if queryset.exists() else None)
            print(f"  ✅ Command completed successfully")
            self.message_user(request, f"🚀 Started: Fetch Both MCQ & Current Affairs (Updated {queryset.count()} task(s))")
        except CommandError as e:
            print(f"  ❌ CommandError: {str(e)}")
            queryset.update(status='failed', error_message=str(e))
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
            queryset.update(status='failed', error_message=str(e))
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
    trigger_fetch_both.short_description = "🚀 Fetch Both (MCQ & Current Affairs)"
    
    def trigger_fetch_mcq(self, request, queryset):
        """Trigger fetch for Current Affairs MCQ only"""
        print("\n" + "="*70)
        print("🎬 ADMIN ACTION TRIGGERED: trigger_fetch_mcq()")
        print(f"   Selected ProcessingLog entries: {queryset.count()}")
        print("="*70)
        
        # Update all selected ProcessingLog entries to 'running' status
        for log_entry in queryset:
            print(f"  📝 Updating ProcessingLog ID {log_entry.id} to 'running' status")
            log_entry.status = 'running'
            log_entry.started_at = timezone.now()
            log_entry.save()
        
        try:
            print(f"  📞 Calling management command: fetch_all_content (type='currentaffairs_mcq')")
            call_command('fetch_all_content', type='currentaffairs_mcq', log_id=queryset.first().id if queryset.exists() else None)
            print(f"  ✅ Command completed successfully")
            self.message_user(request, f"📖 Started: Fetch Current Affairs MCQ (Updated {queryset.count()} task(s))")
        except CommandError as e:
            print(f"  ❌ CommandError: {str(e)}")
            # Mark as failed on error
            queryset.update(status='failed', error_message=str(e))
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
            queryset.update(status='failed', error_message=str(e))
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
    trigger_fetch_mcq.short_description = "📖 Fetch Current Affairs MCQ"
    
    def trigger_fetch_ca(self, request, queryset):
        """Trigger fetch for Current Affairs Descriptive only"""
        print("\n" + "="*70)
        print("🎬 ADMIN ACTION TRIGGERED: trigger_fetch_ca()")
        print(f"   Selected ProcessingLog entries: {queryset.count()}")
        print("="*70)
        
        # Update all selected ProcessingLog entries to 'running' status
        for log_entry in queryset:
            print(f"  📝 Updating ProcessingLog ID {log_entry.id} to 'running' status")
            log_entry.status = 'running'
            log_entry.started_at = timezone.now()
            log_entry.save()
        
        try:
            print(f"  📞 Calling management command: fetch_all_content (type='currentaffairs_descriptive')")
            call_command('fetch_all_content', type='currentaffairs_descriptive', log_id=queryset.first().id if queryset.exists() else None)
            print(f"  ✅ Command completed successfully")
            self.message_user(request, f"📰 Started: Fetch Current Affairs Descriptive (Updated {queryset.count()} task(s))")
        except CommandError as e:
            print(f"  ❌ CommandError: {str(e)}")
            queryset.update(status='failed', error_message=str(e))
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
        except Exception as e:
            print(f"  ❌ Exception: {str(e)}")
            queryset.update(status='failed', error_message=str(e))
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
    trigger_fetch_ca.short_description = "📰 Fetch Current Affairs Descriptive"
    
    def generate_mcq_from_pdf(self, request, queryset):
        """Generate MCQ from PDF file"""
        if not request.FILES:
            self.message_user(request, "❌ Please upload a PDF file", level='ERROR')
            return
        
        try:
            uploaded_file = request.FILES.get('pdf_file')
            if not uploaded_file:
                self.message_user(request, "❌ No PDF file provided", level='ERROR')
                return
            
            # Create PDFUpload record
            pdf_upload = PDFUpload.objects.create(
                title=uploaded_file.name,
                pdf_file=uploaded_file,
                subject='genai',
                uploaded_by=request.user,
                status='processing'
            )
            
            # Create processing log
            log_entry = ProcessingLog.objects.create(
                task_type='pdf_currentaffairs_mcq',
                status='running',
                pdf_upload=pdf_upload,
                started_at=timezone.now()
            )
            
            # Call processing command
            call_command('process_pdf_content', pdf_id=pdf_upload.id, content_type='currentaffairs_mcq')
            
            self.message_user(request, f"📄 Started: Generate Current Affairs MCQ from PDF (Task ID: {log_entry.id})")
        except Exception as e:
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
    generate_mcq_from_pdf.short_description = "📄 Generate Current Affairs MCQ from PDF"
    
    def generate_ca_from_pdf(self, request, queryset):
        """Generate Current Affairs from PDF file"""
        if not request.FILES:
            self.message_user(request, "❌ Please upload a PDF file", level='ERROR')
            return
        
        try:
            uploaded_file = request.FILES.get('pdf_file')
            if not uploaded_file:
                self.message_user(request, "❌ No PDF file provided", level='ERROR')
                return
            
            # Create PDFUpload record
            pdf_upload = PDFUpload.objects.create(
                title=uploaded_file.name,
                pdf_file=uploaded_file,
                subject='genai',
                uploaded_by=request.user,
                status='processing'
            )
            
            # Create processing log
            log_entry = ProcessingLog.objects.create(
                task_type='pdf_currentaffairs_descriptive',
                status='running',
                pdf_upload=pdf_upload,
                started_at=timezone.now()
            )
            
            # Call processing command
            call_command('process_pdf_content', pdf_id=pdf_upload.id, content_type='currentaffairs_descriptive')
            
            self.message_user(request, f"📋 Started: Generate Current Affairs Descriptive from PDF (Task ID: {log_entry.id})")
        except Exception as e:
            self.message_user(request, f"❌ Error: {str(e)}", level='ERROR')
    generate_ca_from_pdf.short_description = "📋 Generate Current Affairs Descriptive from PDF"


class ContentSourceAdmin(admin.ModelAdmin):
    """Admin interface for managing content sources"""
    
    list_display = ('name', 'source_type_display', 'content_date', 'url_preview', 'is_active_badge', 'created_at')
    list_filter = ('source_type', 'is_active', 'created_at')
    search_fields = ('name', 'url', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Source Information', {
            'fields': ('name', 'source_type', 'url', 'description', 'content_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_sources', 'deactivate_sources']
    
    def source_type_display(self, obj):
        """Display source type with icon"""
        icons = {
            'currentaffairs_mcq': '📖',
            'currentaffairs_descriptive': '📰'
        }
        icon = icons.get(obj.source_type, '🔗')
        return f"{icon} {obj.get_source_type_display()}"
    source_type_display.short_description = 'Type'
    
    def url_preview(self, obj):
        """Display URL with link"""
        return format_html(
            '<a href="{}" target="_blank" style="word-break: break-all;">{}</a>',
            obj.url,
            obj.url[:50] + '...' if len(obj.url) > 50 else obj.url
        )
    url_preview.short_description = 'URL'
    
    def is_active_badge(self, obj):
        """Display active status as badge"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: #51CF66; color: white; padding: 5px 10px; border-radius: 3px;">✅ Active</span>'
            )
        return format_html(
            '<span style="background-color: #C92A2A; color: white; padding: 5px 10px; border-radius: 3px;">❌ Inactive</span>'
        )
    is_active_badge.short_description = 'Status'
    
    def activate_sources(self, request, queryset):
        """Activate selected sources"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"✅ Activated {updated} source(s)")
    activate_sources.short_description = "✅ Activate selected sources"
    
    def deactivate_sources(self, request, queryset):
        """Deactivate selected sources"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"❌ Deactivated {updated} source(s)")
    deactivate_sources.short_description = "❌ Deactivate selected sources"


class LLMPromptAdmin(admin.ModelAdmin):
    """Admin interface for managing LLM prompts for MCQ and Descriptive generation"""
    
    list_display = ('prompt_type', 'source_url_preview', 'is_default', 'is_active', 'updated_at')
    list_filter = ('prompt_type', 'is_default', 'is_active', 'created_at')
    search_fields = ('source_url', 'prompt_text')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Prompt Configuration', {
            'fields': ('source_url', 'prompt_type', 'is_default', 'is_active')
        }),
        ('Prompt Content', {
            'fields': ('prompt_text',),
            'description': 'Use {title} and {content} as placeholders for the article title and content'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def source_url_preview(self, obj):
        """Display URL with truncation"""
        if obj.source_url:
            return obj.source_url[:50] + '...' if len(obj.source_url) > 50 else obj.source_url
        return '(Default)'
    source_url_preview.short_description = 'Source URL'


class JobFetchAdmin(admin.ModelAdmin):
    """Admin interface for job fetch tracking"""

    class JobFetchURLForm(forms.Form):
        source_url = forms.CharField(label='Source URL', required=True)
        prompt = forms.ModelChoiceField(
            label='Prompt',
            required=True,
            queryset=LLMPrompt.objects.filter(is_active=True),
        )
        site_identifier = forms.ChoiceField(
            label='Site',
            choices=[('freejobalert', 'freejobalert')],
            initial='freejobalert',
            required=True,
            help_text='Site-specific scraper; currently only freejobalert is supported.'
        )
        max_jobs_to_fetch = forms.IntegerField(
            label='Max jobs to fetch (0 = all)',
            required=False,
            initial=0,
            min_value=0,
            help_text='Process first N rows; leave 0 to fetch all rows from listing page.'
        )
        use_llm = forms.BooleanField(
            label='Use LLM',
            required=False,
            initial=False,
            help_text='Run LLM post-processing on detail pages (skipped when a canonical match exists).'
        )
        prune_html = forms.BooleanField(
            label='Prune HTML before LLM',
            required=False,
            initial=True,
            help_text='Keeps main content/tables/key sections and caps payload (~15k chars) to avoid token limits.'
        )

    class JobFetchPDFForm(forms.Form):
        pdf_file = forms.FileField(label='PDF File', required=True)
        prompt = forms.ModelChoiceField(
            label='Prompt',
            required=True,
            queryset=LLMPrompt.objects.filter(is_active=True),
        )
        notes = forms.CharField(label='Notes', required=False, widget=forms.Textarea(attrs={'rows': 3}))

    list_display = ('id', 'go_button', 'source_url_preview', 'prompt', 'status', 'is_active', 'created_date')
    list_filter = ('status', 'is_active', 'created_date')
    search_fields = ('source_url',)
    fieldsets = (
        ('Job Info', {
            'fields': ('source_url', 'prompt', 'status', 'is_active')
        }),
        ('Timestamps & Logs', {
            'fields': ('created_date', 'fetch_log'),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:object_id>/fetch/<str:mode>/',
                self.admin_site.admin_view(self.fetch_action_view),
                name='genai_jobfetch_fetch',
            ),
        ]
        return custom_urls + urls

    def fetch_action_view(self, request, object_id, mode):
        """Render dynamic form for URL/PDF fetch without processing."""
        obj = self.get_object(request, object_id)
        if not obj:
            return HttpResponseRedirect(reverse('admin:genai_jobfetch_changelist'))

        mode = mode.lower()
        if mode == 'url':
            form_class = self.JobFetchURLForm
            title = 'Fetch from URL'
        elif mode == 'pdf':
            form_class = self.JobFetchPDFForm
            title = 'Fetch from PDF'
        else:
            self.message_user(request, 'Invalid option', level='error')
            return HttpResponseRedirect(reverse('admin:genai_jobfetch_changelist'))

        if request.method == 'POST':
            form = form_class(request.POST, request.FILES, initial={'source_url': obj.source_url, 'prompt': obj.prompt})
            if form.is_valid():
                site_identifier = form.cleaned_data.get('site_identifier', 'freejobalert')
                max_jobs = form.cleaned_data.get('max_jobs_to_fetch') or 0
                use_llm = form.cleaned_data.get('use_llm', False)
                prune_html = form.cleaned_data.get('prune_html', True)
                prompt_obj = form.cleaned_data['prompt']

                try:
                    print(f"[JOBFETCH][ADMIN] Start id={obj.pk} site={site_identifier} max_jobs={max_jobs} use_llm={use_llm} prune_html={prune_html}", flush=True)
                    print(f"[JOBFETCH][ADMIN] Using prompt id={prompt_obj.id} source_url={prompt_obj.source_url or 'Default'}", flush=True)
                    logger.info("[JOB FETCH] Starting fetch for JobFetch id=%s site=%s max_jobs=%s use_llm=%s prune_html=%s", obj.pk, site_identifier, max_jobs, use_llm, prune_html)
                    obj.status = JobFetch.STATUS_IN_PROGRESS
                    obj.save(update_fields=['status'])

                    summary = run_job_fetch(
                        site_identifier=site_identifier,
                        max_jobs_to_fetch=max_jobs,
                        llm_prompt_text=prompt_obj.prompt_text,
                        use_llm=use_llm,
                        prune_html=prune_html,
                    )

                    obj.status = JobFetch.STATUS_COMPLETED
                    obj.fetch_log = json.dumps(summary)
                    obj.save(update_fields=['status', 'fetch_log'])

                    print(f"[JOBFETCH][ADMIN] Completed id={obj.pk} summary={summary}", flush=True)
                    logger.info("[JOB FETCH] Completed id=%s summary=%s", obj.pk, summary)

                    self.message_user(
                        request,
                        f"Scrape done: rows={summary.get('list_rows')} details={summary.get('details_fetched')} inserted={summary.get('inserted')} duplicates={summary.get('duplicates')} errors={summary.get('errors')}"
                    )
                except Exception as exc:
                    obj.status = JobFetch.STATUS_FAILED
                    obj.fetch_log = str(exc)
                    obj.save(update_fields=['status', 'fetch_log'])
                    print(f"[JOBFETCH][ADMIN] Failed id={obj.pk} err={exc}", flush=True)
                    logger.exception("[JOB FETCH] Failed id=%s: %s", obj.pk, exc)
                    self.message_user(request, f"Scrape failed: {exc}", level='error')

                return HttpResponseRedirect(reverse('admin:genai_jobfetch_changelist'))
        else:
            form = form_class(initial={'source_url': obj.source_url, 'prompt': obj.prompt})

        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'original': obj,
            'title': title,
            'form': form,
            'mode': mode,
        }
        return TemplateResponse(request, 'admin/genai/jobfetch_fetch.html', context)

    def go_button(self, obj):
        url_link = reverse('admin:genai_jobfetch_fetch', args=[obj.pk, 'url'])
        pdf_link = reverse('admin:genai_jobfetch_fetch', args=[obj.pk, 'pdf'])
        return format_html(
            '<div class="dropdown" style="position: relative; display: inline-block;">'
            '<button type="button" class="button" style="background: #417690; color: white; padding: 5px 12px; border-radius: 3px; border: none; cursor: pointer;" '
            'onclick="event.preventDefault(); event.stopPropagation(); const m=this.nextElementSibling; m.style.display = m.style.display === \'block\' ? \'none\' : \'block\';">GO ▼</button>'
            '<div style="display: none; position: absolute; background: white; min-width: 160px; box-shadow: 0px 8px 16px rgba(0,0,0,0.2); z-index: 1000; border-radius: 3px; margin-top: 2px;">'
            '<a href="{}" style="color: black; padding: 10px 12px; text-decoration: none; display: block; border-bottom: 1px solid #eee;" '
            'onmouseover="this.style.backgroundColor=\'#f1f1f1\'" onmouseout="this.style.backgroundColor=\'white\'">🕸️ Fetch from URL</a>'
            '<a href="{}" style="color: black; padding: 10px 12px; text-decoration: none; display: block;" '
            'onmouseover="this.style.backgroundColor=\'#f1f1f1\'" onmouseout="this.style.backgroundColor=\'white\'">📄 Fetch from PDF</a>'
            '</div>'
            '</div>'
            '<script>document.addEventListener("click",function(e){{document.querySelectorAll(".dropdown > div").forEach(function(d){{if(!d.contains(e.target) && !d.previousElementSibling.contains(e.target)){{d.style.display="none";}}}});}});</script>',
            url_link,
            pdf_link,
        )
    go_button.short_description = 'Action'

    def source_url_preview(self, obj):
        if not obj.source_url:
            return '(no source)'
        return obj.source_url[:50] + '...' if len(obj.source_url) > 50 else obj.source_url
    source_url_preview.short_description = 'Source URL'


# Processing Form View for Chapter and Difficulty Selection
def process_pdf_with_options(request):
    """
    Intermediate view to collect chapter and difficulty before processing PDF
    This view is called when user selects "Process to MCQ" or "Process to Descriptive"
    """
    from django.contrib.admin.views.decorators import staff_member_required
    from django.template.response import TemplateResponse
    
    # Require staff authentication
    if not request.user.is_staff:
        return redirect('/admin/login/')
    
    pdf_ids = request.session.get('pdf_ids', [])
    process_type = request.session.get('process_type', 'mcq')
    
    if not pdf_ids:
        return redirect('/admin/genai/pdfupload/')
    
    if request.method == 'POST':
        form = ProcessPDFForm(request.POST)
        print(f"\n{'='*80}")
        print(f"[FORM SUBMISSION DEBUG]")
        print(f"{'='*80}")
        print(f"Form is valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
            print(f"Form non-field errors: {form.non_field_errors()}")
        print(f"{'='*80}\n")
        
        if form.is_valid():
            # Get common fields
            processing_type = form.cleaned_data.get('processing_type', 'subject_mcq')
            page_from = form.cleaned_data.get('page_from')
            page_to = form.cleaned_data.get('page_to')
            
            # Debug: Print form data
            print(f"\n{'='*80}")
            print(f"[FORM DEBUG] Cleaned Data:")
            print(f"{'='*80}")
            print(f"page_from type: {type(page_from).__name__}, value: {page_from}")
            print(f"page_to type: {type(page_to).__name__}, value: {page_to}")
            print(f"page_from is None: {page_from is None}")
            print(f"page_to is None: {page_to is None}")
            print(f"{'='*80}\n")
            
            # Get the PDFs
            pdfs = PDFUpload.objects.filter(id__in=pdf_ids)
            
            # Process each PDF
            from genai.tasks.task_router import route_pdf_processing_task
            import logging
            import json
            
            logger = logging.getLogger(__name__)
            count = 0
            
            # ==================== MODE 1: SUBJECT-BASED MCQ ====================
            if processing_type == 'subject_mcq':
                chapter = form.cleaned_data.get('chapter', '')
                difficulty = form.cleaned_data.get('difficulty', 'medium') or 'medium'
                extract_all = form.cleaned_data.get('extract_all', False)
                
                if extract_all:
                    num_items = 999999
                else:
                    num_items = form.cleaned_data.get('num_items', 5) or 5
                
                print("\n" + "█"*80)
                print(f"🎬 ADMIN ACTION: Subject-based MCQ Processing")
                print(f"   Chapter: {chapter if chapter else 'Any'}")
                print(f"   Difficulty: {difficulty}")
                print(f"   Extract All MCQs: {extract_all}")
                print(f"   Num Items: {'ALL' if extract_all else num_items}")
                print(f"   Page Range: {page_from} to {page_to if page_to else 'End'}")
                print(f"   Selected PDFs: {pdfs.count()}")
                print("█"*80 + "\n")
                
                for pdf in pdfs:
                    try:
                        print(f"\n📄 Processing PDF: {pdf.title}")
                        print(f"   Subject: {pdf.subject}")
                        print(f"   File: {pdf.pdf_file.name}\n")
                        
                        print(f"   [ADMIN] Creating ProcessingLog...")
                        log = ProcessingLog.objects.create(
                            task_type='pdf_to_mcq',
                            subject=pdf.subject if pdf.subject else 'other',
                            pdf_upload=pdf,
                            difficulty_level=difficulty,
                            num_items=num_items,
                            start_page=page_from,
                            end_page=page_to,
                            output_format='json',
                            status='pending',
                            created_by=request.user if request.user.is_authenticated else None
                        )
                        print(f"   [ADMIN] ✓ ProcessingLog created (ID: {log.id})\n")
                        
                        if chapter:
                            log_data = {'chapter': chapter}
                            log.log_details = json.dumps(log_data)
                            log.save()
                            print(f"   [ADMIN] Chapter saved: {chapter}\n")
                        
                        print(f"   [ADMIN] Calling route_pdf_processing_task()...")
                        result = route_pdf_processing_task(log)
                        print(f"   [ADMIN] Route completed\n")
                        
                        if result.get('success'):
                            count += 1
                            pdf.status = 'completed'
                            print(f"   ✅ SUCCESS: {result.get('saved_items', 0)} items generated\n")
                        else:
                            pdf.status = 'failed'
                            print(f"   ❌ FAILED\n")
                        pdf.save()
                            
                    except Exception as e:
                        logger.error(f"Error processing PDF {pdf.id}: {str(e)}")
                        print(f"   ❌ ERROR: {str(e)}\n")
                        pdf.status = 'failed'
                        pdf.save()
            
            # ==================== MODE 2: CURRENT AFFAIRS MCQ ====================
            elif processing_type == 'ca_mcq':
                ca_date = form.cleaned_data.get('ca_date')
                ca_year = form.cleaned_data.get('ca_year')
                ca_auto_date = form.cleaned_data.get('ca_auto_date', False)
                num_items = form.cleaned_data.get('num_items', 5) or 5
                
                print("\n" + "█"*80)
                print(f"🎬 ADMIN ACTION: Current Affairs MCQ Processing")
                print(f"   Date: {ca_date if ca_date else 'Today (auto)'}")
                print(f"   Year: {ca_year if ca_year else 'Current year (auto)'}")
                print(f"   Auto-decide: {ca_auto_date}")
                print(f"   Num MCQs: {num_items}")
                print(f"   Page Range: {page_from} to {page_to if page_to else 'End'}")
                print(f"   Selected PDFs: {pdfs.count()}")
                print("█"*80 + "\n")
                
                for pdf in pdfs:
                    try:
                        print(f"\n📄 Processing PDF: {pdf.title}")
                        print(f"   File: {pdf.pdf_file.name}\n")
                        
                        print(f"   [ADMIN] Creating ProcessingLog...")
                        log = ProcessingLog.objects.create(
                            task_type='pdf_currentaffairs_mcq',
                            subject='current_affairs',
                            pdf_upload=pdf,
                            num_items=num_items,
                            start_page=page_from,
                            end_page=page_to,
                            ca_date=ca_date,
                            ca_year=ca_year if ca_year else None,
                            ca_auto_date=ca_auto_date,
                            output_format='json',
                            status='pending',
                            created_by=request.user if request.user.is_authenticated else None
                        )
                        print(f"   [ADMIN] ✓ ProcessingLog created (ID: {log.id})\n")
                        
                        print(f"   [ADMIN] Calling route_pdf_processing_task()...")
                        result = route_pdf_processing_task(log)
                        print(f"   [ADMIN] Route completed\n")
                        
                        if result.get('success'):
                            count += 1
                            pdf.status = 'completed'
                            print(f"   ✅ SUCCESS: {result.get('saved_items', 0)} MCQs generated\n")
                        else:
                            pdf.status = 'failed'
                            print(f"   ❌ FAILED\n")
                        pdf.save()
                            
                    except Exception as e:
                        logger.error(f"Error processing PDF {pdf.id}: {str(e)}")
                        print(f"   ❌ ERROR: {str(e)}\n")
                        pdf.status = 'failed'
                        pdf.save()
            
            # ==================== MODE 3: CURRENT AFFAIRS DESCRIPTIVE ====================
            elif processing_type == 'ca_descriptive':
                ca_date = form.cleaned_data.get('ca_date')
                ca_year = form.cleaned_data.get('ca_year')
                ca_auto_date = form.cleaned_data.get('ca_auto_date', False)
                
                print("\n" + "█"*80)
                print(f"🎬 ADMIN ACTION: Current Affairs Descriptive Processing")
                print(f"   Date: {ca_date if ca_date else 'Today (auto)'}")
                print(f"   Year: {ca_year if ca_year else 'Current year (auto)'}")
                print(f"   Auto-decide: {ca_auto_date}")
                print(f"   Page Range: {page_from} to {page_to if page_to else 'End'}")
                print(f"   Selected PDFs: {pdfs.count()}")
                print("█"*80 + "\n")
                
                for pdf in pdfs:
                    try:
                        print(f"\n📄 Processing PDF: {pdf.title}")
                        print(f"   File: {pdf.pdf_file.name}\n")
                        
                        print(f"   [ADMIN] Creating ProcessingLog...")
                        log = ProcessingLog.objects.create(
                            task_type='pdf_currentaffairs_descriptive',
                            subject='current_affairs',
                            pdf_upload=pdf,
                            num_items=1,  # Descriptive is typically one per PDF
                            start_page=page_from,
                            end_page=page_to,
                            ca_date=ca_date,
                            ca_year=ca_year if ca_year else None,
                            ca_auto_date=ca_auto_date,
                            output_format='markdown',
                            status='pending',
                            created_by=request.user if request.user.is_authenticated else None
                        )
                        print(f"   [ADMIN] ✓ ProcessingLog created (ID: {log.id})\n")
                        
                        print(f"   [ADMIN] Calling route_pdf_processing_task()...")
                        result = route_pdf_processing_task(log)
                        print(f"   [ADMIN] Route completed\n")
                        
                        if result.get('success'):
                            count += 1
                            pdf.status = 'completed'
                            print(f"   ✅ SUCCESS: Descriptive content generated\n")
                        else:
                            pdf.status = 'failed'
                            print(f"   ❌ FAILED\n")
                        pdf.save()
                            
                    except Exception as e:
                        logger.error(f"Error processing PDF {pdf.id}: {str(e)}")
                        print(f"   ❌ ERROR: {str(e)}\n")
                        pdf.status = 'failed'
                        pdf.save()
            
            print("█"*80)
            print(f"✅ ADMIN ACTION COMPLETE: Processed {count}/{pdfs.count()} PDFs")
            print("█"*80 + "\n")
            
            # Clean up session
            del request.session['pdf_ids']
            del request.session['process_type']
            
            
            print("█"*80)
            print(f"✅ ADMIN ACTION COMPLETE: Processed {count}/{pdfs.count()} PDFs")
            print("█"*80 + "\n")
            
            # Redirect back to PDFUpload list
            from django.contrib import messages
            messages.success(request, f"✓ Successfully processed {count}/{pdfs.count()} PDF(s)")
            return redirect('/admin/genai/pdfupload/')
    else:
        form = ProcessPDFForm()
    
    # Render the form
    context = {
        'form': form,
        'title': f'Select Options - Process {len(pdf_ids)} PDF(s) to {process_type.upper()}',
        'pdfs': PDFUpload.objects.filter(id__in=pdf_ids),
        'process_type': process_type,
    }
    
    return TemplateResponse(request, 'admin/genai/process_pdf_form.html', context)


class BulkImportForm(forms.Form):
    """Intermediate form for bulk import with date selection"""
    import_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Date to use for records that don\'t have year_now, month, or day fields'
    )


class JsonImportAdmin(admin.ModelAdmin):
    """Admin interface for JSON Import"""
    list_display = ['to_table_display', 'created_at', 'record_count', 'created_by']
    list_filter = ['to_table', 'created_at']
    search_fields = ['to_table']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Configuration', {
            'fields': ('to_table', 'json_data'),
            'description': 'Select the target table and paste your JSON array of objects'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['bulk_import_action']
    
    def to_table_display(self, obj):
        """Display table name with color"""
        return format_html(
            '<span style="background-color: #e3f2fd; padding: 3px 8px; border-radius: 3px;">{}</span>',
            obj.get_to_table_display()
        )
    to_table_display.short_description = 'Target Table'
    
    def record_count(self, obj):
        """Count records in JSON"""
        try:
            import json
            data = json.loads(obj.json_data)
            if isinstance(data, list):
                return len(data)
            return 1
        except:
            return 0
    record_count.short_description = 'Records'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def bulk_import_action(self, request, queryset):
        """Custom action to trigger bulk import with date selection"""
        print("\n" + "="*80)
        print(f"🎯 [ADMIN] bulk_import_action() CALLED")
        print(f"   Method: {request.method}")
        print(f"   Path: {request.path}")
        print(f"   Selected Records: {queryset.count()}")
        print("="*80)
        
        if request.method == 'POST':
            print(f"\n📋 [ADMIN] POST REQUEST received")
            print(f"   All POST data:")
            for key, value in request.POST.items():
                if len(str(value)) > 100:
                    print(f"      {key}: {str(value)[:100]}... (truncated)")
                else:
                    print(f"      {key}: {value}")
            
            print(f"\n   POST Keys: {list(request.POST.keys())}")
            
            # Check if this is from changelist action form or from bulk_import_form
            is_action_form = 'action' in request.POST or '_selected_action' in request.POST
            is_import_form = 'import_date' in request.POST
            
            print(f"   Is changelist action form: {is_action_form}")
            print(f"   Is import_date form: {is_import_form}")
            
            if is_action_form and not is_import_form:
                print(f"\n   📊 [FLOW] This is the INITIAL action form - showing the date selection form")
                form = BulkImportForm()
            else:
                print(f"\n   📊 [FLOW] This is the IMPORT form submission - processing the import")
                form = BulkImportForm(request.POST)
                print(f"   Form is_bound: {form.is_bound}")
            
            if form.is_bound and form.is_valid():
                print(f"   ✅ Form is VALID")
                import_date = form.cleaned_data['import_date']
                print(f"   📅 Import Date extracted: {import_date}")
                from datetime import time
                
                # Process each selected JsonImport record
                success_count = 0
                error_count = 0
                
                print(f"\n📥 [ADMIN] Processing {queryset.count()} JsonImport records...")
                for idx, json_import in enumerate(queryset, 1):
                    print(f"\n   [{idx}/{queryset.count()}] Processing: {json_import.to_table}")
                    print(f"      - ID: {json_import.id}")
                    print(f"      - JSON Data Length: {len(json_import.json_data)} chars")
                    
                    # Run the importer
                    print(f"      [INIT] Creating BulkImporter instance...")
                    importer = BulkImporter(
                        table_name=json_import.to_table,
                        json_data=json_import.json_data,
                        form_date=import_date,
                        form_time=time(10, 0, 0)  # Default time
                    )
                    print(f"      ✅ BulkImporter created")
                    
                    print(f"      [IMPORT] Calling import_data()...")
                    result = importer.import_data()
                    print(f"      ✅ import_data() returned")
                    print(f"      Result: {result}")
                    
                    if result['success'] or result['created'] > 0:
                        success_count += result['created'] + result['updated']
                        print(f"      ✅ Added {result['created'] + result['updated']} records")
                    else:
                        error_count += len(result['errors'])
                        print(f"      ❌ {len(result['errors'])} errors occurred")
                        for err in result['errors'][:3]:
                            print(f"         - {err}")
                
                print(f"\n✅ [ADMIN] Processing Complete")
                print(f"   Total Created/Updated: {success_count}")
                print(f"   Total Errors: {error_count}")
                
                # Show success message
                message = f'✅ Bulk import completed! Records created/updated: {success_count}. Errors: {error_count}'
                print(f"   Message: {message}")
                self.message_user(request, message)
                print(f"   [REDIRECT] Redirecting to {request.path}")
                return redirect(request.path)
            elif form.is_bound:
                print(f"   ❌ Form is INVALID")
                print(f"   Form Errors: {form.errors}")
                print(f"   Form error_dict: {form.errors.as_data() if hasattr(form.errors, 'as_data') else 'N/A'}")
        else:
            print(f"\n📋 [ADMIN] GET REQUEST received - showing action form")
            form = BulkImportForm()
            print(f"   ✅ Form instance created")
        
        # Show the intermediate form
        print(f"\n📄 [ADMIN] Rendering bulk_import_form.html")
        
        # Extract selected IDs from queryset
        selected_ids = list(queryset.values_list('id', flat=True))
        print(f"   Selected IDs: {selected_ids}")
        
        context = {
            'form': form,
            'title': 'Bulk Import - Select Import Date',
            'queryset': queryset,
            'selected_ids': selected_ids,
            'opts': self.model._meta,
            'has_change_permission': True,
        }
        print(f"   Context prepared with {queryset.count()} records")
        print(f"   Selected IDs passed to template: {selected_ids}")
        print("="*80 + "\n")
        return TemplateResponse(
            request,
            'admin/genai/bulk_import_form.html',
            context
        )
    
    bulk_import_action.short_description = '📥 Bulk Import (Select records & proceed)'


# Register models with admin
admin_site.register(PDFUpload, PDFUploadAdmin)
admin_site.register(CurrentAffairsGeneration, CurrentAffairsGenerationAdmin)
admin_site.register(MathProblemGeneration, MathProblemGenerationAdmin)
admin_site.register(ProcessingTask, ProcessingTaskAdmin)
admin_site.register(ProcessingLog, ProcessingLogAdmin)
admin_site.register(ContentSource, ContentSourceAdmin)
admin_site.register(LLMPrompt, LLMPromptAdmin)
admin_site.register(JobFetch, JobFetchAdmin)
admin_site.register(JsonImport, JsonImportAdmin)
