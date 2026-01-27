from django.db import models
from django.contrib.auth.models import User
import os
import datetime


class PDFUpload(models.Model):
    """Model to track PDF uploads for processing"""
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    title = models.CharField(max_length=255)
    subject = models.CharField(
        max_length=50,
        choices=[
            ('polity', 'Polity'),
            ('history', 'History'),
            ('geography', 'Geography'),
            ('economics', 'Economics'),
            ('physics', 'Physics'),
            ('chemistry', 'Chemistry'),
            ('biology', 'Biology'),
            ('math', 'Math'),
            ('other', 'Other'),
        ],
        default='other'
    )
    pdf_file = models.FileField(upload_to='genai/pdfs/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    total_pages = models.IntegerField(default=0)
    extracted_text = models.TextField(blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} ({self.subject})"
    
    class Meta:
        ordering = ['-uploaded_at']


class CurrentAffairsGeneration(models.Model):
    """Track current affairs content generation"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    topic = models.CharField(max_length=255)
    source_url = models.URLField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    generated_mcq = models.TextField(blank=True, null=True, help_text="Generated MCQ content")
    generated_descriptive = models.TextField(blank=True, null=True, help_text="Generated descriptive content")
    
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.topic} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']


class MathProblemGeneration(models.Model):
    """Track math problem generation"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    expression = models.TextField(help_text="Math expression to convert to LaTeX")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    latex_output = models.TextField(blank=True, null=True)
    generated_mcqs = models.TextField(blank=True, null=True, help_text="Generated MCQs in JSON format")
    
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Math Problem - {self.difficulty} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']


class ProcessingTask(models.Model):
    """Generic task tracking for all GenAI operations"""
    TASK_TYPES = [
        ('pdf_to_mcq', 'PDF to MCQ'),
        ('current_affairs_mcq', 'Current Affairs MCQ'),
        ('current_affairs_descriptive', 'Current Affairs Descriptive'),
        ('math_to_latex', 'Math to LaTeX'),
        ('math_mcq_batch', 'Math MCQ Batch'),
        ('pdf_extraction', 'PDF Text Extraction'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    pdf_upload = models.ForeignKey(PDFUpload, on_delete=models.SET_NULL, null=True, blank=True, help_text="Associated PDF upload")
    
    input_data = models.TextField(blank=True, null=True, help_text="Input parameters as JSON")
    output_data = models.TextField(blank=True, null=True, help_text="Generated output as JSON")
    
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    error_message = models.TextField(blank=True, null=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_task_type_display()} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Processing Task"
        verbose_name_plural = "Processing Tasks"


class ProcessingLog(models.Model):
    """Track processing logs for MCQ and Current Affairs fetches with status monitoring"""
    
    TASK_TYPES = [
        ('currentaffairs_mcq_fetch', 'Current Affairs MCQ Fetch from URL'),
        ('currentaffairs_descriptive_fetch', 'Current Affairs Descriptive Fetch from URL'),
        ('both', 'Both MCQ & Current Affairs from URL'),
        ('pdf_currentaffairs_mcq', 'Current Affairs MCQ Generation from PDF'),
        ('pdf_currentaffairs_descriptive', 'Current Affairs Descriptive Generation from PDF'),
        ('pdf_to_mcq', 'PDF to Generic MCQ'),
        ('pdf_to_descriptive', 'PDF to Generic Descriptive'),
        ('pdf_to_polity', 'PDF to Polity MCQ'),
        ('pdf_to_economics', 'PDF to Economics MCQ'),
        ('pdf_to_math', 'PDF to Math MCQ'),
        ('pdf_to_physics', 'PDF to Physics MCQ'),
        ('pdf_to_chemistry', 'PDF to Chemistry MCQ'),
        ('pdf_to_history', 'PDF to History MCQ'),
        ('pdf_to_geography', 'PDF to Geography MCQ'),
        ('pdf_to_biology', 'PDF to Biology MCQ'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    
    # Source: Either URL-based or PDF-based
    pdf_upload = models.ForeignKey(PDFUpload, on_delete=models.SET_NULL, null=True, blank=True, help_text="PDF file if this is a PDF processing task")
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Progress tracking
    total_items = models.IntegerField(default=0)
    processed_items = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)
    
    # Details
    mcq_status = models.CharField(max_length=100, default='', blank=True)
    current_affairs_status = models.CharField(max_length=100, default='', blank=True)
    
    error_message = models.TextField(blank=True, null=True)
    log_details = models.TextField(blank=True, null=True, help_text="Detailed log as JSON")
    
    # Scheduling
    scheduled_time = models.DateTimeField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)
    
    # LLM-Direct Mode
    skip_scraping = models.BooleanField(default=False, help_text="Skip web scraping and send URLs directly to LLM with prompt")
    
    # NEW FIELDS FOR SUBJECT-BASED ROUTING (Task Router Support)
    subject = models.CharField(
        max_length=50,
        choices=[
            ('polity', 'Polity'),
            ('economics', 'Economics'),
            ('math', 'Mathematics'),
            ('physics', 'Physics'),
            ('chemistry', 'Chemistry'),
            ('history', 'History'),
            ('geography', 'Geography'),
            ('biology', 'Biology'),
            ('other', 'Other'),
        ],
        default='other',
        blank=True,
        null=True,
        db_index=True,
        help_text="Subject for routing to subject-specific processor"
    )
    
    output_format = models.CharField(
        max_length=20,
        choices=[
            ('json', 'JSON'),
            ('markdown', 'Markdown'),
            ('text', 'Plain Text'),
        ],
        default='json',
        blank=True,
        null=True,
        help_text="Format for output (MCQ/Descriptive)"
    )
    
    start_page = models.IntegerField(
        blank=True,
        null=True,
        help_text="Start page for PDF processing"
    )
    
    end_page = models.IntegerField(
        blank=True,
        null=True,
        help_text="End page for PDF processing"
    )
    
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium',
        blank=True,
        null=True,
        help_text="Difficulty level for generated content"
    )
    
    num_items = models.IntegerField(
        default=5,
        blank=True,
        null=True,
        help_text="Number of MCQs/Descriptive answers to generate"
    )
    
    # Current Affairs specific fields
    ca_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date for current affairs (if provided by user)"
    )
    
    ca_year = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=[
            ('2025', '2025'),
            ('2026', '2026'),
            ('2027', '2027'),
            ('2028', '2028'),
        ],
        help_text="Year for current affairs"
    )
    
    ca_auto_date = models.BooleanField(
        default=False,
        help_text="If True, LLM decides date/year from content"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def duration(self):
        """Calculate task duration"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.total_items > 0:
            return int((self.processed_items / self.total_items) * 100)
        return 0
    
    def __str__(self):
        return f"{self.get_task_type_display()} - {self.status} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Processing Log"
        verbose_name_plural = "Processing Logs"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]


class ContentSource(models.Model):
    """Model to store and manage content sources (URLs) for MCQ and Current Affairs"""
    SOURCE_TYPE_CHOICES = [
        ('currentaffairs_mcq', 'Current Affairs MCQ Source'),
        ('currentaffairs_descriptive', 'Current Affairs Descriptive Source'),
    ]
    
    source_type = models.CharField(max_length=40, choices=SOURCE_TYPE_CHOICES)
    url = models.URLField(max_length=500, help_text="Enter the full URL to fetch content from")
    name = models.CharField(max_length=255, help_text="Display name for this source")
    description = models.TextField(blank=True, null=True, help_text="Optional description of this source")
    
    # Content date - MANDATORY - used for MCQ generation
    content_date = models.DateField(
        default=datetime.date.today,
        help_text="Date for which this content is relevant. Year, Month, and Date will be extracted for MCQs"
    )
    
    # Status
    is_active = models.BooleanField(default=True, help_text="Enable/disable this source")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Content Source"
        verbose_name_plural = "Content Sources"
        unique_together = ['source_type', 'url']
    
    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"


class LLMPrompt(models.Model):
    """Store and manage LLM prompts for MCQ and Descriptive generation"""
    PROMPT_TYPE_CHOICES = [
        ('mcq', 'MCQ'),
        ('descriptive', 'Descriptive'),
    ]
    
    source_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Source URL or leave blank for default prompt (e.g., https://example.com/news)"
    )
    prompt_type = models.CharField(
        max_length=20,
        choices=PROMPT_TYPE_CHOICES,
        help_text="Type of prompt: MCQ or Descriptive"
    )
    prompt_text = models.TextField(
        help_text="The actual prompt to send to LLM. Use {title} and {content} as placeholders."
    )
    is_default = models.BooleanField(
        default=False,
        help_text="Check if this is the default prompt for this type"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Deactivate to disable this prompt without deleting"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ('source_url', 'prompt_type')
        verbose_name = 'LLM Prompt'
        verbose_name_plural = 'LLM Prompts'
        ordering = ['-is_default', 'source_url', 'prompt_type']
    
    def __str__(self):
        source = self.source_url if self.source_url else 'Default'
        return f"{self.get_prompt_type_display()} - {source}"
    
    def save(self, *args, **kwargs):
        # If this is set as default, unset other defaults of the same type and source
        if self.is_default:
            LLMPrompt.objects.filter(
                prompt_type=self.prompt_type,
                source_url=self.source_url
            ).exclude(id=self.id).update(is_default=False)
        super(LLMPrompt, self).save(*args, **kwargs)

