# -*- coding: utf-8 -*-

import os
import sys

from django.contrib.messages import constants as message_constants

from environs import Env

# Directory that contains this file.
PROJECT_SETTINGS_DIRECTORY = os.path.dirname(globals()['__file__'])
# Root directory. Contains manage.py
PROJECT_ROOT_DIRECTORY = os.path.normpath(os.path.join(PROJECT_SETTINGS_DIRECTORY, '..', '..'))

INSTALLED_APPS = (
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Studlan apps
    'apps.api.config.Config',
    'apps.arrivals.config.Config',
    'apps.authentication.config.Config',
    'apps.competition.config.Config',
    'apps.lan.config.Config',
    'apps.lottery.config.Config',
    'apps.news.config.Config',
    'apps.payment.config.Config',
    'apps.poll.config.Config',
    'apps.seating.config.Config',
    'apps.sendmail.config.Config',
    'apps.sponsor.config.Config',
    'apps.statistics.config.Config',
    'apps.team.config.Config',
    'apps.userprofile.config.Config',
    'apps.misc.config.Config',

    # Third-party apps
    'markdown_deux',
    'postman',
    'anymail',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT_DIRECTORY, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'apps.misc.context_processors.global_variables',
            ],
        },
    },
]

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
ROOT_URLCONF = 'studlan.urls'
WSGI_APPLICATION = 'studlan.wsgi.application'
AUTH_PROFILE_MODULE = 'userprofile.UserProfile'
LOGIN_URL = '/auth/login/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SITE_ID = 1
# SITE_NAME = Example
# ALLOWED_HOSTS = [
#     SITE_HOST
# ]

# Locale information
TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT_DIRECTORY, 'locale'),
)

LANGUAGES = (
    ('nb', 'Norsk'),
    ('en', 'English'),
)

# Media and static files
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = ''
# URL that handles the media served from MEDIA_ROOT.
# Make sure to use a trailing slash.
MEDIA_URL = ''
# Absolute path to the directory static files should be collected to.
STATIC_ROOT = 'static/'
# URL prefix for static files.
STATIC_URL = '/static/'
# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
ADMIN_MEDIA_PREFIX = '/static/admin/'
# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT_DIRECTORY, 'files'),
]
# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Security
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

MARKDOWN_DEUX_STYLES = {
    'default': {
        'extras': {
            'code-friendly': None,
        },
        'safe_mode': False,
    },
}


# Postman
# Used for internal invitation messages
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_DISALLOW_COPIES_ON_REPLY = True
POSTMAN_DISABLE_USER_EMAILING = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_SHOW_USER_AS = None
POSTMAN_QUICKREPLY_QUOTE_BODY = False
POSTMAN_NOTIFIER_APP = None
POSTMAN_MAILER_APP = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/warning.log',
            'maxBytes': 8 * 1024 * 1024,  # 8 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/error.log',
            'maxBytes': 8 * 1024 * 1024,  # 8 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'payment_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/payment.log',
            'maxBytes': 8 * 1024 * 1024,  # 8 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'sendmail_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/sendmail.log',
            'maxBytes': 8 * 1024 * 1024,  # 8 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['warning_file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'payment': {
            'handlers': ['payment_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sendmail': {
            'handlers': ['sendmail_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# Overiding messagetags to match bootstrap 3
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

# Version
VERSION = 'Unknown version'
version_file_path = os.path.join(PROJECT_ROOT_DIRECTORY, 'VERSION')
if os.path.isfile(version_file_path):
    with open(version_file_path, 'r') as version_file:
        content = version_file.read()
    content = content.strip()
    if (content):
        VERSION = content

env = Env()
env.read_env()

with env.prefixed("STUDLAN_"):
    DEBUG = env.bool("DEBUG", default=False)

    SITE_NAME = env.str("SITE_NAME", default="example")

    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

    DATABASES = {"default": env.dj_db_url("DATABASE_URL")}

    SECRET_KEY = env.str("SECRET_KEY")

    # Recommended settings that require HTTPS
    CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
    SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=False)
    SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)

    # Email
    # Use this backend for local testing
    EMAIL_BACKEND = env.str("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
    # Use this backend in production
    # EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
    ANYMAIL = {
        'MAILGUN_API_KEY': env.str("ANYMAIL_MAILGUN_API_KEY", default=""),
        'MAILGUN_SENDER_DOMAIN': env.str("ANYMAIL_MAILGUN_SENDER_DOMAIN", default=""),
    }
    STUDLAN_FROM_MAIL = env.str("STUDLAN_FROM_MAIL", default="")
    DEFAULT_FROM_EMAIL = STUDLAN_FROM_MAIL
    REGISTER_FROM_MAIL = STUDLAN_FROM_MAIL
    SERVER_EMAIL = STUDLAN_FROM_MAIL
    SUPPORT_MAIL = env.str("SUPPORT_MAIL", default="")

    # Stripe
    STRIPE_PUBLIC_KEY = env.str("STRIPE_PUBLIC_KEY", default="")
    STRIPE_PRIVATE_KEY = env.str("STRIPE_PRIVATE_KEY", default="")

    # Cal src attribute from the google embedded iframe
    GOOGLE_CAL_SRC = env.str("GOOGLE_CAL_SRC", default="")

    # challonge credentials
    CHALLONGE_INTEGRATION_ENABLED = env.bool("CHALLONGE_INTEGRATION_ENABLED", default=False)
    CHALLONGE_API_USERNAME = env.str("CHALLONGE_API_USERNAME", default="")
    CHALLONGE_API_KEY = env.str("CHALLONGE_API_KEY", default="")

    # Plausible
    PLAUSIBLE_ENABLE = env.bool("PLAUSIBLE_ENABLE", default=False)
    PLAUSIBLE_LOCAL_DOMAIN = env.str("PLAUSIBLE_LOCAL_DOMAIN", default='localhost')
    PLAUSIBLE_REMOTE_DOMAIN = env.str("PLAUSIBLE_REMOTE_DOMAIN", default='localhost')

    # Show studlan version in footer
    SHOW_VERSION = env.bool("SHOW_VERSION", default=False)

    MAX_TEAMS = env.int("MAX_TEAMS", 10)

# Compatibility
# When django-anymail[mailgun] replaced django-mailgun
if EMAIL_BACKEND == 'django_mailgun.MailgunBackend':
    EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
if 'MAILGUN_ACCESS_KEY' in globals() and not ANYMAIL['MAILGUN_API_KEY']:
    ANYMAIL['MAILGUN_API_KEY'] = MAILGUN_ACCESS_KEY  # noqa: F821 (undefined name)
if 'MAILGUN_SERVER_NAME' in globals() and not ANYMAIL['MAILGUN_SENDER_DOMAIN']:
    ANYMAIL['MAILGUN_SENDER_DOMAIN'] = MAILGUN_SERVER_NAME  # noqa: F821 (undefined name)
