"""
GenAI Views
API endpoints for GenAI tasks
"""

import logging
import json
import subprocess
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Q

from genai.tasks.current_affairs import fetch_and_process_current_affairs
from genai.tasks.pdf_processor import process_subject_pdf
from genai.tasks.math_processor import process_math_problem, batch_process_math_problems
from genai.models import ProcessingLog

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
    Process subject PDF and generate MCQs
    
    POST data:
    - pdf_file: File upload
    - chapter: Chapter name
    - topic: Topic name
    - start_page: (optional) Starting page
    - end_page: (optional) Ending page
    - num_questions: (optional) Number of questions
    """
    try:
        # Handle file upload
        if 'pdf_file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No PDF file provided'
            }, status=400)
        
        pdf_file = request.FILES['pdf_file']
        chapter = request.POST.get('chapter', '')
        topic = request.POST.get('topic', '')
        start_page = int(request.POST.get('start_page', 0))
        end_page = request.POST.get('end_page')
        end_page = int(end_page) if end_page else None
        num_questions = int(request.POST.get('num_questions', 5))
        
        # Save uploaded file temporarily
        file_path = default_storage.save(f'temp/{pdf_file.name}', ContentFile(pdf_file.read()))
        
        logger.info(f"Processing PDF: {chapter} - {topic}")
        result = process_subject_pdf(
            file_path,
            chapter,
            topic,
            start_page=start_page,
            end_page=end_page,
            num_questions=num_questions
        )
        
        # Clean up
        default_storage.delete(file_path)
        
        return JsonResponse({
            'success': True,
            'message': 'PDF processing completed',
            'data': result
        })
    
    except Exception as e:
        logger.error(f"Error in process_subject_pdf_view: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


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

