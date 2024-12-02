"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import os
import mimetypes
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

envf = os.path.join(BASE_DIR, '.env')
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a=zj2!)j7o^jfb56m65f@=6zq9n#b!&b0sqd7i)%)5!g07d4)b'
SPREADSHEET_API = os.getenv('SPREADSHEET_API')
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_browser_reload",
    "django.contrib.humanize",
    'taggit',
    # internal apps
    'ecommerce.abstract',
    'ecommerce.account',
    'ecommerce.order',
    'ecommerce.product',
    'ecommerce.htmx_messages',
    'ecommerce.home',
    # 3d party apps
    'sorl.thumbnail',
    'simple_menu',
    'django_sass',
    "django_htmx",
    'compressor',
    'djmoney',
    'silk',
    'django_filters',
    'crispy_forms',
    "crispy_bootstrap4",
    'storages',
    'dbbackup',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True
#
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'ecommerce.htmx_messages.middleware.HtmxMessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    'django_ratelimit.middleware.RatelimitMiddleware',
]

RATELIMIT_VIEW = 'ecommerce.abstract.views.beenLimited'

AUTH_USER_MODEL = 'account.User'

ROOT_URLCONF = 'ecommerce.urls'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# commented out for now since we are using s3 buckets
#

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "rich": {"datefmt": "[%X]"},
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "filters": ["require_debug_true"],
            "formatter": "rich",
            "level": "DEBUG",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": [],
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
INTERNAL_IPS = [
    "127.0.0.1",
]

SILKY_IGNORE_PATHS = [
    '/admin/jsi18n/'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

USE_RDS = bool(int(os.getenv('USE_RDS', False)))
if USE_RDS:
    DB_NAME = os.getenv('RDB_NAME')
    DB_USER = os.getenv('RDB_USER')
    DB_PASS = os.getenv('RDB_PASS')
    DB_HOST = os.getenv('RDB_HOST')
    DB_PORT = os.getenv('RDB_PORT')

else:
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

os.mkdir(os.path.join(BASE_DIR, 'static')) if not os.path.exists(os.path.join(BASE_DIR, 'static')) else None

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CURRENCIES = ('USD', 'IQD')
mimetypes.add_type("text/css", ".css", True)

# light, medium and heavy here to referece the importance of the request(login is heavy while home screen is light)
LIGHT_REQUESTS_RATE_LIMIT = '250/m'
MEDIUM_REQUESTS_RATE_LIMIT = '100/m'
HEAVY_REQUESTS_RATE_LIMIT = '50/m'
# LIGHT_REQUESTS_RATE_LIMIT = '25/m'
# MEDIUM_REQUESTS_RATE_LIMIT = '10/m'
# HEAVY_REQUESTS_RATE_LIMIT = '5/m'

USE_S3 = bool(int(os.getenv('USE_S3', False)))
if USE_S3:
    CORS_ALLOW_ALL_ORIGINS = True
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_ACL = 'public-read'
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'

    STATICFILES_STORAGE = 'ecommerce.storage_backends.StaticStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'ecommerce.storage_backends.PublicMediaStorage'
    STORAGES = {
        "default": {
            "BACKEND": "ecommerce.storage_backends.PublicMediaStorage",
        },
        "staticfiles": {
            "BACKEND": "ecommerce.storage_backends.StaticStorage",
        },
    }

else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
    }
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]




DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'db_backup/'}
DBBACKUP_POSTGRESQL_OPTIONS = '--no-owner'
DBBACKUP_POSTGRESQL_PGDUMP_OPTIONS = '--no-owner'


