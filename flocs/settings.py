"""
Django settings for flocs project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-zocq!_l$gw_@cc1u7l$7j8y=b&+t2e4^e9bmx1&rk0ztp*&dj'

ON_STAGING = os.getenv('ON_STAGING', "False") == "True"
ON_PRODUCTION = os.getenv('ON_AL', "False") == "True" and not ON_STAGING
DEVELOPMENT = not ON_STAGING and not ON_PRODUCTION
DEBUG = (not ON_PRODUCTION) or (os.getenv('DJANGO_DEBUG', "False") == "True")
ALLOWED_HOSTS = [
    '.thran.cz'
]

if ON_PRODUCTION or ON_STAGING:
    FRONTEND_BUILD_DIR = os.path.join(BASE_DIR, 'frontend', 'production-build')
else:
    FRONTEND_BUILD_DIR = os.path.join(BASE_DIR, 'frontend', 'development-build')


# Application definition

INSTALLED_APPS = (
    'modeltranslation', # must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'import_export',
    'lazysignup',
    # our apps
    'common',
    'feedback',
    'tasks',
    'practice',
    'flocs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'flocs.aspects.localization.LocalizationMiddleware',
)

ROOT_URLCONF = 'flocs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # frontend home directory (where to search for index.html)
        'DIRS': [FRONTEND_BUILD_DIR],

        # allow for fallback index.html in flocs/templates/
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

WSGI_APPLICATION = 'flocs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))}


# Internationalization
USE_I18N = True
USE_L10N = True
USE_TZ = False
#TIME_ZONE = 'UTC'
LANGUAGES = [
    ('cs', 'Czech'),
    ('en', 'English')
]
if ON_PRODUCTION:
    LANGUAGE_DOMAINS = {
        'cs': 'flocs.thran.cz',
        'en': 'en.flocs.thran.cz',
    }
elif ON_STAGING:
    LANGUAGE_DOMAINS = {
        'cs': 'staging.flocs.thran.cz',
        'en': 'en.staging.flocs.thran.cz',
    }
else:
    LANGUAGE_DOMAINS = {
        'cs': 'localhost:8000',
        'en': 'en.localhost:8000',
    }
LANGUAGE_CODE = 'cs'  # fallback language
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_TRANSLATION_FILES = (
    'tasks.models.translation',
    'practice.models.translation',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(FRONTEND_BUILD_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, '../static')


AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'lazysignup.backends.LazySignupBackend',
)

# --------------------------------------------------------------------------
# Email
# --------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = '[flocs]'
EMAIL_ADMINS = ['adaptive-programming@googlegroups.com']
SERVER_EMAIL = 'error-reporting@flocs.thran.cz'
ADMINS = (('Errors', 'adaptive-programming-errors@googlegroups.com'),)
if DEVELOPMENT:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------
LOGGING_DIR = os.getenv('LOGGING_DIR', "logs")
LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s'
        },
        'long-messages': {
            'format': '[%(asctime)s] %(message)s----------'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(module)s : "%(message)s" in %(filename)s:%(lineno)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'practice-file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR + '/practice.log',
            'formatter': 'verbose'
        },
        'feedback-file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR + '/feedback.log',
            'formatter': 'long-messages'
        },
        'requests-file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR + '/requests.log',
            'formatter': 'simple'
        },
        'mail-admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'feedback': {
            'handlers': ['feedback-file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'practice': {
            'handlers': ['practice-file'],
            'level': 'DEBUG',
            'propagate': True
            },
        'django.request' : {
            'handlers': ['requests-file', 'mail-admins'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
