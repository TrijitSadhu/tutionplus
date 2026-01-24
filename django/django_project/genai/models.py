from django.db import models
from django.contrib.auth.models import User
import os


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
