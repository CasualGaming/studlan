# -*- coding: utf-8 -*-

import os
import sys

from django.contrib.messages import constants as message_constants

# Directory that contains this file.
PROJECT_SETTINGS_DIRECTORY = os.path.dirname(globals()['__file__'])
# Root directory. Contains manage.py
PROJECT_ROOT_DIRECTORY = os.path.normpath(os.path.join(PROJECT_SETTINGS_DIRECTORY, '..', '..'))

DEBUG = False

ADMINS = (
    ('example', 'example@example.net'),
)

MANAGERS = ADMINS

INSTALLED_APPS = (
    # third party apps
    'markdown_deux',
    'postman',

    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # studlan apps
    'apps.api.config.Config',
    'apps.arrivals.config.Config',
    'apps.authentication.config.Config',
    'apps.competition.config.Config',
    'apps.lan.config.Config',
    'apps.lottery.config.Config',
    'apps.misc.config.Config',
    'apps.news.config.Config',
    'apps.payment.config.Config',
    'apps.seating.config.Config',
    'apps.sponsor.config.Config',
    'apps.team.config.Config',
    'apps.userprofile.config.Config',
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

LANGUAGES = (
    ('nb', u'Norsk'),
    ('en', u'English'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/media/'
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/'
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'
STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: 'http://media.lawrence.com/static/'
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: 'http://foo.com/static/admin/', '/static/admin/'.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT_DIRECTORY, 'files'),
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

ROOT_URLCONF = 'studlan.urls'

WSGI_APPLICATION = 'studlan.wsgi.application'

LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT_DIRECTORY, 'locale'),
)

MARKDOWN_DEUX_STYLES = {
    'default': {
        'extras': {
            'code-friendly': None,
        },
        'safe_mode': False,
    },
}

# Postman
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_DISALLOW_COPIES_ON_REPLY = True
POSTMAN_DISABLE_USER_EMAILING = True
POSTMAN_AUTO_MODERATE_AS = True
POSTMAN_SHOW_USER_AS = None
POSTMAN_QUICKREPLY_QUOTE_BODY = False
POSTMAN_NOTIFIER_APP = None
POSTMAN_MAILER_APP = 'mailer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'error_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'log/error.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# Max teams a user can lead
MAX_TEAMS = 10

# Overiding messagetags to match bootstrap 3
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

VERSION = 'Unknown version'
version_file_path = os.path.join(PROJECT_ROOT_DIRECTORY, 'VERSION')
if os.path.isfile(version_file_path):
    with open(version_file_path, 'r') as version_file:
        content = version_file.read()
    content = content.strip()
    if (content):
        VERSION = content

# Remember to keep 'local' last, so it can override any setting.
for settings_module in ['local']:  # local last
    if not os.path.exists(os.path.join(PROJECT_SETTINGS_DIRECTORY, settings_module + '.py')):
        sys.stderr.write(u'Could not find settings module "{0}".\n'.format(settings_module))
        if settings_module == 'local':
            sys.stderr.write('You need to add the settings file "studlan/settings/local.py".\n')
        sys.exit(1)
    try:
        exec(u'from {0} import *'.format(settings_module))  # noqa: S102
    except ImportError as e:
        print(u'Could not import settings for "{0}" : {1}'.format(settings_module, str(e)))  # noqa: T001
