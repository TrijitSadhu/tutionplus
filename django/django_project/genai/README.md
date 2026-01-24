# GenAI Content Generation System

Comprehensive AI-powered content generation system for the TutionPlus application.

## Features

### 1. Current Affairs Processing
- **Scraping**: Automatically fetch current affairs from configured websites
- **LLM Processing**: Use GPT to generate high-quality MCQs and descriptive content
- **Database Integration**: Save to respective tables (MCQ/Descriptive)
- **Endpoints**:
  - `POST /genai/api/current-affairs/mcq/` - Process MCQ content
  - `POST /genai/api/current-affairs/descriptive/` - Process descriptive content

### 2. Subject PDF Processing
- **PDF Extraction**: Extract text from PDF files
- **Selective Processing**: Choose specific chapters and topics
- **LLM-Generated MCQs**: Aligned with your table structure
- **Endpoints**:
  - `POST /genai/api/pdf/process/` - Process PDF with parameters

### 3. Math LaTeX Processing
- **Syntax Conversion**: Converts math expressions to LaTeX
- **MCQ Generation**: Creates MCQs with proper LaTeX formatting
- **Batch Processing**: Handle multiple problems
- **Endpoints**:
  - `POST /genai/api/math/process/` - Single problem
  - `POST /genai/api/math/batch/` - Batch processing

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
```

### 3. Update settings.py
Add `genai` to INSTALLED_APPS:
```python
INSTALLED_APPS = (
    'bank',
    'genai',  # Add this
    'django.contrib.admin',
    # ... rest of apps
)
```

### 4. Configure Scraping Sources
Edit `genai/config.py` to add your current affairs sources:
```python
CURRENT_AFFAIRS_SOURCES = {
    'mcq': ['https://your-mcq-site.com'],
    'descriptive': ['https://your-descriptive-site.com']
}
```

## Usage

### Via Django Views (API)

#### Current Affairs MCQ
```bash
curl -X POST http://localhost:8000/genai/api/current-affairs/mcq/
```

#### Process PDF for Subject
```bash
curl -X POST -F "pdf_file=@document.pdf" \
  -F "chapter=History" \
  -F "topic=Ancient India" \
  -F "start_page=0" \
  -F "end_page=10" \
  -F "num_questions=5" \
  http://localhost:8000/genai/api/pdf/process/
```

#### Process Math Problem
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"problem": "Find the value of x in 2x + 5 = 13", "difficulty": "Medium"}' \
  http://localhost:8000/genai/api/math/process/
```

#### Batch Math Processing
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "problems": ["Problem 1", "Problem 2", "Problem 3"],
    "chapter": "Algebra",
    "difficulty": "Hard"
  }' \
  http://localhost:8000/genai/api/math/batch/
```

### Via Management Commands

#### Fetch Current Affairs
```bash
python manage.py fetch_current_affairs --type=mcq
python manage.py fetch_current_affairs --type=descriptive
```

### Via Python Code

```python
from genai.tasks.current_affairs import fetch_and_process_current_affairs
from genai.tasks.pdf_processor import process_subject_pdf
from genai.tasks.math_processor import process_math_problem, batch_process_math_problems

# Current Affairs
result = fetch_and_process_current_affairs('mcq')

# PDF Processing
result = process_subject_pdf(
    pdf_path='path/to/pdf.pdf',
    chapter='History',
    topic='Ancient India',
    num_questions=5
)

# Math Problem
result = process_math_problem(
    problem='Solve: 2x + 5 = 13',
    difficulty='Medium'
)

# Batch Math
result = batch_process_math_problems(
    problems=['Problem 1', 'Problem 2'],
    chapter='Algebra',
    difficulty='Hard'
)
```

## Project Structure

```
genai/
├── config.py              # Configuration and settings
├── views.py              # API views/endpoints
├── urls.py               # URL routing
├── tasks/
│   ├── current_affairs.py    # Current affairs scraping & processing
│   ├── pdf_processor.py      # PDF processing module
│   └── math_processor.py     # Math LaTeX conversion
├── utils/
│   └── llm_provider.py       # LLM API integration
└── management/
    └── commands/
        └── fetch_current_affairs.py
```

## Database Integration

The system automatically saves processed content to your database:

- **MCQ Current Affairs** → `current_affairs` table
- **Descriptive Content** → Custom descriptive table (configure in `pdf_processor.py`)
- **Subject MCQs** → `total` table (or your subject table)
- **Math Problems** → Configure in `math_processor.py`

## Configuration

### LLM Provider
Choose between OpenAI, mock, or custom providers in `config.py`.

### API Models
Adjust the saved model fields in task files to match your actual database schema:
- `current_affairs.py` - Line 214
- `pdf_processor.py` - Line 152
- `math_processor.py` - Line 219

### Sources
Add your scraping sources in `config.py`:
```python
CURRENT_AFFAIRS_SOURCES = {
    'mcq': ['URL1', 'URL2', ...],
    'descriptive': ['URL1', 'URL2', ...]
}
```

## Advanced Features

### Custom LLM Providers
Extend `LLMProvider` class in `utils/llm_provider.py` to use other models (Anthropic, Google, etc.).

### Async Processing
For production, integrate with Celery for background task processing:
```python
# In views.py or tasks
@shared_task
def async_process_pdf(pdf_path, chapter, topic):
    return process_subject_pdf(pdf_path, chapter, topic)
```

### Error Handling
All tasks include comprehensive error logging. Check logs for detailed error information.

## Common Issues

### "No PDF library available"
```bash
pip install PyPDF2 pdfplumber
```

### OpenAI API errors
- Verify API key in `.env`
- Check API rate limits
- Ensure valid organization ID if using organization accounts

### LaTeX Validation Errors
Invalid LaTeX syntax will be caught and reported. Check the response for validation details.

## Future Enhancements

1. **Real-time Scraping**: Scheduled scraping tasks
2. **Advanced PDF OCR**: Handle scanned PDFs with image content
3. **Multi-language Support**: Process content in multiple languages
4. **Custom Grading**: AI-powered answer evaluation
5. **Analytics Dashboard**: Track content generation metrics

## Support

For issues or feature requests, please check the project documentation or contact the development team.

## License

Proprietary - TutionPlus
