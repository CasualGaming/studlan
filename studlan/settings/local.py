# App settings used when running the application locally during development
# Replace this file somehow in production, e.g. using a Docker volume

ALLOWED_HOSTS = (
    '*'
)
SITE_NAME = 'example'
STUDLAN_FROM_MAIL = 'example@example.net'
SUPPORT_MAIL = 'example@example.net'
ADMINS = (
    ('example', 'example@example.net'),
)

SECRET_KEY = 'UKf79mPQPRngeH9Qh5ZUegFuiIa68ctkmqiR2aqH8pXEwmL5tUaP37orzA7Gkx4M'

CSRF_COOKIE_DOMAIN = ''
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tmp/studlan.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # prints
