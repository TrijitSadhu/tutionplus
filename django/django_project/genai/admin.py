from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from .models import PDFUpload, CurrentAffairsGeneration, MathProblemGeneration, ProcessingTask


class PDFUploadAdmin(admin.ModelAdmin):
    """Admin interface for PDF uploads with processing actions"""
    
    list_display = ('title', 'subject', 'status_badge', 'total_pages', 'uploaded_at', 'actions_column')
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
    
    actions = ['process_pdf_to_mcq', 'extract_text_from_pdf']
    
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
    
    def actions_column(self, obj):
        """Show action buttons"""
        urls = f'<a class="button" href="#">Process MCQ</a> '
        return format_html(urls)
    actions_column.short_description = 'Actions'
    
    def process_pdf_to_mcq(self, request, queryset):
        """Action to process selected PDFs into MCQs"""
        for pdf in queryset:
            pdf.status = 'processing'
            pdf.save()
        self.message_user(request, f"Started processing {queryset.count()} PDF(s)")
    process_pdf_to_mcq.short_description = "Process selected PDFs to MCQs"
    
    def extract_text_from_pdf(self, request, queryset):
        """Action to extract text from PDFs"""
        for pdf in queryset:
            pdf.status = 'processing'
            pdf.save()
        self.message_user(request, f"Started text extraction for {queryset.count()} PDF(s)")
    extract_text_from_pdf.short_description = "Extract text from selected PDFs"


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
    
    list_display = ('expression_preview', 'difficulty', 'status_badge', 'created_at', 'has_latex')
    list_filter = ('difficulty', 'status', 'created_at')
    search_fields = ('expression',)
    readonly_fields = ('created_at', 'processed_at')
    
    fieldsets = (
        ('Math Input', {
            'fields': ('expression', 'difficulty')
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
    
    def expression_preview(self, obj):
        preview = obj.expression[:50] + '...' if len(obj.expression) > 50 else obj.expression
        return preview
    expression_preview.short_description = 'Expression'
    
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
        for item in queryset:
            item.status = 'processing'
            item.save()
        self.message_user(request, f"Started LaTeX conversion for {queryset.count()} item(s)")
    convert_to_latex.short_description = "Convert to LaTeX"
    
    def generate_math_mcqs(self, request, queryset):
        for item in queryset:
            item.status = 'processing'
            item.save()
        self.message_user(request, f"Started MCQ generation for {queryset.count()} math problem(s)")
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


# Register models with admin
admin.site.register(PDFUpload, PDFUploadAdmin)
admin.site.register(CurrentAffairsGeneration, CurrentAffairsGenerationAdmin)
admin.site.register(MathProblemGeneration, MathProblemGenerationAdmin)
admin.site.register(ProcessingTask, ProcessingTaskAdmin)
