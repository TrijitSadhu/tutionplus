"""
GenAI Configuration File
Configure your LLM API keys and endpoints here
"""

import os
from dotenv import load_dotenv

load_dotenv()

# LLM Provider Selection (options: 'gemini', 'openai', 'mock')
DEFAULT_LLM_PROVIDER = os.getenv('DEFAULT_LLM_PROVIDER', 'gemini')

# Gemini Pro Configuration (DEFAULT)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
GEMINI_TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', '0.7'))
GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv('GEMINI_MAX_OUTPUT_TOKENS', '2048'))

# OpenAI Configuration (BACKUP)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

# Alternative LLM Providers (add as needed)
# ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Web Scraping Configuration - HARDCODED FALLBACK (use database for main sources)
CURRENT_AFFAIRS_SOURCES = {
    'currentaffairs_mcq': [
        'https://www.gktoday.in/daily-current-affairs-quiz-january-24-2026/',
    ],
    'currentaffairs_descriptive': [
        'https://example-descriptive-site.com',
    ]
}

# PDF Processing Configuration
PDF_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'uploaded_pdfs')
MAX_PDF_SIZE = 50 * 1024 * 1024  # 50MB

# Request Headers
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Task Queue Configuration (if using Celery)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

print("[OK] GenAI Configuration loaded (Default Provider: {})".format(DEFAULT_LLM_PROVIDER.upper()))
