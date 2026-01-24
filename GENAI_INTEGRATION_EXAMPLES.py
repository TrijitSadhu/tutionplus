"""
Example Integration of GenAI into Existing Views

Add these patterns to your bank/views.py to use GenAI functionality
"""

# Example 1: Add GenAI processing to existing views
# =================================================

def dashboard_with_genai(request):
    """
    Extend your existing dashboard to show AI-generated content
    """
    from genai.tasks.current_affairs import fetch_and_process_current_affairs
    
    try:
        # Fetch latest current affairs MCQs
        ca_mcqs = fetch_and_process_current_affairs('mcq')
        context = {
            'ca_mcqs': ca_mcqs['processed_items'],
            'total_processed': ca_mcqs['articles_scraped']
        }
    except Exception as e:
        context = {'error': str(e)}
    
    return render(request, 'dashboard.html', context)


# Example 2: Create a new view for PDF upload and processing
# ==========================================================

from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from genai.tasks.pdf_processor import process_subject_pdf

@require_http_methods(["GET", "POST"])
def process_pdf_view(request):
    """
    Handle PDF upload and generate MCQs
    """
    if request.method == 'POST':
        if 'pdf_file' not in request.FILES:
            return JsonResponse({'error': 'No PDF provided'}, status=400)
        
        # Get form data
        pdf_file = request.FILES['pdf_file']
        chapter = request.POST.get('chapter', '')
        topic = request.POST.get('topic', '')
        num_questions = int(request.POST.get('num_questions', 5))
        
        try:
            # Save temporarily
            file_path = default_storage.save(
                f'temp/{pdf_file.name}',
                ContentFile(pdf_file.read())
            )
            
            # Process with GenAI
            result = process_subject_pdf(
                file_path,
                chapter,
                topic,
                num_questions=num_questions
            )
            
            # Clean up
            default_storage.delete(file_path)
            
            return JsonResponse({
                'success': True,
                'data': result['processed_mcqs'],
                'message': f"Generated {len(result.get('processed_mcqs', []))} MCQs"
            })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    # GET request - show form
    return render(request, 'pdf_processor.html')


# Example 3: Math problem view with LaTeX
# =======================================

from genai.tasks.math_processor import process_math_problem

def math_problem_solver(request):
    """
    Solve math problems with LaTeX formatting
    """
    if request.method == 'POST':
        problem = request.POST.get('problem', '')
        difficulty = request.POST.get('difficulty', 'Medium')
        
        try:
            result = process_math_problem(problem, difficulty)
            
            return render(request, 'math_solution.html', {
                'problem': problem,
                'solution': result,
                'latex': result.get('problem_latex', '')
            })
        
        except Exception as e:
            return render(request, 'math_problem.html', {
                'error': str(e)
            })
    
    return render(request, 'math_problem.html')


# Example 4: Batch math processing
# ================================

from genai.tasks.math_processor import batch_process_math_problems

def batch_math_processor(request):
    """
    Generate MCQs from multiple math problems at once
    """
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        problems = data.get('problems', [])
        chapter = data.get('chapter', 'General')
        difficulty = data.get('difficulty', 'Medium')
        
        if not problems:
            return JsonResponse({'error': 'No problems provided'}, status=400)
        
        try:
            result = batch_process_math_problems(problems, chapter, difficulty)
            
            return JsonResponse({
                'success': True,
                'total': len(problems),
                'processed': len(result['processed_mcqs']),
                'mcqs': result['processed_mcqs']
            })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'batch_math.html')


# Example 5: Async task scheduling (with Celery)
# ==============================================

from celery import shared_task
from genai.tasks.current_affairs import CurrentAffairsProcessor

@shared_task
def scheduled_ca_fetch():
    """
    Run as a Celery task for scheduled content updates
    Usage: celery -A django_project beat
    """
    processor = CurrentAffairsProcessor()
    result = processor.run_complete_pipeline('mcq')
    return result


# Example 6: Add GenAI to your existing models
# ============================================

# In bank/models.py, add a field to track AI-generated content:

# ai_generated = models.BooleanField(default=False)
# ai_model = models.CharField(max_length=50, blank=True)
# ai_prompt = models.TextField(blank=True)

# Then when saving:
# mcq = current_affairs(
#     upper_heading=data['question'],
#     yellow_heading=data['explanation'],
#     ai_generated=True,
#     ai_model='gpt-4'
# )
# mcq.save()


# Example 7: Add API endpoint for frontend integration
# ==================================================

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def api_generate_math_mcq(request):
    """
    REST API endpoint for JavaScript frontend
    Usage: fetch('/api/genai/math/', {method: 'POST', body: JSON.stringify(...)})
    """
    problem = request.data.get('problem')
    
    if not problem:
        return Response({'error': 'Problem required'}, status=400)
    
    try:
        result = process_math_problem(problem)
        return Response({
            'success': True,
            'mcq': result
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)


# Example 8: Monitoring and logging
# ================================

import logging

def monitored_ca_processing(request):
    """
    Process with detailed logging and monitoring
    """
    logger = logging.getLogger('genai.tasks.current_affairs')
    
    logger.info("User initiated CA processing")
    
    try:
        result = fetch_and_process_current_affairs('mcq')
        
        logger.info(f"Successfully processed {len(result.get('processed_items', []))} items")
        
        return JsonResponse({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        logger.error(f"Error in CA processing: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=400)


# Example 9: Error handling and validation
# ======================================

from django.http import HttpResponseBadRequest

def process_with_validation(request):
    """
    Process with input validation
    """
    problem = request.POST.get('problem', '').strip()
    
    # Validation
    if not problem:
        return HttpResponseBadRequest("Problem cannot be empty")
    
    if len(problem) < 10:
        return HttpResponseBadRequest("Problem too short")
    
    if len(problem) > 5000:
        return HttpResponseBadRequest("Problem too long")
    
    try:
        result = process_math_problem(problem)
        return JsonResponse({'success': True, 'result': result})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Example 10: Update your URLs to include these new views
# ======================================================

# In bank/urls.py, add:
# re_path(r'^genai/process-pdf/$', views.process_pdf_view, name='process_pdf'),
# re_path(r'^genai/math-solver/$', views.math_problem_solver, name='math_solver'),
# re_path(r'^genai/batch-math/$', views.batch_math_processor, name='batch_math'),
# re_path(r'^api/genai/math/$', views.api_generate_math_mcq, name='api_math'),

# HTML Form Example
# ================

"""
<!-- math_problem.html -->
<form method="POST" action="{% url 'bank:math_solver' %}">
    {% csrf_token %}
    <textarea name="problem" required></textarea>
    <select name="difficulty">
        <option value="Easy">Easy</option>
        <option value="Medium" selected>Medium</option>
        <option value="Hard">Hard</option>
    </select>
    <button type="submit">Generate MCQ</button>
</form>

{% if solution %}
<div class="latex-content">
    {{ solution.problem_latex|safe }}
</div>
<div class="mcq">
    <p>{{ solution.question }}</p>
    <!-- Render options -->
</div>
{% endif %}
"""

# JavaScript Example
# ==================

"""
// Generate math problem via AJAX
async function generateMathMCQ() {
    const problem = document.getElementById('problem').value;
    
    const response = await fetch('/api/genai/math/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({problem: problem})
    });
    
    const data = await response.json();
    
    if (data.success) {
        displayMCQ(data.mcq);
    } else {
        alert('Error: ' + data.error);
    }
}
"""


if __name__ == '__main__':
    print("GenAI Integration Examples")
    print("=" * 50)
    print("Add these patterns to your views.py to use GenAI")
    print("See documentation for more details")
