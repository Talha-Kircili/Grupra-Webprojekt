from pathlib import Path
from os import path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

DEBUG = False

ALLOWED_HOSTS = ['localhost']

CSRF_TRUSTED_ORIGINS = ['https://support.netzlabor', 'https://192.168.1.8']

INSTALLED_APPS = [
    'Praktikum.apps.PraktikumConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware'
]

ROOT_URLCONF = 'Grundlagenpraktikum.urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
    'handlers': {
        'Error.log': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class':'logging.FileHandler',
            'filename': BASE_DIR / 'Praktikum/logs/error.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
            '': {
            'handlers': ['Error.log'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'Grundlagenpraktikum.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'CONN_MAX_AGE': 60
    }
}

AUTH_USER_MODEL = "Praktikum.CustomUser"

LANGUAGE_CODE = 'de-DE'
USE_L10N = True

TIME_ZONE = 'Europe/Berlin'
USE_TZ = True
TIME_INPUT_FORMATS = ['%H:%M']

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media/')

FILE_UPLOAD_PERMISSIONS = 0o444

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login/'
LOGIN_REDIRECT_URL = '/'
SESSION_COOKIE_AGE = 86400

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

CSP_INCLUDE_NONCE_IN=['script-src']
CSP_DEFAULT_SRC=("'self'",)
CSP_OBJECT_SRC=("'none'",)
CSP_SCRIPT_SRC=("'self'",)
CSP_BASE_URI=("'none'",)
