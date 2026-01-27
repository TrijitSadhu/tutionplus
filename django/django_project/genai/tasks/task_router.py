"""
Task Router - Routes PDF processing based on task_type
This is the missing bridge between task_type selection and actual processing
"""

import json
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
    print("\n" + "="*80)
    print(f"[ROUTER] get_processor_for_task_type()")
    print(f"  INPUT: task_type='{task_type}', subject='{subject}'")
    print("="*80)
    
    # Import subject processors
    from genai.tasks.subject_processor import (
        PolityProcessor, EconomicsProcessor, MathProcessor,
        PhysicsProcessor, ChemistryProcessor, HistoryProcessor,
        GeographyProcessor, BiologyProcessor
    )
    from genai.tasks.pdf_processor import CurrentAffairsProcessor
    
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
        'pdf_currentaffairs_mcq': CurrentAffairsProcessor,
        'pdf_currentaffairs_descriptive': CurrentAffairsProcessor,
    }
    
    processor_class = processors.get(task_type, SubjectMCQGenerator)
    print(f"  SELECTED PROCESSOR: {processor_class.__name__}")
    print(f"  OUTPUT: Processor instance created\n")
    return processor_class()


def get_llm_prompt_for_task(task_type: str, subject: str, prompt_type: str = 'mcq'):
    """
    Get subject-specific LLM prompt from database
    """
    print("\n" + "-"*80)
    print(f"[ROUTER] get_llm_prompt_for_task()")
    print(f"  INPUT: task_type='{task_type}', subject='{subject}', prompt_type='{prompt_type}'")
    print("-"*80)
    
    try:
        # Try subject-specific prompt first
        if task_type.startswith('pdf_to_'):
            # e.g., pdf_to_mcq_polity or pdf_to_descriptive_computer
            source_url = f"{task_type}_{subject}"
        else:
            source_url = f"pdf_{subject}_{prompt_type}"
        
        print(f"  SEARCHING: Prompt with source_url='{source_url}'")
        
        prompt = LLMPrompt.objects.get(
            source_url=source_url,
            prompt_type=prompt_type,
            is_active=True
        )
        print(f"  FOUND: ✓ Prompt loaded (length: {len(prompt.prompt_text)} chars)")
        print(f"  OUTPUT: Prompt text returned\n")
        return prompt.prompt_text
        
    except LLMPrompt.DoesNotExist:
        print(f"  NOT FOUND: Specific prompt not found, trying default...")
        # Fallback to default
        try:
            prompt = LLMPrompt.objects.get(
                source_url='',  # Empty source_url = default
                prompt_type=prompt_type,
                is_active=True
            )
            print(f"  FOUND: ✓ Default prompt loaded")
            print(f"  OUTPUT: Default prompt returned\n")
            return prompt.prompt_text
        except LLMPrompt.DoesNotExist:
            print(f"  ERROR: ✗ No prompt found for {task_type}/{prompt_type}")
            logger.warning(f"No prompt found for {task_type}/{prompt_type}")
            return None


def route_pdf_processing_task(processing_log: ProcessingLog) -> Dict[str, Any]:
    """
    Route PDF processing based on task_type and subject
    
    THIS IS THE MISSING FUNCTION THAT USES TASK_TYPE
    """
    
    print("\n" + "="*80)
    print(f"🚀 [ROUTER] route_pdf_processing_task() - MAIN ENTRY POINT")
    print("="*80)
    print(f"INPUT:")
    print(f"  task_type: {processing_log.task_type}")
    print(f"  subject: {processing_log.subject}")
    print(f"  difficulty: {processing_log.difficulty_level}")
    print(f"  output_format: {processing_log.output_format}")
    print(f"  num_items: {processing_log.num_items}")
    print(f"  pdf_file: {processing_log.pdf_upload.pdf_file.name if processing_log.pdf_upload else 'NONE'}")
    print("="*80 + "\n")
    
    try:
        processing_log.status = 'running'
        processing_log.started_at = timezone.now()
        processing_log.save()
        print(f"[STEP 1] Status updated to 'running'\n")
        
        logger.info(f"Processing task {processing_log.id}: {processing_log.task_type}")
        
        # Determine processing parameters based on task_type
        task_type = processing_log.task_type
        subject = processing_log.subject or 'other'
        
        print(f"[STEP 2] Determining prompt type...")
        if 'descriptive' in task_type:
            prompt_type = 'descriptive'
            output_format = processing_log.output_format or 'markdown'
        else:
            prompt_type = 'mcq'
            output_format = processing_log.output_format or 'json'
        print(f"  prompt_type: {prompt_type}, output_format: {output_format}\n")
        
        # Get appropriate processor
        print(f"[STEP 3] Getting processor for task_type...")
        processor = get_processor_for_task_type(task_type, subject)
        logger.info(f"Using processor: {processor.__class__.__name__}")
        
        # Get PDF file path
        print(f"[STEP 4] Validating PDF file...")
        if not processing_log.pdf_upload:
            raise ValueError("No PDF associated with this task")
        
        pdf_path = processing_log.pdf_upload.pdf_file.path
        print(f"  PDF path: {pdf_path}\n")
        
        # Validate PDF
        print(f"[STEP 5] Validating PDF...")
        if not processor.pdf_processor.validate_pdf(pdf_path):
            raise ValueError("Invalid PDF file")
        print(f"  ✓ PDF validation passed\n")
        
        # Extract content with page range
        print(f"[STEP 6] Extracting PDF content...")
        if processing_log.start_page or processing_log.end_page:
            print(f"  Range mode: pages {processing_log.start_page} to {processing_log.end_page}")
            content = processor.pdf_processor.extract_by_page_range(
                pdf_path,
                start_page=processing_log.start_page or 0,
                end_page=processing_log.end_page
            )
        else:
            print(f"  Full PDF extraction mode")
            content = processor.pdf_processor.extract_text_from_pdf(pdf_path)
        
        if not content:
            raise ValueError("No content extracted from PDF")
        
        print(f"  ✓ Extracted {len(content)} characters\n")
        logger.info(f"Extracted {len(content)} characters from PDF")
        
        # Get subject-specific LLM prompt
        print(f"[STEP 7] Fetching LLM prompt...")
        llm_prompt_text = get_llm_prompt_for_task(task_type, subject, prompt_type)
        if not llm_prompt_text:
            logger.warning(f"Using default prompt for {task_type}")
            print(f"  WARNING: Using default prompt\n")
        else:
            print(f"  ✓ Prompt loaded ({len(llm_prompt_text)} chars)\n")
        
        # ==================== HANDLE CURRENT AFFAIRS TASKS ====================
        if task_type == 'pdf_currentaffairs_mcq':
            print(f"[STEP 8] Processing PDF with Current Affairs MCQ processor...")
            result = processor.process_currentaffairs_mcq(
                pdf_path,
                num_questions=processing_log.num_items or 5,
                start_page=processing_log.start_page or 0,
                end_page=processing_log.end_page
            )
            
            if 'error' in result:
                raise ValueError(result.get('error', 'Processing failed'))
            
            print(f"  ✓ Processing complete\n")
            
            # Save to currentaffairs_mcq table
            print(f"[STEP 9] Saving results to database...")
            from genai.tasks.save_handlers import save_currentaffairs_mcq
            saved_items = save_currentaffairs_mcq(
                result,
                processing_log=processing_log,
                created_by=processing_log.created_by
            )
            
            print(f"  ✓ Saved {len(saved_items)} MCQs to database\n")
        
        elif task_type == 'pdf_currentaffairs_descriptive':
            print(f"[STEP 8] Processing PDF with Current Affairs Descriptive processor...")
            result = processor.process_currentaffairs_descriptive(
                pdf_path,
                start_page=processing_log.start_page or 0,
                end_page=processing_log.end_page
            )
            
            if 'error' in result:
                raise ValueError(result.get('error', 'Processing failed'))
            
            print(f"  ✓ Processing complete\n")
            
            # Save to currentaffairs_descriptive table
            print(f"[STEP 9] Saving results to database...")
            from genai.tasks.save_handlers import save_currentaffairs_descriptive
            saved_items = save_currentaffairs_descriptive(
                result,
                processing_log=processing_log,
                created_by=processing_log.created_by
            )
            
            print(f"  ✓ Saved descriptive content to database\n")
        
        # ==================== HANDLE SUBJECT-BASED TASKS ====================
        else:
            # Generate output using processor
            print(f"[STEP 8] Processing PDF with subject processor...")
            result = processor.process_pdf_for_subject(
                pdf_path,
                chapter=subject.replace('_', ' ').title(),
                topic=processing_log.pdf_upload.title,
                start_page=processing_log.start_page or 0,
                end_page=processing_log.end_page,
                num_questions=processing_log.num_items or 5,
                difficulty=processing_log.difficulty_level,
                output_format=output_format,
                subject=subject,
                task_type=processing_log.task_type
            )
            
            if 'error' in result:
                raise ValueError(result.get('error', 'Processing failed'))
            
            print(f"  ✓ Processing complete\n")
            
            # Extract chapter from log_details if available
            chapter = None
            if processing_log.log_details:
                try:
                    log_data = json.loads(processing_log.log_details)
                    chapter = log_data.get('chapter')
                except (json.JSONDecodeError, TypeError):
                    pass
            
            # Save to appropriate table
            print(f"[STEP 9] Saving results to database...")
            saved_items = processor.save_mcqs_to_subject_table(
                result,
                subject=subject,
                created_by=processing_log.created_by,
                chapter=chapter,
                difficulty=processing_log.difficulty_level
            )
            
            print(f"  ✓ Saved {len(saved_items)} items to database\n")
        
        # Update ProcessingLog with results
        print(f"[STEP 10] Updating ProcessingLog status...")
        processing_log.success_count = len(saved_items)
        processing_log.processed_items = len(saved_items)
        processing_log.status = 'completed'
        processing_log.completed_at = timezone.now()
        
        if prompt_type == 'mcq':
            processing_log.mcq_status = f"Generated {len(saved_items)} MCQs"
        else:
            processing_log.current_affairs_status = f"Generated {len(saved_items)} descriptive answers"
        
        processing_log.save()
        print(f"  ✓ Status updated to 'completed'\n")
        
        logger.info(f"Task {processing_log.id} completed. Saved {len(saved_items)} items")
        
        print("="*80)
        print(f"✅ TASK COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"OUTPUT:")
        print(f"  task_id: {processing_log.id}")
        print(f"  items_saved: {len(saved_items)}")
        print(f"  task_type: {task_type}")
        print(f"  subject: {subject}")
        print(f"  prompt_type: {prompt_type}")
        print(f"  output_format: {output_format}")
        print("="*80 + "\n")
        
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
        
        print("\n" + "="*80)
        print(f"❌ ERROR IN TASK PROCESSING")
        print("="*80)
        print(f"  task_id: {processing_log.id}")
        print(f"  error: {str(e)}")
        print("="*80 + "\n")
        
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
