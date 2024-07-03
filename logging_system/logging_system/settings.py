"""
Django settings for logging_system project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yf6o7gu&-kfb6*3^%_m2kfdnd9nlc$1&@wv2va=)wj8e@kkwq*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'config',
    'devices',
    'services',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'logging_system.urls'

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

WSGI_APPLICATION = 'logging_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'logging_system',
        'USER': 'root',
        'PASSWORD': 'password123',
        'HOST': 'db',
        'PORT': '3306'

    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery Configuration Options
CELERY_TIMEZONE = "Europe/Warsaw"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'classify-every-minute': {
        'task': 'website.tasks.ml_classify_task',
        'schedule': 60.0,
        'args': (),
    },
    'train-every-week': {
        'task': 'website.tasks.ml_train_task',
        # 'schedule': crontab(hour=0, minute=0, day_of_week='sunday'),
        'schedule': 3600.0,
        'args':()
    },
    'ping-every-2-minutes': {
        'task': 'website.tasks.ping_task',
        'schedule': 300.0,
        'args':(),
    }

}

# Email SMTP Config

# def load_app_settings():
#     from config.models import Settings
#     settings = Settings.load()
#     return {
#         'EMAIL_HOST': settings.email_host,
#         'EMAIL_PORT': settings.email_port,
#         'EMAIL_HOST_USER': settings.email_host_user,
#         'EMAIL_HOST_PASSWORD': settings.email_host_password,
#         'EMAIL_USE_SSL': settings.email_use_ssl,
#         'DEFAULT_FROM_EMAIL': settings.email_from_address,
#     }

# # Update EMAIL settings
# EMAIL_CONFIG = load_app_settings()

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = EMAIL_CONFIG['EMAIL_HOST']
# EMAIL_PORT = EMAIL_CONFIG['EMAIL_PORT']
# EMAIL_HOST_USER = EMAIL_CONFIG['EMAIL_HOST_USER']
# EMAIL_HOST_PASSWORD = EMAIL_CONFIG['EMAIL_HOST_PASSWORD']
# EMAIL_USE_SSL = EMAIL_CONFIG['EMAIL_USE_SSL']
# DEFAULT_FROM_EMAIL = EMAIL_CONFIG['DEFAULT_FROM_EMAIL']

