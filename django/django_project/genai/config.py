"""
GenAI Configuration File
Configure your LLM API keys and endpoints here
"""

import os
from dotenv import load_dotenv

# Load .env from project root (3 directories up from this file)
# genai/config.py → django_project → django → tutionplus
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.env'))
print(f"[CONFIG] Looking for .env at: {env_path}")
print(f"[CONFIG] .env exists: {os.path.exists(env_path)}")
loaded = load_dotenv(env_path)
print(f"[CONFIG] load_dotenv() result: {loaded}")

# LLM Provider Selection (options: 'groq', 'gemini', 'openai', 'mock')
DEFAULT_LLM_PROVIDER = os.getenv('DEFAULT_LLM_PROVIDER', 'groq')

# Groq Configuration (DEFAULT)
# Available Groq Models: openai/gpt-oss-120b, llama-3.3-70b-versatile
GROQ_API_KEY = os.getenv('GROQ_API_KEY', 'your-groq-api-key-here')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'qwen/qwen3-32b')
GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', '0.7'))
GROQ_MAX_OUTPUT_TOKENS_ENV = os.getenv('GROQ_MAX_OUTPUT_TOKENS')
GROQ_MAX_OUTPUT_TOKENS = int(GROQ_MAX_OUTPUT_TOKENS_ENV) if GROQ_MAX_OUTPUT_TOKENS_ENV else 8192
print(f"[CONFIG] GROQ_MAX_OUTPUT_TOKENS from env: {GROQ_MAX_OUTPUT_TOKENS_ENV}")
print(f"[CONFIG] Final GROQ_MAX_OUTPUT_TOKENS: {GROQ_MAX_OUTPUT_TOKENS}")

# Gemini Pro Configuration (BACKUP)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
GEMINI_TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', '0.7'))
GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv('GEMINI_MAX_OUTPUT_TOKENS', '8192'))

# OpenAI Configuration (BACKUP)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

# DeepSeek Configuration (OpenAI-compatible API)
# Note: reasoning-capable DeepSeek models spend a chunk of the token budget on hidden
# reasoning before writing the visible answer, and this app's prompts ask for verbose
# HTML/SVG-formatted solutions - 8192 is too tight and truncates mid-JSON. 24576 leaves
# headroom (~7000 completion tokens was typical in testing against the real math prompt).
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'your-deepseek-api-key-here')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
DEEPSEEK_TEMPERATURE = float(os.getenv('DEEPSEEK_TEMPERATURE', '0.7'))
DEEPSEEK_MAX_OUTPUT_TOKENS = int(os.getenv('DEEPSEEK_MAX_OUTPUT_TOKENS', '32768'))
DEEPSEEK_REQUEST_TIMEOUT = int(os.getenv('DEEPSEEK_REQUEST_TIMEOUT', '420'))

# NVIDIA NIM Configuration (OpenAI-compatible API, integrate.api.nvidia.com)
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', 'your-nvidia-api-key-here')
NVIDIA_MODEL = os.getenv('NVIDIA_MODEL', 'qwen/qwen3.5-397b-a17b')
NVIDIA_BASE_URL = os.getenv('NVIDIA_BASE_URL', 'https://integrate.api.nvidia.com/v1')
NVIDIA_TEMPERATURE = float(os.getenv('NVIDIA_TEMPERATURE', '0.7'))
NVIDIA_MAX_OUTPUT_TOKENS = int(os.getenv('NVIDIA_MAX_OUTPUT_TOKENS', '32768'))
NVIDIA_REQUEST_TIMEOUT = int(os.getenv('NVIDIA_REQUEST_TIMEOUT', '420'))

# Claude Configuration (official Anthropic SDK, Messages API)
# Note: a claude.ai / Claude Code subscription does NOT include API access - the key comes from
# console.anthropic.com and is billed per token. Left empty, the SDK falls back to the
# ANTHROPIC_API_KEY env var or an `ant auth login` profile. Claude Opus 5.5 always thinks before
# answering; ANTHROPIC_EFFORT (low/medium/high/xhigh/max) controls how much - its own default is
# medium, 'high' suits multi-step math validation.
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-opus-5-5')
ANTHROPIC_EFFORT = os.getenv('ANTHROPIC_EFFORT', 'high')
ANTHROPIC_MAX_OUTPUT_TOKENS = int(os.getenv('ANTHROPIC_MAX_OUTPUT_TOKENS', '64000'))
ANTHROPIC_REQUEST_TIMEOUT = int(os.getenv('ANTHROPIC_REQUEST_TIMEOUT', '600'))

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
