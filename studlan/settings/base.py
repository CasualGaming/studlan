# Django settings for studlan project.
import os
import sys


PROJECT_ROOT_DIRECTORY = os.path.join(os.path.dirname(globals()['__file__']),'..')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MAX_TEAMS = 10

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('dotKom', 'dotkom@online.ntnu.no'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'
LOGIN_URL = '/auth/login/'

# Locale information
TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

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
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#1vxcq+rnraclqxt!@@4qu@9f$rj_egkirh)x)p&t1tj7xia&-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

ROOT_URLCONF = 'studlan.urls'

THEME_NAME = 'bootstrap202'

THEME_DIRECTORY = os.path.join(PROJECT_ROOT_DIRECTORY, 'themes', THEME_NAME)

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT_DIRECTORY, 'themes', THEME_NAME, 'templates'),
    ]
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT_DIRECTORY, 'themes', THEME_NAME, 'static'),
    ]

INSTALLED_APPS = (
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',

    # studlan apps
    'studlan.authentication',
    'studlan.competition',
    'studlan.lan',
    'studlan.misc',
    'studlan.news',
    'studlan.sponsor',
    'studlan.team',
    'studlan.userprofile',

    # other apps
    'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

for settings_module in ['local']:
    if not os.path.exists(PROJECT_ROOT_DIRECTORY + '/settings/' + settings_module + '.py'):
        sys.stderr.write('Could not find settings module settings/%s.py\n' % (settings_module))
        if settings_module == 'local':
            print "You need to copy the settings file 'settings/example-local.py' to 'settings/local.py'."
        sys.exit(1)
    try:
        #TODO: __import__('onlineweb.settings.' +settings_module, fromlist=['*']) does not seem to work
        if settings_module == 'local':
            from studlan.settings.local import *
    except ImportError, e:
        print 'Could not import settings for', settings_module, ': ', str(e)
        pass
