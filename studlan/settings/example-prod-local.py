# -*- coding: utf-8 -*-
DEBUG = False

SECRET_KEY = 'CHANGEME'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db_name',                      # Or path to database file if using sqlite3.
        'USER': 'db_user',                      # Not used with sqlite3.
        'PASSWORD': 'db_pw',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STUDLAN_FROM_MAIL = 'noreply@domain.no'
SUPPORT_MAIL = 'change@me.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # real
EMAIL_HOST = "smtp.domain.no"
DEFAULT_FROM_EMAIL = STUDLAN_FROM_MAIL
REGISTER_FROM_MAIL = DEFAULT_FROM_EMAIL
EMAIL_PORT = 25

SITE_NAME = "THIS LAN"
ALLOWED_HOSTS = [
    "domain.no",
]

#Enable and set to your domain when deployed
CSRF_COOKIE_DOMAIN = 'domain.no'
CSRF_COOKIE_HTTPONLY = True

STRIPE_PUBLIC_KEY = 'pk_live_xxxxxxxxxxxxxxxxxxxxxx'

STRIPE_PRIVATE_KEY = 'sk_live_xxxxxxxxxxxxxxxxxxxxxxxx'


#Settings for Sentry
#DSN adress is accessable on sentry.io
RAVEN_CONFIG = {
    'dsn': 'https://*****@sentry.io/******'
}

# Cal src attribute from the google embedded iframe
GOOGLE_CAL_SRC = ''

# challonge credentials
CHALLONGE_INTERGRATION_ENABLED = False
CHALLONGE_API_USERNAME = ''
CHALLONGE_API_KEY = ''
