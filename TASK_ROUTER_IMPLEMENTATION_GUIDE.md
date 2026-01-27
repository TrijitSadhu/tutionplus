# Task Router Implementation Guide

## ✅ COMPLETED: 3 Files Created

### 1. genai/tasks/task_router.py ✅ CREATED
**Purpose:** Main router that bridges task_type → processor → database

**Key Functions:**
- `get_processor_for_task_type()` - Maps task_type to correct processor
- `get_llm_prompt_for_task()` - Fetches subject-specific LLM prompts from database
- `route_pdf_processing_task()` - Main routing logic (THE MISSING PIECE)
- `process_pending_tasks()` - CLI helper to process all pending tasks

**What It Does:**
```
ProcessingLog.task_type='pdf_to_polity'
       ↓
route_pdf_processing_task() reads task_type
       ↓
Selects PolityProcessor (not generic)
       ↓
Fetches 'pdf_to_polity_mcq' prompt from database
       ↓
Extracts PDF content
       ↓
Generates MCQs using PolityProcessor
       ↓
Saves to polity table (not 'total' table)
       ↓
Updates ProcessingLog with success_count
```

---

### 2. genai/tasks/subject_processor.py ✅ CREATED
**Purpose:** Subject-specific processor classes

**Classes:**
- `SubjectSpecificProcessor` - Base class extending SubjectMCQGenerator
- `PolityProcessor` - For Polity subjects
- `EconomicsProcessor` - For Economics subjects
- `MathProcessor` - For Mathematics subjects
- `PhysicsProcessor` - For Physics subjects
- `ChemistryProcessor` - For Chemistry subjects
- `HistoryProcessor` - For History subjects
- `GeographyProcessor` - For Geography subjects
- `BiologyProcessor` - For Biology subjects

Each processor automatically:
- Fetches subject-specific LLM prompts
- Applies subject-specific logic
- Saves to subject-specific tables

---

### 3. genai/management/commands/process_pdf_tasks.py ✅ CREATED
**Purpose:** CLI command to process pending tasks

**Usage:**
```bash
python manage.py process_pdf_tasks
```

**Output:**
```
Starting PDF task processing...
✓ Completed: 5 tasks
✓ Failed: 0 tasks
```

---

## 📋 NEXT STEPS: Files to MODIFY

### Step 1: Update ProcessingLog Model
**File:** `genai/models.py`

**Find this section (around line 114):**
```python
TASK_TYPES = (
    ('currentaffairs_mcq_fetch', 'Current Affairs MCQ'),
    ('currentaffairs_descriptive_fetch', 'Current Affairs Descriptive'),
    ...
)
```

**Add these 10 new TASK_TYPES:**
```python
TASK_TYPES = (
    ('currentaffairs_mcq_fetch', 'Current Affairs MCQ'),
    ('currentaffairs_descriptive_fetch', 'Current Affairs Descriptive'),
    ('both', 'Both MCQ & Descriptive'),
    ('pdf_currentaffairs_mcq', 'PDF - Current Affairs MCQ'),
    ('pdf_currentaffairs_descriptive', 'PDF - Current Affairs Descriptive'),
    # NEW SUBJECT-SPECIFIC TYPES:
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
)
```

**Add these 6 NEW FIELDS to ProcessingLog model:**
```python
class ProcessingLog(models.Model):
    # ... existing fields ...
    
    # NEW FIELDS FOR SUBJECT ROUTING:
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
```

---

### Step 2: Update views.py
**File:** `genai/views.py`

**Find `process_subject_pdf_view()` function (around line 91)**

**Replace with:**
```python
def process_subject_pdf_view(request):
    """Process subject PDF and generate MCQs/Descriptive using task router"""
    
    from genai.tasks.task_router import route_pdf_processing_task
    
    try:
        # Extract all parameters from request
        subject = request.POST.get('subject', 'other')
        task_type = request.POST.get('task_type', 'pdf_to_mcq')
        difficulty_level = request.POST.get('difficulty_level', 'medium')
        output_format = request.POST.get('output_format', 'json')
        num_items = int(request.POST.get('num_items', 5))
        start_page = request.POST.get('start_page', '')
        end_page = request.POST.get('end_page', '')
        
        start_page = int(start_page) if start_page else None
        end_page = int(end_page) if end_page else None
        
        # Get PDF file
        pdf_file = request.FILES.get('pdf_file')
        if not pdf_file:
            return JsonResponse({'success': False, 'error': 'No PDF file provided'}, status=400)
        
        # Create PDFUpload record
        pdf_upload = PDFUpload.objects.create(
            title=pdf_file.name,
            subject=subject,
            pdf_file=pdf_file,
            uploaded_by=request.user,
            status='processing'
        )
        
        # Create ProcessingLog with all task routing info
        log = ProcessingLog.objects.create(
            task_type=task_type,
            subject=subject,
            pdf_upload=pdf_upload,
            difficulty_level=difficulty_level,
            output_format=output_format,
            num_items=num_items,
            start_page=start_page,
            end_page=end_page,
            status='pending',
            created_by=request.user
        )
        
        # Route to appropriate processor (THIS IS THE KEY CHANGE!)
        result = route_pdf_processing_task(log)
        
        return JsonResponse({
            'success': result['success'],
            'task_id': log.id,
            'message': f"Generated {result.get('saved_items', 0)} items" if result['success'] else result.get('error')
        })
        
    except Exception as e:
        logger.error(f"Error in process_subject_pdf_view: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
```

---

### Step 3: Update admin.py
**File:** `genai/admin.py`

**Find `process_pdf_to_mcq()` action (around line 58)**

**Replace with:**
```python
def process_pdf_to_mcq(self, request, queryset):
    """Process selected PDFs as MCQ generation"""
    from genai.tasks.task_router import route_pdf_processing_task
    
    count = 0
    for pdf in queryset:
        try:
            # Create ProcessingLog with MCQ task type
            log = ProcessingLog.objects.create(
                task_type='pdf_to_mcq',
                subject=pdf.subject,
                pdf_upload=pdf,
                difficulty_level='medium',
                num_items=5,
                status='pending',
                created_by=request.user
            )
            
            # Route using the task router (THIS IS THE KEY CHANGE!)
            result = route_pdf_processing_task(log)
            
            if result['success']:
                count += 1
                
        except Exception as e:
            logger.error(f"Error processing PDF {pdf.id}: {str(e)}")
    
    self.message_user(
        request,
        self.style.SUCCESS(f"✓ Successfully processed {count} PDFs to MCQ")
    )
```

**Also add similar action for descriptive:**
```python
def process_pdf_to_descriptive(self, request, queryset):
    """Process selected PDFs as Descriptive generation"""
    from genai.tasks.task_router import route_pdf_processing_task
    
    count = 0
    for pdf in queryset:
        try:
            # Create ProcessingLog with Descriptive task type
            log = ProcessingLog.objects.create(
                task_type='pdf_to_descriptive',
                subject=pdf.subject,
                pdf_upload=pdf,
                difficulty_level='medium',
                output_format='markdown',
                num_items=5,
                status='pending',
                created_by=request.user
            )
            
            # Route using the task router
            result = route_pdf_processing_task(log)
            
            if result['success']:
                count += 1
                
        except Exception as e:
            logger.error(f"Error processing PDF {pdf.id}: {str(e)}")
    
    self.message_user(
        request,
        self.style.SUCCESS(f"✓ Successfully processed {count} PDFs to Descriptive")
    )
```

**Add to PDFUploadAdmin.actions:**
```python
class PDFUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_by', 'status', 'created_at')
    actions = ['process_pdf_to_mcq', 'process_pdf_to_descriptive']  # ADD THIS LINE
    # ... rest of admin config ...
```

---

### Step 4: Create Migration
**Run in terminal:**
```bash
cd c:\Users\newwe\Desktop\tution\tutionplus\django\django_project
python manage.py makemigrations genai
python manage.py migrate genai
```

---

### Step 5: Add LLM Prompts to Database
**Run in Django shell:**
```bash
python manage.py shell
```

**Then execute:**
```python
from genai.models import LLMPrompt

# Create subject-specific MCQ prompts
subjects = [
    ('polity', 'Polity'),
    ('economics', 'Economics'),
    ('math', 'Mathematics'),
    ('physics', 'Physics'),
    ('chemistry', 'Chemistry'),
    ('history', 'History'),
    ('geography', 'Geography'),
    ('biology', 'Biology'),
]

for slug, name in subjects:
    # MCQ prompt
    LLMPrompt.objects.create(
        source_url=f'pdf_{slug}_mcq',
        prompt_type='mcq',
        prompt_text=f"""You are an expert {name} teacher. Create 5 multiple choice questions based on the provided content.
        
Format as JSON:
[
    {{"question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "correct": "A"}},
    ...
]

Use ONLY the provided content. Do not add external information.""",
        is_active=True
    )
    
    # Descriptive prompt
    LLMPrompt.objects.create(
        source_url=f'pdf_{slug}_descriptive',
        prompt_type='descriptive',
        prompt_text=f"""You are an expert {name} teacher. Create 3 detailed descriptive answers based on the provided content.

Format as Markdown:
## Question 1
Answer...

## Question 2
Answer...

## Question 3
Answer...

Use ONLY the provided content. Do not add external information.""",
        is_active=True
    )

print("✓ Created prompts for all subjects")
```

---

## 🧪 Testing

### Test 1: Process a PDF via admin
1. Go to Django admin: `http://localhost:8000/admin/genai/pdfupload/`
2. Upload a PDF with subject='polity'
3. Select it, click "Process PDF to MCQ" action
4. Check ProcessingLog - should show `task_type='pdf_to_mcq'` and `status='completed'`

### Test 2: Process via management command
```bash
python manage.py process_pdf_tasks
```

### Test 3: Check database
```python
from genai.models import ProcessingLog
log = ProcessingLog.objects.latest('created_at')
print(f"Task Type: {log.task_type}")
print(f"Subject: {log.subject}")
print(f"Status: {log.status}")
print(f"Success Count: {log.success_count}")
```

---

## 📊 What Changed

| Component | Before | After |
|-----------|--------|-------|
| Task Type Handling | Ignored | ✅ Routes to correct processor |
| Subject Routing | None | ✅ Subject-specific processors |
| LLM Prompts | Generic only | ✅ Subject-specific prompts |
| Output Tables | Always 'total' | ✅ Subject-specific tables |
| Difficulty Level | Not used | ✅ Passed to processor |
| Page Range | Not used | ✅ Selective PDF processing |
| Admin Actions | Stubs | ✅ Fully functional |

---

## 🎯 Result

After these changes:

✅ `task_type='pdf_to_polity'` → Routes to PolityProcessor  
✅ Subject='polity' → Fetches polity-specific LLM prompt  
✅ Difficulty='hard' → Passed to processor  
✅ Results → Saved to polity table (not 'total')  
✅ ProcessingLog → Updated with success_count  
✅ created_by → Auto-filled from request.user  
✅ All 10 TASK_TYPES → Fully functional  

---

## 📝 Summary

**Files Created:**
- ✅ genai/tasks/task_router.py
- ✅ genai/tasks/subject_processor.py
- ✅ genai/management/commands/process_pdf_tasks.py

**Files to Modify:**
1. genai/models.py - Add 6 fields + 10 TASK_TYPES
2. genai/views.py - Pass task_type to router
3. genai/admin.py - Implement admin actions with router

**Migration Required:**
- Run makemigrations & migrate

**LLM Prompts to Add:**
- 16 new prompts (2 per subject × 8 subjects)

**Timeline:** 2-3 hours for all modifications + testing
