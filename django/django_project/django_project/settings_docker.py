"""
Docker / Production settings for tutionplus.
Used when DJANGO_SETTINGS_MODULE=django_project.settings_docker

All values come from the .env file (never hardcode secrets here).
"""
import os

# ─── Core ─────────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# ─── Apps ─────────────────────────────────────────────────────────────────────
INSTALLED_APPS = (
    'bank',
    'genai',
    'mocktest',
    'students',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'django_project.urls'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'

# ─── Database (reads from .env) ───────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'tutionplus'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c timezone=UTC',
        }
    }
}

# ─── Cache / Celery (Redis) ───────────────────────────────────────────────────
REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# ─── Email ────────────────────────────────────────────────────────────────────
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587

# ─── Static & Media ───────────────────────────────────────────────────────────
STATIC_URL = '/static/'
# Files land at this path after COPY . /app/ in Dockerfile
STATIC_ROOT = '/app/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# ─── Internationalisation ─────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Fix UTC timezone assertion for psycopg2 (same as original settings.py)
import django.db.backends.postgresql.utils as _pg_utils
_original_utc = _pg_utils.utc_tzinfo_factory

def _utc_tzinfo_factory_patched(conn):
    try:
        return _original_utc(conn)
    except AssertionError:
        import datetime
        return datetime.timezone.utc

_pg_utils.utc_tzinfo_factory = _utc_tzinfo_factory_patched
