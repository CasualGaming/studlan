# Django settings for studlan project.
# -*- coding: utf-8 -*-

import os
import re
import sys
import raven

from django.contrib.messages import constants as message_constants

# Directory that contains this file.
PROJECT_SETTINGS_DIRECTORY = os.path.dirname(globals()['__file__'])
# Root directory. Contains manage.py
PROJECT_ROOT_DIRECTORY = os.path.join(PROJECT_SETTINGS_DIRECTORY, '..', '..')

DEBUG = True

MAX_TEAMS = 10

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('dotKom', 'dotkom@online.ntnu.no'),
)

MANAGERS = ADMINS

INSTALLED_APPS = (
    # third party apps
    'markdown_deux',
    'postman',
    'raven.contrib.django.raven_compat',

    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # studlan apps
    'apps.api',
    'apps.authentication',
    'apps.competition',
    'apps.lan',
    'apps.lottery',
    'apps.misc',
    'apps.news',
    'apps.sponsor',
    'apps.team',
    'apps.userprofile',
    'apps.seating',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
            ],
        },
    },
]


TEST_RUNNER = 'django.test.runner.DiscoverRunner'

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'
LOGIN_URL = '/auth/login/'

# Locale information
TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
SECRET_KEY = 'override-this-in-local.py'

LANGUAGES = (
    ('nb', u'Norsk'),
    ('en', u'English'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT_DIRECTORY, "files")
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

CSRF_COOKIE_PATH = '/'

ROOT_URLCONF = 'studlan.urls'

WSGI_APPLICATION = 'studlan.wsgi.application'


LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT_DIRECTORY, 'locale'),
)

MARKDOWN_DEUX_STYLES = {
    'default': {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": False,
}}

#POSTMAN SETTINGS
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_DISALLOW_COPIES_ON_REPLY = True
POSTMAN_DISABLE_USER_EMAILING = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_SHOW_USER_AS = None
POSTMAN_QUICKREPLY_QUOTE_BODY = False
POSTMAN_NOTIFIER_APP = None
POSTMAN_MAILER_APP = 'mailer'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

SUPPORT_MAIL = ''

#Overiding messagetags to match bootstrap 3
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

# Remember to keep 'local' last, so it can override any setting.
for settings_module in ['local']:  # local last
    if not os.path.exists(os.path.join(PROJECT_SETTINGS_DIRECTORY,
            settings_module + ".py")):
        sys.stderr.write("Could not find settings module '%s'.\n" %
                settings_module)
        if settings_module == 'local':
            sys.stderr.write("You need to copy the settings file "
                             "'studlan/settings/example-local.py' to "
                             "'studlan/settings/local.py'.\n")
        sys.exit(1)
    try:
        exec('from %s import *' % settings_module)
    except ImportError, e:
        print "Could not import settings for '%s' : %s" % (settings_module,
                str(e))
