# Quick Start Guide - GenAI System Setup

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Setup Configuration
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

## Step 3: Update Django Settings
Add `genai` to INSTALLED_APPS in `django/django_project/django_project/settings.py`:
```python
INSTALLED_APPS = (
    'bank',
    'genai',  # <-- Add this
    'django.contrib.admin',
    # ... rest
)
```

## Step 4: Configure Your Data Sources
Edit `django/django_project/genai/config.py`:
```python
CURRENT_AFFAIRS_SOURCES = {
    'mcq': [
        'https://your-mcq-site.com',
        'https://another-site.com',
    ],
    'descriptive': [
        'https://your-desc-site.com',
    ]
}
```

## Step 5: Update Your Models (Important!)
Adjust the database field mappings in:
- `genai/tasks/current_affairs.py` (line ~214)
- `genai/tasks/pdf_processor.py` (line ~152)
- `genai/tasks/math_processor.py` (line ~219)

Map LLM output to your actual database fields.

## Step 6: Run Migrations (if needed)
```bash
python manage.py migrate
```

## Step 7: Test the System

### Test API Status
```bash
curl http://localhost:8000/genai/api/status/
```

### Test Current Affairs Processing
```bash
curl -X POST http://localhost:8000/genai/api/current-affairs/mcq/
```

### Test Math Processing
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"problem": "Find x if 2x + 5 = 13"}' \
  http://localhost:8000/genai/api/math/process/
```

## Using Management Commands
```bash
python manage.py fetch_current_affairs --type=mcq
python manage.py fetch_current_affairs --type=descriptive
```

## Integration with Your Views

In your `bank/views.py`, you can now import and use GenAI:

```python
from genai.tasks.current_affairs import fetch_and_process_current_affairs
from genai.tasks.math_processor import process_math_problem

def my_view(request):
    # Generate current affairs MCQs
    result = fetch_and_process_current_affairs('mcq')
    
    # Or process a math problem
    mcq = process_math_problem('Solve: x² - 5x + 6 = 0')
    
    return render(request, 'template.html', {'result': result})
```

## Debugging

### Check Logs
All tasks log to Django's logger with namespace `genai.tasks.*`:
```python
import logging
logger = logging.getLogger('genai.tasks.current_affairs')
```

### Test LLM Provider
```python
from genai.utils.llm_provider import default_llm
response = default_llm.generate("Hello, say a mathematical problem")
print(response)
```

### Mock Provider for Testing
Without spending API credits, use the mock provider:
```python
from genai.utils.llm_provider import get_llm_provider
mock_llm = get_llm_provider('mock')
response = mock_llm.generate_json('{"test": "data"}')
```

## Next Steps

1. **Configure Web Scraping**: Add real URLs for current affairs
2. **Update Database Mappings**: Ensure fields match your schema
3. **Add Custom Processors**: Extend the base classes for custom behavior
4. **Setup Async Tasks**: Integrate with Celery for production
5. **Add Analytics**: Track content generation metrics

## Troubleshooting

### "genai is not in INSTALLED_APPS"
→ Add `'genai'` to INSTALLED_APPS in settings.py

### "No module named 'openai'"
→ Run: `pip install openai`

### "OPENAI_API_KEY not found"
→ Create `.env` file and add your API key

### PDF extraction not working
→ Install: `pip install PyPDF2 pdfplumber`

For more help, see the README.md in the genai folder.
