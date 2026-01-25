from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone
from bank.admin import admin_site
from .models import PDFUpload, CurrentAffairsGeneration, MathProblemGeneration, ProcessingTask, ProcessingLog, ContentSource, LLMPrompt


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


class ProcessingLogAdmin(admin.ModelAdmin):
    """Admin interface for Processing Logs with status tracking"""
    
    list_display = ('id', 'task_type_display', 'status_badge', 'progress_bar', 'duration_display', 'created_at', 'admin_action_buttons')
    list_filter = ('status', 'task_type', 'created_at')
    search_fields = ('id', 'mcq_status', 'current_affairs_status')
    readonly_fields = ('id', 'created_at', 'updated_at', 'started_at', 'completed_at', 'duration_display', 'progress_percentage_display', 'log_details_formatted')
    
    fieldsets = (
        ('Task Information', {
            'fields': ('id', 'task_type', 'status', 'created_by')
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
    
    list_display = ('name', 'source_type_display', 'url_preview', 'is_active_badge', 'created_at')
    list_filter = ('source_type', 'is_active', 'created_at')
    search_fields = ('name', 'url', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Source Information', {
            'fields': ('name', 'source_type', 'url', 'description')
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


# Register models with admin
admin_site.register(PDFUpload, PDFUploadAdmin)
admin_site.register(CurrentAffairsGeneration, CurrentAffairsGenerationAdmin)
admin_site.register(MathProblemGeneration, MathProblemGenerationAdmin)
admin_site.register(ProcessingTask, ProcessingTaskAdmin)
admin_site.register(ProcessingLog, ProcessingLogAdmin)
admin_site.register(ContentSource, ContentSourceAdmin)
admin_site.register(LLMPrompt, LLMPromptAdmin)
