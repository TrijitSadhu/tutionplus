# ProcessingLog Model Enhancement - Code Changes

## Current ProcessingLog Model

Located at: `genai/models.py` (lines 150-240)

## Proposed Changes

### 1. New Task Types to Add

**Before:**
```python
TASK_TYPES = [
    ('currentaffairs_mcq_fetch', 'Current Affairs MCQ Fetch from URL'),
    ('currentaffairs_descriptive_fetch', 'Current Affairs Descriptive Fetch from URL'),
    ('both', 'Both MCQ & Current Affairs from URL'),
    ('pdf_currentaffairs_mcq', 'Current Affairs MCQ Generation from PDF'),
    ('pdf_currentaffairs_descriptive', 'Current Affairs Descriptive Generation from PDF'),
]
```

**After:**
```python
TASK_TYPES = [
    ('currentaffairs_mcq_fetch', 'Current Affairs MCQ Fetch from URL'),
    ('currentaffairs_descriptive_fetch', 'Current Affairs Descriptive Fetch from URL'),
    ('both', 'Both MCQ & Current Affairs from URL'),
    ('pdf_currentaffairs_mcq', 'Current Affairs MCQ Generation from PDF'),
    ('pdf_currentaffairs_descriptive', 'Current Affairs Descriptive Generation from PDF'),
    
    # NEW SUBJECT-WISE PDF PROCESSING
    ('pdf_to_mcq', 'PDF → MCQ Questions'),
    ('pdf_to_descriptive', 'PDF → Descriptive Answers'),
    ('pdf_to_polity', 'PDF → Polity Notes'),
    ('pdf_to_economics', 'PDF → Economics Notes'),
    ('pdf_to_math', 'PDF → Math Problems'),
    ('pdf_to_physics', 'PDF → Physics Notes'),
    ('pdf_to_chemistry', 'PDF → Chemistry Notes'),
    ('pdf_to_history', 'PDF → History Notes'),
    ('pdf_to_geography', 'PDF → Geography Notes'),
    ('pdf_to_biology', 'PDF → Biology Notes'),
]
```

### 2. New Fields to Add

Add these fields to ProcessingLog class (after existing fields):

```python
# Subject Classification (for PDF processing)
SUBJECT_CHOICES = [
    ('polity', 'Polity'),
    ('economics', 'Economics'),
    ('math', 'Math'),
    ('physics', 'Physics'),
    ('chemistry', 'Chemistry'),
    ('history', 'History'),
    ('geography', 'Geography'),
    ('biology', 'Biology'),
    ('current_affairs', 'Current Affairs'),
    ('other', 'Other'),
]

subject = models.CharField(
    max_length=50,
    choices=SUBJECT_CHOICES,
    null=True,
    blank=True,
    db_index=True,
    help_text="Subject for PDF processing (null for web-based tasks)"
)

# Output Format Configuration
OUTPUT_FORMAT_CHOICES = [
    ('json', 'JSON'),
    ('markdown', 'Markdown'),
    ('text', 'Plain Text'),
    ('csv', 'CSV'),
]

output_format = models.CharField(
    max_length=50,
    choices=OUTPUT_FORMAT_CHOICES,
    default='json',
    help_text="Format for generated output"
)

# Page Range for Large PDFs
start_page = models.IntegerField(
    null=True,
    blank=True,
    help_text="Start page for PDF processing (1-indexed, null means start from page 1)"
)

end_page = models.IntegerField(
    null=True,
    blank=True,
    help_text="End page for PDF processing (inclusive, null means until end)"
)

# Difficulty Level (for MCQ/Math generation)
DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]

difficulty_level = models.CharField(
    max_length=20,
    choices=DIFFICULTY_CHOICES,
    null=True,
    blank=True,
    help_text="Difficulty level for generated questions (used for pdf_to_mcq, pdf_to_math)"
)

# Number of Items to Generate
num_items = models.IntegerField(
    default=10,
    help_text="Number of questions/items to generate from PDF"
)
```

### 3. Updated fieldsets in Admin

Add new fieldsets to ProcessingLogAdmin (genai/admin.py):

```python
class ProcessingLogAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Task Information', {
            'fields': ('task_type', 'status', 'pdf_upload', 'created_by')
        }),
        ('PDF Processing Options', {
            'fields': ('subject', 'output_format', 'difficulty_level', 'num_items', 'start_page', 'end_page'),
            'description': 'Fill these fields when processing PDFs. Leave blank for URL-based tasks.'
        }),
        ('Progress Tracking', {
            'fields': ('total_items', 'processed_items', 'success_count', 'error_count')
        }),
        ('Timing', {
            'fields': ('scheduled_time', 'is_scheduled', 'started_at', 'completed_at')
        }),
        ('Details', {
            'fields': ('mcq_status', 'current_affairs_status', 'skip_scraping', 'error_message', 'log_details'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Auto-filled by system'
        }),
    )

    list_display = ('task_type', 'status', 'subject', 'difficulty_level', 'progress_percentage', 'created_at')
    list_filter = ('task_type', 'status', 'subject', 'difficulty_level', 'created_at')
    search_fields = ('created_by__username', 'error_message')
    readonly_fields = ('created_at', 'updated_at', 'started_at', 'completed_at', 'progress_percentage')
```

### 4. Updated Meta class

```python
class Meta:
    ordering = ['-created_at']
    verbose_name = "Processing Log"
    verbose_name_plural = "Processing Logs"
    indexes = [
        models.Index(fields=['-created_at']),
        models.Index(fields=['status', '-created_at']),
        models.Index(fields=['subject', 'task_type']),  # NEW: For quick subject filtering
    ]
```

---

## Migration Script

After updating the model, run:

```bash
# Create migration
python manage.py makemigrations genai

# Apply migration
python manage.py migrate genai
```

### Expected Migration Output:
```
Migrations for 'genai':
  0010_processinglog_enhancements.py
    - Add field subject to processinglog
    - Add field output_format to processinglog
    - Add field start_page to processinglog
    - Add field end_page to processinglog
    - Add field difficulty_level to processinglog
    - Add field num_items to processinglog
    - Add index for subject + task_type
```

---

## Updated Model Summary

### ProcessingLog Fields After Enhancement

**Existing (18 fields):**
- id, task_type, status, pdf_upload, started_at, completed_at
- total_items, processed_items, success_count, error_count
- mcq_status, current_affairs_status, error_message, log_details
- scheduled_time, is_scheduled, skip_scraping
- created_at, updated_at, created_by

**NEW (6 fields):**
- subject (CharField, optional)
- output_format (CharField, default='json')
- start_page (IntegerField, optional)
- end_page (IntegerField, optional)
- difficulty_level (CharField, optional)
- num_items (IntegerField, default=10)

**Total: 24 fields** (organized by feature)

---

## Backward Compatibility

✅ All new fields are optional (null=True) or have defaults
✅ Existing URL-based tasks unaffected
✅ ProcessingLog can still track all types of tasks
✅ Admin interface backward compatible

---

## Admin Interface Updates

### Changes to ProcessingLogAdmin

1. **Conditional field display based on task_type:**
   ```python
   def get_fieldsets(self, request, obj=None):
       if obj and obj.task_type.startswith('pdf_'):
           # Show PDF-specific fields
       else:
           # Show URL-specific fields
   ```

2. **New list filters:**
   - subject (filter by Polity, Economics, Math, etc.)
   - difficulty_level (Easy, Medium, Hard)
   - task_type (already exists, but now more options)

3. **New search fields:**
   - creator (created_by__username)
   - subject

4. **New action buttons:**
   - Process to MCQ
   - Process to Descriptive
   - Process to Subject Notes
   - View Results
   - Export Results

---

## Database Size Impact

**Per ProcessingLog record:**
- 6 new fields = ~50 bytes additional storage
- Indexed field (subject) = minimal overhead
- **Negligible impact** on database size

**Estimate:**
- 1000 ProcessingLogs = 50 KB additional storage
- Acceptable for production systems

---

## What Gets Stored in ProcessingLog

### For URL-based tasks (existing):
```python
{
    task_type: 'currentaffairs_mcq_fetch',
    status: 'completed',
    pdf_upload: None,  # Not used
    subject: None,  # Not used
    success_count: 5,
    error_message: None
}
```

### For PDF-based tasks (new):
```python
{
    task_type: 'pdf_to_economics',
    status: 'completed',
    pdf_upload: <PDFUpload object>,  # Points to uploaded PDF
    subject: 'economics',  # Specific subject
    difficulty_level: 'medium',  # For MCQs
    num_items: 15,  # Generated 15 items
    output_format: 'json',  # Output as JSON
    start_page: 1,  # Processed pages 1-10
    end_page: 10,
    success_count: 15,
    error_message: None
}
```

---

## Next Steps

1. ✅ Review this enhancement plan
2. ✅ Update ProcessingLog model (add 6 fields, 10 task types)
3. ✅ Run migrations
4. ✅ Update admin interface
5. ✅ Create new LLM prompts
6. ✅ Build PDF processing logic
7. ✅ Test full workflow

Ready to proceed?
