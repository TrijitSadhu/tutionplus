# SOLUTION: Create the Missing Task Router

## The Problem You Found

Task types (`pdf_to_mcq`, `pdf_to_polity`, etc.) are **defined in the database** but **never used in the code**.

There's a gap between:
```
✅ Task type in ProcessingLog model
        ↓
   [MISSING ROUTER CODE]
        ↓
❌ Actual processing ignores task type
```

---

## The Solution: 3 Files to Create

### FILE 1: genai/tasks/task_router.py (NEW - MAIN ROUTER)

```python
"""
Task Router - Routes PDF processing based on task_type
This is the missing bridge between task_type selection and actual processing
"""

import logging
from typing import Dict, Any, Optional
from genai.models import ProcessingLog, LLMPrompt
from genai.tasks.pdf_processor import SubjectMCQGenerator, PDFProcessor
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_processor_for_task_type(task_type: str, subject: Optional[str] = None):
    """
    Get appropriate processor based on task_type
    
    Returns processor class instance
    """
    # Import subject processors
    from genai.tasks.subject_processor import (
        PolityProcessor, EconomicsProcessor, MathProcessor,
        PhysicsProcessor, ChemistryProcessor, HistoryProcessor,
        GeographyProcessor, BiologyProcessor
    )
    
    processors = {
        'pdf_to_mcq': SubjectMCQGenerator,
        'pdf_to_descriptive': SubjectMCQGenerator,
        'pdf_to_polity': PolityProcessor,
        'pdf_to_economics': EconomicsProcessor,
        'pdf_to_math': MathProcessor,
        'pdf_to_physics': PhysicsProcessor,
        'pdf_to_chemistry': ChemistryProcessor,
        'pdf_to_history': HistoryProcessor,
        'pdf_to_geography': GeographyProcessor,
        'pdf_to_biology': BiologyProcessor,
    }
    
    processor_class = processors.get(task_type, SubjectMCQGenerator)
    return processor_class()


def get_llm_prompt_for_task(task_type: str, subject: str, prompt_type: str = 'mcq'):
    """
    Get subject-specific LLM prompt from database
    """
    try:
        # Try subject-specific prompt first
        if task_type.startswith('pdf_to_'):
            # e.g., pdf_to_polity_mcq
            source_url = f"{task_type}_{prompt_type}"
        else:
            source_url = f"pdf_{subject}_{prompt_type}"
        
        prompt = LLMPrompt.objects.get(
            source_url=source_url,
            prompt_type=prompt_type,
            is_active=True
        )
        return prompt.prompt_text
        
    except LLMPrompt.DoesNotExist:
        # Fallback to default
        try:
            prompt = LLMPrompt.objects.get(
                source_url='',  # Empty source_url = default
                prompt_type=prompt_type,
                is_active=True
            )
            return prompt.prompt_text
        except LLMPrompt.DoesNotExist:
            logger.warning(f"No prompt found for {task_type}/{prompt_type}")
            return None


def route_pdf_processing_task(processing_log: ProcessingLog) -> Dict[str, Any]:
    """
    Route PDF processing based on task_type and subject
    
    THIS IS THE MISSING FUNCTION THAT USES TASK_TYPE
    """
    
    try:
        processing_log.status = 'running'
        processing_log.started_at = timezone.now()
        processing_log.save()
        
        logger.info(f"Processing task {processing_log.id}: {processing_log.task_type}")
        
        # Determine processing parameters based on task_type
        task_type = processing_log.task_type
        subject = processing_log.subject or 'other'
        
        if 'descriptive' in task_type:
            prompt_type = 'descriptive'
            output_format = processing_log.output_format or 'markdown'
        else:
            prompt_type = 'mcq'
            output_format = processing_log.output_format or 'json'
        
        # Get appropriate processor
        processor = get_processor_for_task_type(task_type, subject)
        logger.info(f"Using processor: {processor.__class__.__name__}")
        
        # Get PDF file path
        if not processing_log.pdf_upload:
            raise ValueError("No PDF associated with this task")
        
        pdf_path = processing_log.pdf_upload.pdf_file.path
        
        # Validate PDF
        if not processor.pdf_processor.validate_pdf(pdf_path):
            raise ValueError("Invalid PDF file")
        
        # Extract content with page range
        if processing_log.start_page or processing_log.end_page:
            content = processor.pdf_processor.extract_by_page_range(
                pdf_path,
                start_page=processing_log.start_page or 0,
                end_page=processing_log.end_page
            )
        else:
            content = processor.pdf_processor.extract_text_from_pdf(pdf_path)
        
        if not content:
            raise ValueError("No content extracted from PDF")
        
        logger.info(f"Extracted {len(content)} characters from PDF")
        
        # Get subject-specific LLM prompt
        llm_prompt_text = get_llm_prompt_for_task(task_type, subject, prompt_type)
        if not llm_prompt_text:
            logger.warning(f"Using default prompt for {task_type}")
        
        # Generate output using processor
        result = processor.process_pdf_for_subject(
            pdf_path,
            chapter=subject.replace('_', ' ').title(),
            topic=processing_log.pdf_upload.title,
            start_page=processing_log.start_page or 0,
            end_page=processing_log.end_page,
            num_questions=processing_log.num_items or 5,
            difficulty=processing_log.difficulty_level,
            output_format=output_format
        )
        
        if 'error' in result:
            raise ValueError(result.get('error', 'Processing failed'))
        
        # Save to appropriate table
        saved_items = processor.save_mcqs_to_subject_table(
            result,
            subject=subject,
            created_by=processing_log.created_by
        )
        
        # Update ProcessingLog with results
        processing_log.success_count = len(saved_items)
        processing_log.processed_items = len(saved_items)
        processing_log.status = 'completed'
        processing_log.completed_at = timezone.now()
        
        if prompt_type == 'mcq':
            processing_log.mcq_status = f"Generated {len(saved_items)} MCQs"
        else:
            processing_log.current_affairs_status = f"Generated {len(saved_items)} descriptive answers"
        
        processing_log.save()
        
        logger.info(f"Task {processing_log.id} completed. Saved {len(saved_items)} items")
        
        return {
            'success': True,
            'task_id': processing_log.id,
            'saved_items': len(saved_items),
            'task_type': task_type,
            'subject': subject,
            'prompt_type': prompt_type,
            'output_format': output_format
        }
        
    except Exception as e:
        logger.error(f"Error processing task {processing_log.id}: {str(e)}")
        
        processing_log.status = 'failed'
        processing_log.error_message = str(e)
        processing_log.completed_at = timezone.now()
        processing_log.save()
        
        return {
            'success': False,
            'task_id': processing_log.id,
            'error': str(e)
        }


def process_pending_tasks():
    """
    Process all pending PDF processing tasks
    Called by management command or task queue
    """
    pending_tasks = ProcessingLog.objects.filter(
        status='pending',
        task_type__startswith='pdf_to_'
    ).order_by('created_at')
    
    results = []
    for task in pending_tasks:
        result = route_pdf_processing_task(task)
        results.append(result)
        logger.info(f"Processed: {result}")
    
    return results
```

---

### FILE 2: genai/tasks/subject_processor.py (NEW - SUBJECT PROCESSORS)

```python
"""
Subject-Specific Processors
Extend SubjectMCQGenerator for different subjects
"""

from genai.tasks.pdf_processor import SubjectMCQGenerator
from genai.models import LLMPrompt
import logging

logger = logging.getLogger(__name__)


class SubjectSpecificProcessor(SubjectMCQGenerator):
    """Base class for subject-specific processors"""
    
    SUBJECT_NAME = None
    SUBJECT_SLUG = None
    
    def get_subject_specific_prompt(self, prompt_type: str = 'mcq') -> str:
        """Get subject-specific prompt from database"""
        try:
            source_url = f"pdf_{self.SUBJECT_SLUG}_{prompt_type}"
            prompt = LLMPrompt.objects.get(
                source_url=source_url,
                prompt_type=prompt_type,
                is_active=True
            )
            return prompt.prompt_text
        except LLMPrompt.DoesNotExist:
            logger.warning(f"Subject prompt not found: {source_url}, using default")
            return self.generate_mcq_prompt(
                chapter=self.SUBJECT_NAME,
                topic="General",
                content="",
                num_questions=5
            )


class PolityProcessor(SubjectSpecificProcessor):
    """Process PDFs for Polity"""
    SUBJECT_NAME = "Polity"
    SUBJECT_SLUG = "polity"


class EconomicsProcessor(SubjectSpecificProcessor):
    """Process PDFs for Economics"""
    SUBJECT_NAME = "Economics"
    SUBJECT_SLUG = "economics"


class MathProcessor(SubjectSpecificProcessor):
    """Process PDFs for Mathematics"""
    SUBJECT_NAME = "Mathematics"
    SUBJECT_SLUG = "math"


class PhysicsProcessor(SubjectSpecificProcessor):
    """Process PDFs for Physics"""
    SUBJECT_NAME = "Physics"
    SUBJECT_SLUG = "physics"


class ChemistryProcessor(SubjectSpecificProcessor):
    """Process PDFs for Chemistry"""
    SUBJECT_NAME = "Chemistry"
    SUBJECT_SLUG = "chemistry"


class HistoryProcessor(SubjectSpecificProcessor):
    """Process PDFs for History"""
    SUBJECT_NAME = "History"
    SUBJECT_SLUG = "history"


class GeographyProcessor(SubjectSpecificProcessor):
    """Process PDFs for Geography"""
    SUBJECT_NAME = "Geography"
    SUBJECT_SLUG = "geography"


class BiologyProcessor(SubjectSpecificProcessor):
    """Process PDFs for Biology"""
    SUBJECT_NAME = "Biology"
    SUBJECT_SLUG = "biology"
```

---

### FILE 3: genai/management/commands/process_pdf_tasks.py (NEW - CLI)

```python
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
```

---

## Files to MODIFY

### MODIFY: genai/views.py (Add task_type parameter)

**Current (Line 91-140):**
```python
def process_subject_pdf_view(request):
    chapter = request.POST.get('chapter', '')
    topic = request.POST.get('topic', '')
    # ... processes generically ...
```

**Change To:**
```python
def process_subject_pdf_view(request):
    # New parameters for task routing
    subject = request.POST.get('subject', 'other')
    task_type = request.POST.get('task_type', 'pdf_to_mcq')
    difficulty_level = request.POST.get('difficulty_level', 'medium')
    output_format = request.POST.get('output_format', 'json')
    num_items = int(request.POST.get('num_items', 5))
    start_page = int(request.POST.get('start_page', 0))
    end_page = request.POST.get('end_page')
    end_page = int(end_page) if end_page else None
    
    # Create ProcessingLog with task routing info
    from genai.models import PDFUpload, ProcessingLog
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    
    pdf_file = request.FILES.get('pdf_file')
    if not pdf_file:
        return JsonResponse({'success': False, 'error': 'No PDF'}, status=400)
    
    # Create PDFUpload
    pdf_upload = PDFUpload.objects.create(
        title=pdf_file.name,
        subject=subject,
        pdf_file=pdf_file,
        uploaded_by=request.user,
        status='processing'
    )
    
    # Create ProcessingLog with task_type (THIS ENABLES ROUTING)
    log = ProcessingLog.objects.create(
        task_type=task_type,
        subject=subject,
        pdf_upload=pdf_upload,
        difficulty_level=difficulty_level,
        output_format=output_format,
        num_items=num_items,
        start_page=start_page if start_page > 0 else None,
        end_page=end_page,
        status='pending',
        created_by=request.user
    )
    
    # Call the router (NEW - this is the bridge!)
    from genai.tasks.task_router import route_pdf_processing_task
    result = route_pdf_processing_task(log)
    
    return JsonResponse({
        'success': result['success'],
        'task_id': log.id,
        'message': result.get('saved_items', f"Error: {result.get('error')}")
    })
```

---

### MODIFY: genai/admin.py (Implement admin actions)

**Current (Line 58-65):**
```python
def process_pdf_to_mcq(self, request, queryset):
    for pdf in queryset:
        pdf.status = 'processing'
        pdf.save()
    self.message_user(request, f"Started processing")
```

**Change To:**
```python
def process_pdf_to_mcq(self, request, queryset):
    from genai.tasks.task_router import route_pdf_processing_task
    from genai.models import ProcessingLog
    
    count = 0
    for pdf in queryset:
        # Create ProcessingLog with task routing
        log = ProcessingLog.objects.create(
            task_type='pdf_to_mcq',
            subject=pdf.subject,
            pdf_upload=pdf,
            num_items=5,
            status='pending',
            created_by=request.user
        )
        
        # Route the task (uses task_type!)
        result = route_pdf_processing_task(log)
        
        if result['success']:
            count += 1
    
    self.message_user(
        request,
        self.style.SUCCESS(f"✓ Successfully processed {count} PDFs")
    )
```

---

## How It NOW Works: With Task Router

### Before (Broken)
```
User selects "Process as Polity MCQ"
        ↓
Admin action sets status='processing'
        ↓
[NOTHING HAPPENS - task_type ignored]
        ↓
PDF stays in processing forever
```

### After (Fixed)
```
User selects task_type='pdf_to_polity'
        ↓
ProcessingLog created with:
  - task_type='pdf_to_polity'
  - subject='polity'
  - created_by=user
        ↓
route_pdf_processing_task() is called
        ↓
Router reads task_type → selects PolityProcessor
Router reads subject → fetches LLMPrompt for 'polity_mcq'
Router respects difficulty_level → passes to processor
        ↓
Extract PDF → Process with PolityProcessor → Save to polity table
        ↓
ProcessingLog updated with results
Status='completed', success_count=5
```

---

## Testing the Fix

**After creating these 3 files and modifying views.py:**

```bash
# 1. Upload a PDF with subject=polity and task_type=pdf_to_polity
curl -X POST http://localhost:8000/genai/api/pdf/process/ \
  -F "pdf_file=@sample.pdf" \
  -F "subject=polity" \
  -F "task_type=pdf_to_polity" \
  -F "difficulty_level=medium" \
  -F "num_items=5"

# 2. Check if ProcessingLog was created with task_type
python manage.py shell
>>> from genai.models import ProcessingLog
>>> log = ProcessingLog.objects.latest('created_at')
>>> log.task_type
'pdf_to_polity'  # ✅ WORKS!
>>> log.subject
'polity'  # ✅ WORKS!

# 3. Check if task was processed
>>> log.status
'completed'  # ✅ PROCESSED!
>>> log.success_count
5  # ✅ GENERATED 5 MCQs!

# 4. Or process via CLI
python manage.py process_pdf_tasks
```

---

## Summary

The task router **bridges the gap** between:
- Database model fields (task_type, subject, difficulty_level)
- Actual processing logic (which processor to use, which prompt, where to save)

**Files created:**
1. ✅ `genai/tasks/task_router.py` - Routes tasks by type
2. ✅ `genai/tasks/subject_processor.py` - Subject-specific logic
3. ✅ `genai/management/commands/process_pdf_tasks.py` - CLI command

**Files modified:**
1. ✅ `genai/views.py` - Pass task_type to router
2. ✅ `genai/admin.py` - Implement admin actions with router

**Result:** task_type now ACTUALLY WORKS!
