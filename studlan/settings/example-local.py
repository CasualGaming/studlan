
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dev.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STUDLAN_FROM_MAIL = 'studlan@online.ntnu.no'
SUPPORT_MAIL = 'change@me.com'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # real
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # prints

SITE_NAME = 'studLAN'

# Enable and set to your domain when deployed
# CSRF_COOKIE_DOMAIN = 'studlan.no'
CSRF_COOKIE_HTTPONLY = True

STRIPE_PUBLIC_KEY = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

STRIPE_PRIVATE_KEY = 'sk_test_BQokikJOvBiI2HlWgH4olfQ2'


#Settings for Sentry
RAVEN_CONFIG = {
    'dsn': 'https://***@sentry.io/213600',
}
SENTRY_DSN=None

# Cal src attribute from the google embedded iframe
GOOGLE_CAL_SRC = ''

# challonge credentials
CHALLONGE_API_USERNAME = ''
CHALLONGE_API_KEY = ''
