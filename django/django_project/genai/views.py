"""
GenAI Views
API endpoints for GenAI tasks
"""

import logging
import json
import os
import re
import tempfile
import shutil
import subprocess
import threading
import time
import uuid
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

from genai.tasks.current_affairs import fetch_and_process_current_affairs
from genai.tasks.pdf_processor import process_subject_pdf
from genai.tasks.math_processor import process_math_problem, batch_process_math_problems
from genai.models import ProcessingLog, MathProblemGeneration, LLMPrompt, JsonImport
from genai.forms import MathPDFProcessingForm, MathPromptGenerationForm, MathPromptRowFormSet

logger = logging.getLogger(__name__)

# Custom decorator for staff-only views
def staff_required(view_func):
    """Decorator to require staff status"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'error': 'Staff access required'}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_exempt
@require_http_methods(["POST"])
def process_current_affairs_mcq(request):
    """
    Fetch and process current affairs MCQs
    
    POST data:
    - (optional) sources: List of URLs to scrape
    """
    try:
        data = json.loads(request.body) if request.body else {}
        
        logger.info("Starting current affairs MCQ processing")
        result = fetch_and_process_current_affairs('mcq')
        
        return JsonResponse({
            'success': True,
            'message': 'Current affairs MCQ processing completed',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"Error in process_current_affairs_mcq: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def process_current_affairs_descriptive(request):
    """
    Fetch and process current affairs descriptive content
    """
    try:
        logger.info("Starting current affairs descriptive processing")
        result = fetch_and_process_current_affairs('descriptive')
        
        return JsonResponse({
            'success': True,
            'message': 'Current affairs descriptive processing completed',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"Error in process_current_affairs_descriptive: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def process_subject_pdf_view(request):
    """
    Process subject PDF and generate MCQs/Descriptive using task router
    
    POST data:
    - pdf_file: File upload (REQUIRED)
    - subject: Subject name (polity, economics, math, etc.)
    - task_type: Task type for routing (pdf_to_polity, pdf_to_economics, etc.)
    - difficulty_level: easy, medium, hard
    - output_format: json, markdown, text
    - num_items: Number of MCQs/descriptive answers
    - start_page: (optional) Starting page
    - end_page: (optional) Ending page
    """
    try:
        from genai.tasks.task_router import route_pdf_processing_task
        from genai.models import PDFUpload, ProcessingLog
        
        print("\n" + "═"*80)
        print("[VIEW] process_subject_pdf_view()")
        print("═"*80)
        
        # Handle file upload
        if 'pdf_file' not in request.FILES:
            print("  ❌ ERROR: No PDF file provided\n")
            return JsonResponse({
                'success': False,
                'error': 'No PDF file provided'
            }, status=400)
        
        pdf_file = request.FILES['pdf_file']
        print(f"  FILE: {pdf_file.name} ({pdf_file.size} bytes)")
        
        # Extract all parameters from request
        subject = request.POST.get('subject', 'other')
        task_type = request.POST.get('task_type', 'pdf_to_mcq')
        difficulty_level = request.POST.get('difficulty_level', 'medium')
        output_format = request.POST.get('output_format', 'json')
        num_items = int(request.POST.get('num_items', 5))
        start_page = request.POST.get('start_page', '')
        end_page = request.POST.get('end_page', '')
        
        print(f"  PARAMS: subject={subject}, task_type={task_type}")
        print(f"          difficulty={difficulty_level}, format={output_format}, items={num_items}")
        
        start_page = int(start_page) if start_page else None
        end_page = int(end_page) if end_page else None
        
        if start_page or end_page:
            print(f"          page_range={start_page}-{end_page}")
        
        print("  Creating PDFUpload record...")
        
        # Create PDFUpload record
        pdf_upload = PDFUpload.objects.create(
            title=pdf_file.name,
            subject=subject,
            pdf_file=pdf_file,
            uploaded_by=request.user if request.user.is_authenticated else None,
            status='processing'
        )
        
        print(f"  ✅ PDFUpload created: ID={pdf_upload.id}")
        
        print("  Creating ProcessingLog record...")
        
        # Create ProcessingLog with task routing info
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
            created_by=request.user if request.user.is_authenticated else None
        )
        
        print(f"  ✅ ProcessingLog created: ID={log.id}")
        print(f"  Routing to task processor...")
        
        # Route to appropriate processor (THIS IS THE KEY CHANGE!)
        result = route_pdf_processing_task(log)
        
        print(f"  ✅ Route completed: success={result['success']}")
        print(f"  OUTPUT: saved_items={result.get('saved_items', 0)}\n")
        
        return JsonResponse({
            'success': result['success'],
            'task_id': log.id,
            'message': f"Generated {result.get('saved_items', 0)} items" if result['success'] else result.get('error'),
            'data': {
                'task_type': result.get('task_type'),
                'subject': result.get('subject'),
                'saved_items': result.get('saved_items', 0)
            }
        })
        
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}\n")
        logger.error(f"Error in process_subject_pdf_view: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def process_math_problem_view(request):
    """
    Process math problem and generate MCQ with LaTeX
    
    POST data:
    - problem: Math problem statement
    - difficulty: (optional) Easy/Medium/Hard
    """
    try:
        data = json.loads(request.body) if request.body else {}
        
        problem = data.get('problem', '')
        difficulty = data.get('difficulty', 'Medium')
        
        if not problem:
            return JsonResponse({
                'success': False,
                'error': 'Problem statement required'
            }, status=400)
        
        logger.info(f"Processing math problem: {problem[:50]}...")
        result = process_math_problem(problem, difficulty)
        
        return JsonResponse({
            'success': True,
            'message': 'Math problem processing completed',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"Error in process_math_problem_view: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def batch_process_math_view(request):
    """
    Batch process multiple math problems
    
    POST data:
    - problems: List of math problems
    - chapter: Chapter name
    - difficulty: (optional) Difficulty level
    """
    try:
        data = json.loads(request.body) if request.body else {}
        
        problems = data.get('problems', [])
        chapter = data.get('chapter', 'General')
        difficulty = data.get('difficulty', 'Medium')
        
        if not problems:
            return JsonResponse({
                'success': False,
                'error': 'List of problems required'
            }, status=400)
        
        logger.info(f"Batch processing {len(problems)} math problems")
        result = batch_process_math_problems(problems, chapter, difficulty)
        
        return JsonResponse({
            'success': True,
            'message': f'Batch processing completed ({len(problems)} problems)',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"Error in batch_process_math_view: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def genai_status(request):
    """Get GenAI system status"""
    return JsonResponse({
        'status': 'active',
        'available_tasks': [
            'current_affairs_mcq',
            'currentaffairs_descriptive',
            'subject_pdf_processing',
            'math_problem_processing',
            'batch_math_processing'
        ]
    })


@staff_required
def processing_dashboard(request):
    """Dashboard to view and trigger processing tasks"""
    
    # Get recent processing logs
    recent_logs = ProcessingLog.objects.all()[:20]
    
    # Get statistics
    stats = {
        'total_tasks': ProcessingLog.objects.count(),
        'completed': ProcessingLog.objects.filter(status='completed').count(),
        'running': ProcessingLog.objects.filter(status='running').count(),
        'failed': ProcessingLog.objects.filter(status='failed').count(),
        'pending': ProcessingLog.objects.filter(status='pending').count(),
    }
    
    # Get latest task
    latest_task = ProcessingLog.objects.first()
    
    context = {
        'recent_logs': recent_logs,
        'stats': stats,
        'latest_task': latest_task,
        'title': 'Processing Dashboard',
    }
    
    return render(request, 'genai/admin/processing_dashboard.html', context)


@staff_required
@require_http_methods(["POST"])
def trigger_fetch(request):
    """
    Trigger fetch task for MCQ and/or Current Affairs
    POST params:
    - task_type: 'currentaffairs_mcq', 'currentaffairs_descriptive', or 'both'
    """
    try:
        task_type = request.POST.get('task_type', 'both')
        
        # Validate task type
        if task_type not in ['currentaffairs_mcq', 'currentaffairs_descriptive', 'both']:
            return JsonResponse({
                'success': False,
                'error': 'Invalid task type'
            }, status=400)
        
        # Run management command
        command = f'python manage.py fetch_all_content --type={task_type}'
        
        logger.info(f"Triggering fetch: {command}")
        
        # Create log entry
        log_entry = ProcessingLog.objects.create(
            task_type='both' if task_type == 'both' else f'{task_type}_fetch',
            status='pending',
        )
        
        # Run async if possible, else run synchronously
        try:
            # For synchronous execution (blocking)
            result = subprocess.run(
                command,
                shell=True,
                cwd='/c:/Users/newwe/Desktop/tution/tutionplus/django/django_project',
                capture_output=True,
                text=True,
                timeout=300
            )
            
            return JsonResponse({
                'success': result.returncode == 0,
                'message': 'Fetch task completed',
                'task_id': log_entry.id,
                'output': result.stdout[:500] if result.stdout else '',
                'error': result.stderr[:500] if result.stderr else '',
            })
        
        except subprocess.TimeoutExpired:
            log_entry.status = 'failed'
            log_entry.error_message = 'Task timed out after 5 minutes'
            log_entry.completed_at = timezone.now()
            log_entry.save()
            
            return JsonResponse({
                'success': False,
                'error': 'Task timed out after 5 minutes',
                'task_id': log_entry.id,
            }, status=408)
    
    except Exception as e:
        logger.error(f"Error triggering fetch: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@staff_required
def task_status(request, task_id):
    """Get status of a processing task"""
    try:
        task = ProcessingLog.objects.get(id=task_id)
        
        return JsonResponse({
            'id': task.id,
            'status': task.status,
            'task_type': task.get_task_type_display(),
            'progress': task.progress_percentage,
            'processed': task.processed_items,
            'total': task.total_items,
            'success_count': task.success_count,
            'error_count': task.error_count,
            'mcq_status': task.mcq_status,
            'current_affairs_status': task.current_affairs_status,
            'duration': task.duration,
            'created_at': task.created_at.isoformat(),
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'error_message': task.error_message,
        })
    
    except ProcessingLog.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Task not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error getting task status: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# Math PDF Processing Views

@staff_member_required
def math_pdf_processing_form(request, pk):
    """
    Intermediate form for configuring PDF processing options
    Accessed via the GO button in admin
    """
    math_problem = get_object_or_404(MathProblemGeneration, pk=pk)
    
    if request.method == 'POST':
        # Build prompt choices needed for form validation (populated after form build below)
        from genai.models import LLMPrompt as LLMPromptModel
        from genai.config import DEFAULT_LLM_PROVIDER, GROQ_MODEL, GROQ_TEMPERATURE, GEMINI_MODEL, OPENAI_MODEL
        _prompt_qs_post = LLMPromptModel.objects.filter(is_active=True).order_by('-is_default', 'prompt_type', 'source_url')
        _prompt_choices_post = [('', '— Auto (use default) —')] + [
            (str(p.id), f"[{p.get_prompt_type_display()}] {str(p)}")
            for p in _prompt_qs_post
        ]
        from bank.models import RULE_NAME_CHOICES
        _rule_choices_post = [('', '— Select Rule —')] + list(RULE_NAME_CHOICES)
        form = MathPDFProcessingForm(request.POST, prompt_choices=_prompt_choices_post, rule_choices=_rule_choices_post)

        if form.is_valid():
            print(f"\n{'='*80}")
            print(f"[MATH PDF PROCESSING] Starting for ID: {pk}")
            print(f"{'='*80}\n")
            
            # Extract form data
            config = {
                'chapter_decide_by_llm': form.cleaned_data['chapter_decide_by_llm'],
                'difficulty_level_decide_by_llm': form.cleaned_data['difficulty_level_decide_by_llm'],
                'use_paddle_ocr': form.cleaned_data['use_paddle_ocr'],
                'use_easy_ocr': form.cleaned_data['use_easy_ocr'],
                'use_tesseract': form.cleaned_data['use_tesseract'],
                'process_pdf': form.cleaned_data['process_pdf'],
                'page_from': form.cleaned_data['page_from'],
                'page_to': form.cleaned_data['page_to'],
                'process_all_the_mcq_of_the_pageRange': form.cleaned_data['process_all_the_mcq_of_the_pageRange'],
                'no_of_pages_at_a_time_For_EntirePDF': form.cleaned_data['no_of_pages_at_a_time_For_EntirePDF'],
                'process_all_the_mcq_all_pages': form.cleaned_data['process_all_the_mcq_all_pages'],
                'pdf_prompt_id': form.cleaned_data.get('pdf_prompt') or None,
                'expression_prompt_id': form.cleaned_data.get('expression_prompt') or None,
                'extract_rule': form.cleaned_data.get('extract_rule', False),
                'rule_number': form.cleaned_data.get('rule_number') or None,
            }
            
            print(f"[CONFIG] Processing Configuration:")
            for key, value in config.items():
                print(f"  {key}: {value}")
            print()
            
            # Create ProcessingLog entry
            log_entry = ProcessingLog.objects.create(
                task_type='math_pdf_to_mcq',
                status='pending',
                log_details=json.dumps({
                    'math_problem_id': pk,
                    'config': config,
                    'has_pdf': bool(math_problem.pdf_file),
                    'has_expression': bool(math_problem.expression),
                })
            )
            
            # Update math problem status
            math_problem.status = 'processing'
            math_problem.save()
            
            # Process synchronously
            try:
                from genai.tasks.math_processor import MathPDFProcessor
                processor = MathPDFProcessor()
                result = processor.process_math_problem_with_config(
                    math_problem=math_problem,
                    config=config,
                    log_entry=log_entry
                )
                
                if result.get('success'):
                    if config.get('extract_rule'):
                        messages.success(request, f"✅ Rule extracted and saved: {result.get('rule_name', '')} for chapter {result.get('chapter', '')}.")
                    else:
                        messages.success(request, f"✅ Successfully processed math problem. Generated {result.get('mcq_count', 0)} MCQs.")
                else:
                    messages.error(request, f"❌ Processing failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f"❌ Unexpected error: {str(e)}")
                math_problem.status = 'failed'
                math_problem.error_message = str(e)
                math_problem.save()
                
                log_entry.status = 'failed'
                log_entry.error_message = str(e)
                log_entry.save()
            
            # Redirect back to admin
            return redirect('admin:genai_mathproblemgeneration_change', pk)

    # ── GET (or POST that failed validation) ─────────────────────────────────
    from genai.models import LLMPrompt as LLMPromptModel
    from genai.config import DEFAULT_LLM_PROVIDER, GROQ_MODEL, GROQ_TEMPERATURE, GEMINI_MODEL, OPENAI_MODEL
    prompt_qs = LLMPromptModel.objects.filter(is_active=True).order_by('-is_default', 'prompt_type', 'source_url')
    prompt_choices = [('', '— Auto (use default) —')] + [
        (str(p.id), f"[{p.get_prompt_type_display()}] {str(p)}")
        for p in prompt_qs
    ]

    # Rule number choices for the Extract Rule dropdown (all 50 rules)
    from bank.models import RULE_NAME_CHOICES
    rule_choices = [('', '— Select Rule —')] + list(RULE_NAME_CHOICES)

    # Determine active LLM info for display
    provider = DEFAULT_LLM_PROVIDER.lower()
    if provider == 'groq':
        llm_display = f"Groq — {GROQ_MODEL}  (temp: {GROQ_TEMPERATURE})"
    elif provider == 'gemini':
        llm_display = f"Gemini — {GEMINI_MODEL}"
    elif provider == 'openai':
        llm_display = f"OpenAI — {OPENAI_MODEL}"
    else:
        llm_display = provider

    if request.method != 'POST':
        initial_data = {
            'process_pdf': bool(math_problem.pdf_file),
            'chapter_decide_by_llm': not bool(math_problem.chapter),
            'difficulty_level_decide_by_llm': False,
            'use_paddle_ocr': False,
            'use_easy_ocr': False,
            'use_tesseract': True,
            'page_from': 1,
            'page_to': 0,
            'no_of_pages_at_a_time_For_EntirePDF': 2,
            'process_all_the_mcq_of_the_pageRange': False,
            'process_all_the_mcq_all_pages': False,
        }
        form = MathPDFProcessingForm(initial=initial_data, prompt_choices=prompt_choices, rule_choices=rule_choices)

    # Get chapter choices dynamically
    chapter_choices = MathProblemGeneration.get_chapter_choices()

    context = {
        'form': form,
        'math_problem': math_problem,
        'chapter_choices': chapter_choices,
        'has_pdf': bool(math_problem.pdf_file),
        'has_expression': bool(math_problem.expression),
        'title': f'Process Math Problem #{pk}',
        'opts': MathProblemGeneration._meta,
        'llm_display': llm_display,
        'llm_provider': provider.upper(),
        'prompt_qs': prompt_qs,
        'rule_choices': rule_choices,
        'math_chapter': math_problem.chapter or '',
    }

    return render(request, 'admin/genai/math_pdf_processing_form.html', context)


@staff_member_required
def fix_json_page(request):
    """HTML page + API to fix invalid LaTeX escape sequences in JSON strings."""
    if request.method == 'GET':
        return render(request, 'genai/admin/fix_json.html', {'title': 'Fix JSON'})

    # POST — fix and return corrected JSON
    try:
        body = json.loads(request.body)
        raw = body.get('json_text', '')
        if not raw:
            return JsonResponse({'success': False, 'error': 'No json_text provided.'})
    except Exception:
        return JsonResponse({'success': False, 'error': 'Invalid request body.'})

    import re

    def fix_backslashes(text):
        # Valid JSON escape sequences: \", \\, \/, \b, \f, \n, \r, \t, \uXXXX
        # Everything else (e.g. \( \) \[ \] \frac \text) is invalid and must be doubled.
        valid_escape = re.compile(r'\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4})')

        result = []
        i = 0
        while i < len(text):
            if text[i] == '\\':
                m = valid_escape.match(text, i)
                if m:
                    result.append(m.group())
                    i = m.end()
                else:
                    # Lone backslash — double it
                    result.append('\\\\')
                    i += 1
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)

    fixed_text = fix_backslashes(raw)

    try:
        json.loads(fixed_text)
    except json.JSONDecodeError as e:
        return JsonResponse({'success': False, 'error': f'Could not auto-fix JSON: {str(e)}'})

    return JsonResponse({'success': True, 'fixed_json': fixed_text})


def _detect_rule_name(text):
    """
    Find a "Rule N" mention in generated content (e.g. a rule card's <h2> heading, or a
    question's rule_based_explanation saying "Using Rule 3:...") and normalize it to the
    "Rule N" form used by bank.RULE_NAME_CHOICES. Content is the source of truth for which
    rule something actually is — more reliable than trusting the row's dropdown, since the
    LLM can (and does) return content for a different rule than requested.
    """
    if not text:
        return None
    match = re.search(r'Rule\s*(\d+)', text)
    if match:
        return f"Rule {match.group(1)}"
    return None


# ─── Math JSON generation: background job store (same pattern as bank's translate/action
# progress jobs — plain in-process dict + lock, single Django process only) ─────────────
_MPG_JOBS: dict = {}
_MPG_LOCK = threading.Lock()


def _mpg_job_update(job_id, done=None, err_inc=0, msg=None):
    with _MPG_LOCK:
        job = _MPG_JOBS.get(job_id)
        if not job:
            return
        if done is not None:
            job['done'] = done
        job['errors'] += err_inc
        if msg:
            job['log'].append(msg)


def _run_math_prompt_generation_job(job_id, tmp_dir, pdf_path, prompt_text, rows, provider_name, user_id,
                                     delay_seconds=20):
    """
    Background worker for math_prompt_generation_view. Runs OCR extraction + one LLM call
    per row, writing progress into _MPG_JOBS[job_id] as it goes so the browser can poll live
    status instead of blocking on one long synchronous request. Rows are always processed
    sequentially (one LLM call at a time); delay_seconds is an extra pause between rows on
    top of that, e.g. to stay under a provider's rate limit.
    """
    from genai.tasks.math_processor import OCRDispatcher
    from genai.utils.llm_provider import get_llm_provider

    merged_questions = []
    merged_rules = []
    row_prompts = []

    try:
        ocr = OCRDispatcher(use_paddle=False, use_easy=False, use_tesseract=True)
        llm = get_llm_provider(provider_name)

        for idx, row in enumerate(rows, 1):
            chapter = row['chapter']
            rule_name = row.get('rule_name') or ''
            page_from = row['page_from']
            page_to = row['page_to']
            difficulty = row['difficulty']
            row_label = f"Row {idx}/{len(rows)} ({chapter}, {rule_name or 'all rules'}, pages {page_from}-{page_to})"

            _mpg_job_update(job_id, msg=f"{row_label}: extracting text from pages {page_from}-{page_to}...")

            page_texts = []
            ocr_pages = []
            for page_num in range(page_from - 1, page_to):  # 0-indexed, inclusive of page_to
                page_text = ocr.extract_text(pdf_path, page_num)
                if page_text and page_text.strip():
                    page_texts.append(page_text)
                else:
                    ocr_pages.append(page_num + 1)
            content = "\n".join(page_texts)

            if ocr_pages:
                _mpg_job_update(job_id, msg=f"{row_label}: page(s) {ocr_pages} had no text layer — ran Tesseract OCR on them.")

            if not content.strip():
                _mpg_job_update(job_id, done=idx, err_inc=1,
                                 msg=f"{row_label}: no text extracted, even with OCR — skipped. "
                                     f"Check the page numbers are correct for this PDF.")
                continue

            row_prompt = prompt_text.replace('{difficulty}', difficulty)
            if rule_name:
                # Overrides any rule number mentioned elsewhere in the pasted prompt (e.g. a
                # leftover "RULE 1 ONLY" line) so this row's dropdown is an actual instruction
                # to the LLM, not just a label applied after the fact.
                row_prompt += (
                    f"\n\nSCOPE OVERRIDE: Regardless of any other instruction above about "
                    f"which rule number to use, extract ONLY content and questions for "
                    f"\"{rule_name}\" of chapter \"{chapter}\" from the source content below. "
                    f"Ignore all other rules present in the source, even if they appear on "
                    f"the same pages."
                )
            row_prompt += (
                f"\n\n--- SOURCE CONTENT (Chapter: {chapter}"
                f"{', ' + rule_name if rule_name else ''}, Pages {page_from}-{page_to}) ---\n"
                f"{content}\n--- END SOURCE CONTENT ---\n"
            )
            row_prompts.append({'label': row_label, 'prompt': row_prompt})

            _mpg_job_update(job_id, msg=f"{row_label}: sending prompt to the LLM "
                                         f"({len(row_prompt)} chars) — this can take 1-3 minutes...")

            response = llm.generate_json(row_prompt)
            truncated = getattr(llm, 'last_finish_reason', None) == 'length'

            if not response and not truncated:
                # one retry with a stricter reminder before giving up on this row - skipped when
                # the failure was a token-budget truncation, since asking more firmly for valid
                # JSON won't make the response shorter.
                _mpg_job_update(job_id, msg=f"{row_label}: response wasn't valid JSON — retrying once...")
                retry_prompt = row_prompt + (
                    "\n\nYour previous response was not valid JSON. "
                    "Return ONLY a valid JSON object — no markdown, no commentary."
                )
                response = llm.generate_json(retry_prompt)
                truncated = getattr(llm, 'last_finish_reason', None) == 'length'

            if not response:
                if truncated:
                    _mpg_job_update(
                        job_id, done=idx, err_inc=1,
                        msg=f"{row_label}: LLM response was cut off before finishing (hit the "
                            f"output token limit) — skipped. Try a narrower page range for this "
                            f"row and add more rows to cover the rest."
                    )
                else:
                    _mpg_job_update(job_id, done=idx, err_inc=1,
                                     msg=f"{row_label}: LLM did not return valid JSON — skipped.")
                if idx < len(rows) and delay_seconds:
                    _mpg_job_update(job_id, msg=f"Waiting {delay_seconds}s before the next row...")
                    time.sleep(delay_seconds)
                continue

            _mpg_job_update(job_id, msg=f"{row_label}: response received, parsing "
                                         f"{len((response.get('questions') or []))} question(s)...")

            row_questions = [q for q in (response.get('questions') or []) if isinstance(q, dict)]
            row_rules = response.get('rules_html') or []

            mismatch_notes = []

            for r in row_rules:
                html = r.get('rule_html') if isinstance(r, dict) else r
                detected = _detect_rule_name(html)
                effective_rule_name = detected or rule_name
                if rule_name and detected and detected != rule_name:
                    mismatch_notes.append(f"a rule card came back as {detected}, not the requested {rule_name}")
                if effective_rule_name:
                    merged_rules.append({'chapter': chapter, 'rule_name': effective_rule_name, 'rule_html': html})
                else:
                    # Couldn't identify which rule this is, and the row didn't specify one
                    # either — kept in the JSON for manual review only, not auto-linked.
                    merged_rules.append(html)

            for q in row_questions:
                q['chapter'] = chapter
                detected = _detect_rule_name(q.get('rule_based_explanation') or '')
                effective_rule_name = detected or rule_name
                if rule_name and detected and detected != rule_name:
                    mismatch_notes.append(
                        f"question \"{str(q.get('question', ''))[:50]}...\" came back as "
                        f"{detected}, not the requested {rule_name}"
                    )
                if effective_rule_name:
                    q['rule_name'] = effective_rule_name

            merged_questions.extend(row_questions)
            report_line = f"{row_label}: {len(row_questions)} question(s) extracted."
            if mismatch_notes:
                report_line += " ⚠️ Rule mismatch — " + "; ".join(mismatch_notes)
            _mpg_job_update(job_id, done=idx, msg=report_line)

            if idx < len(rows) and delay_seconds:
                _mpg_job_update(job_id, msg=f"Waiting {delay_seconds}s before the next row...")
                time.sleep(delay_seconds)

        if not merged_questions:
            with _MPG_LOCK:
                _MPG_JOBS[job_id]['result'] = {
                    'success': False,
                    'message': 'No questions were extracted from any row.',
                    'row_prompts': row_prompts,
                }
                _MPG_JOBS[job_id]['done_flag'] = True
            return

        payload = {'rules_html': merged_rules, 'questions': merged_questions}
        from django.contrib.auth import get_user_model
        User = get_user_model()
        created_by = User.objects.filter(pk=user_id).first()
        json_import = JsonImport.objects.create(
            to_table='math',
            json_data=json.dumps(payload, indent=2, ensure_ascii=False),
            created_by=created_by,
        )

        with _MPG_LOCK:
            _MPG_JOBS[job_id]['result'] = {
                'success': True,
                'message': f"Generated {len(merged_questions)} question(s) across {len(rows)} row(s).",
                'json_import_id': json_import.pk,
                'row_prompts': row_prompts,
            }
            _MPG_JOBS[job_id]['done_flag'] = True

    except Exception as e:
        logger.exception("math_prompt_generation background job failed")
        with _MPG_LOCK:
            job = _MPG_JOBS.get(job_id)
            if job:
                job['errors'] += 1
                job['log'].append(f"Unexpected error: {e}")
                job['result'] = {'success': False, 'message': f"Unexpected error: {e}", 'row_prompts': row_prompts}
                job['done_flag'] = True
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


@staff_member_required
def math_prompt_generation_view(request):
    """
    Paste your own extraction prompt (or load a saved one), upload a PDF, and give one or
    more (chapter, rule, page range, difficulty) rows. Submitting kicks off a background job
    (one LLM call per row, via OCRDispatcher with OCR fallback for scanned pages) and redirects
    to a live-progress page — nothing here blocks the request. Results are tagged with each
    row's chapter/rule and merged into a single JsonImport (to_table='math') for you to
    review/edit — nothing is written to the math/rule_math tables until you use the "Bulk
    Import" action on the JsonImport changelist (or the one-click "Insert" button on its
    change page).
    """
    from genai.models import MathPromptTemplate

    title = 'Generate Math JSON from PDF + Prompt'
    prompt_templates = {t.name: t.prompt_text for t in MathPromptTemplate.objects.all()}

    if request.method == 'POST':
        form = MathPromptGenerationForm(request.POST, request.FILES)
        formset = MathPromptRowFormSet(request.POST, prefix='rows')

        if form.is_valid() and formset.is_valid():
            rows = [
                f.cleaned_data for f in formset
                if f.cleaned_data and not f.cleaned_data.get('DELETE')
            ]
            if not rows:
                messages.error(request, "Add at least one chapter/page-range row.")
                return render(request, 'admin/genai/math_prompt_generation.html',
                              {'form': form, 'formset': formset, 'title': title,
                               'prompt_templates': prompt_templates})

            prompt_text = form.cleaned_data['prompt_text']
            uploaded_pdf = form.cleaned_data['pdf_file']

            save_prompt_as = form.cleaned_data.get('save_prompt_as')
            if save_prompt_as:
                MathPromptTemplate.objects.update_or_create(
                    name=save_prompt_as,
                    defaults={
                        'prompt_text': prompt_text,
                        'is_default': form.cleaned_data.get('make_default_prompt', False),
                        'created_by': request.user,
                    }
                )

            # The background thread needs a real file path, so persist the upload to a temp
            # dir that survives past this request (cleaned up by the worker when it finishes).
            tmp_dir = tempfile.mkdtemp(prefix='math_prompt_gen_')
            pdf_path = os.path.join(tmp_dir, uploaded_pdf.name)
            with open(pdf_path, 'wb') as f:
                for chunk in uploaded_pdf.chunks():
                    f.write(chunk)

            job_id = str(uuid.uuid4())
            with _MPG_LOCK:
                _MPG_JOBS[job_id] = {
                    'total': len(rows), 'done': 0, 'errors': 0, 'done_flag': False,
                    'log': [], 'result': None,
                }
            delay_seconds = form.cleaned_data.get('delay_seconds')
            if delay_seconds is None:
                delay_seconds = 20

            threading.Thread(
                target=_run_math_prompt_generation_job,
                args=(job_id, tmp_dir, pdf_path, prompt_text, rows,
                      form.cleaned_data.get('llm_provider') or None, request.user.pk),
                kwargs={'delay_seconds': delay_seconds},
                daemon=True,
            ).start()

            return redirect(reverse('genai:math_prompt_generation_progress') + '?job_id=' + job_id)
    else:
        default_template = MathPromptTemplate.objects.filter(is_default=True).first()
        initial = {'prompt_text': default_template.prompt_text, 'saved_prompt': default_template.name} \
            if default_template else {}
        form = MathPromptGenerationForm(initial=initial)
        formset = MathPromptRowFormSet(prefix='rows')

    return render(request, 'admin/genai/math_prompt_generation.html',
                  {'form': form, 'formset': formset, 'title': title, 'prompt_templates': prompt_templates})


@staff_member_required
def math_prompt_generation_progress(request):
    """Live-progress page shown right after submitting the generation form."""
    job_id = request.GET.get('job_id', '')
    with _MPG_LOCK:
        job = _MPG_JOBS.get(job_id)
    if not job:
        return render(request, 'admin/genai/math_prompt_generation_progress.html',
                       {'error': f'Job not found: {job_id}'})
    return render(request, 'admin/genai/math_prompt_generation_progress.html', {
        'job_id': job_id,
        'total': job['total'],
    })


@staff_member_required
def math_prompt_generation_poll(request):
    """Polled by the progress page's JS every couple seconds."""
    job_id = request.GET.get('job_id', '')
    with _MPG_LOCK:
        job = dict(_MPG_JOBS.get(job_id, {}))
    if not job:
        return JsonResponse({'error': 'not found'}, status=404)

    result = job.get('result')
    if result and result.get('json_import_id'):
        result = dict(result)
        result['json_import_url'] = reverse('admin:genai_jsonimport_change', args=[result['json_import_id']])

    return JsonResponse({
        'total': job.get('total', 0),
        'done': job.get('done', 0),
        'errors': job.get('errors', 0),
        'done_flag': job.get('done_flag', False),
        'log': job.get('log', [])[-200:],
        'result': result,
    })


@staff_member_required
def jsonimport_quick_insert(request, pk):
    """
    One-click "Insert into Math Table" button on the JsonImport change page — runs the same
    BulkImporter used by the changelist's Bulk Import action, but for this single record and
    without the intermediate date-picker form (today's date is used as the fallback date for
    any records that don't specify one).
    """
    from datetime import date, time as time_cls
    from genai.bulk_import import BulkImporter

    json_import = get_object_or_404(JsonImport, pk=pk)

    if request.method != 'POST':
        return redirect('admin:genai_jsonimport_change', pk)

    resolved = request.POST.get('conflicts_resolved') == '1'

    # For math imports, check for (chapter, rule_name) conflicts BEFORE writing anything, so
    # they can be reviewed and resolved (keep one / merge) instead of one side being silently
    # discarded and only reported after the fact.
    if json_import.to_table == 'math' and not resolved:
        try:
            payload = json.loads(json_import.json_data)
        except json.JSONDecodeError:
            payload = None
        if payload is not None:
            scanner = BulkImporter(
                table_name=json_import.to_table,
                json_data=json_import.json_data,
                form_date=date.today(),
                form_time=time_cls(10, 0, 0),
            )
            conflicts = scanner.scan_math_conflicts(payload)
            if conflicts:
                return render(request, 'admin/genai/jsonimport/resolve_conflicts.html', {
                    'json_import': json_import,
                    'conflicts': conflicts,
                    'opts': JsonImport._meta,
                    'title': 'Resolve rule conflicts before inserting',
                })

    resolutions = {}
    if resolved:
        i = 0
        while True:
            key = request.POST.get(f'key_{i}')
            if key is None:
                break
            resolutions[key] = {
                'merged_html': request.POST.get(f'merged_{i}', ''),
            }
            i += 1

    importer = BulkImporter(
        table_name=json_import.to_table,
        json_data=json_import.json_data,
        form_date=date.today(),
        form_time=time_cls(10, 0, 0),
    )
    result = importer.import_data(resolutions=resolutions)

    if result['success'] or result['created'] or result['updated']:
        messages.success(
            request,
            f"✅ Inserted! Created: {result['created']}, Updated: {result['updated']}, "
            f"Errors: {len(result['errors'])}."
        )
    else:
        messages.error(request, f"❌ Insert failed: {result['message']}")

    for err in (result.get('errors') or [])[:10]:
        messages.warning(request, f"⚠️ {err}")

    for skipped in (result.get('skipped_rules') or []):
        messages.warning(
            request,
            f"⚠️ Rule \"{skipped['rule_name']}\" for chapter \"{skipped['chapter']}\" already "
            f"existed in rule_math and was NOT overwritten — question(s) were linked to the "
            f"existing rule. Generated text (copy manually if you want to update it): "
            f"{skipped['generated_html'][:500]}"
        )

    for conflict in (result.get('batch_rule_conflicts') or []):
        messages.warning(
            request,
            f"⚠️ Two different rule cards both claimed \"{conflict['rule_name']}\" for chapter "
            f"\"{conflict['chapter']}\" in this same import — only the first was kept. This "
            f"discarded one was NOT saved (check if it's actually a different rule number): "
            f"{conflict['discarded_html'][:500]}"
        )

    return redirect('admin:genai_jsonimport_change', pk)

