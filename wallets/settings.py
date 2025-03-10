import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

# Core settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
if DEBUG:
    ALLOWED_HOSTS = ['*']

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = 'wallets.urls'
WSGI_APPLICATION = 'wallets.wsgi.application'

# Apps and middleware
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'wallets',
]

MIDDLEWARE = ['django.middleware.common.CommonMiddleware']

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'wallets/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

# Security
CSRF_COOKIE_SECURE = False  # We are API-only
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = False  # API-only
SILENCED_SYSTEM_CHECKS = ['security.W019']  # API-only
X_FRAME_OPTIONS = 'DENY'

# Performance
APPEND_SLASH = True
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 50
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5 MB
USE_X_FORWARDED_HOST = False
USE_X_FORWARDED_PORT = False

# Internationalization
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
THOUSAND_SEPARATOR = False
USE_I18N = False
USE_L10N = False
USE_THOUSAND_SEPARATOR = False
USE_TZ = True

# Database
db_url = urlparse(os.getenv('DATABASE_URL'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_url.path[1:],
        'USER': db_url.username,
        'PASSWORD': db_url.password,
        'HOST': db_url.hostname,
        'PORT': db_url.port,
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'connect_timeout': 5,
            'keepalives': 1,
            'keepalives_idle': 30,
            'keepalives_interval': 10,
            'keepalives_count': 5,
            'client_encoding': 'UTF8',
            'application_name': 'wallets',
            'sslmode': 'disable',
        },
        'CONN_HEALTH_CHECKS': True,
        'AUTOCOMMIT': True,
        'DISABLE_SERVER_SIDE_CURSORS': True,  # Better for short queries
        'ATOMIC_REQUESTS': True,  # Slower but more secure
        'TEST': {'MIRROR': None},  # Don't mirror test DB
    },
}

# API
JSON_API_COMPACT_RESPONSE = True
JSON_API_FORMAT_FIELD_NAMES = 'dasherize'
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = True

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,  # Handle decimals better
    'COMPACT_JSON': True,  # Trim whitespace
    'DATE_FORMAT': '%Y-%m-%d',
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    'DEFAULT_PARSER_CLASSES': ('rest_framework_json_api.parsers.JSONParser',),
    'DEFAULT_RENDERER_CLASSES': ['rest_framework_json_api.renderers.JSONRenderer'],
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'HTML_SELECT_CUTOFF': 100,  # Limit browsable API
    'MAX_PAGINATE_BY': 100,
    'NUM_PROXIES': 0,
    'PAGE_SIZE': 10,
    'UNICODE_JSON': False,  # Speed up JSON encoding
}
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework_json_api.renderers.BrowsableAPIRenderer'
    )
