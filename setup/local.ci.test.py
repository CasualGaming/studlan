# Place or mount as studlan/settings/local.py or specify it using env var CONFIG_FILE_DIR.
# WARNING: This version contains settings for testing only!

DEBUG = False

SITE_NAME = 'example'
ALLOWED_HOSTS = [
    'example.net'
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
SECRET_KEY = '00000000'

STUDLAN_FROM_MAIL = 'example@example.net'
SUPPORT_MAIL = 'example@example.net'
DEFAULT_FROM_EMAIL = STUDLAN_FROM_MAIL
REGISTER_FROM_MAIL = DEFAULT_FROM_EMAIL
ADMINS = (
    ('example', 'example@example.net'),
)

# Recommended settings that require HTTPS
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False

# Dummy e-mail backend which prints to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Mailgun (https://pypi.org/project/django-mailgun/)
# EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
# MAILGUN_ACCESS_KEY = 'ACCESS-KEY'
# MAILGUN_SERVER_NAME = 'SERVER-NAME'

# Stripe
STRIPE_PUBLIC_KEY = ''
STRIPE_PRIVATE_KEY = ''

# Cal src attribute from the google embedded iframe
GOOGLE_CAL_SRC = ''

# challonge credentials
CHALLONGE_INTEGRATION_ENABLED = False
CHALLONGE_API_USERNAME = ''
CHALLONGE_API_KEY = ''
