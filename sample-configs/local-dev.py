# Place or mount as studlan/settings/local.py
# Remember to run "python manage.py check --deploy" to validate the settings
# This version contains settings for local development

ALLOWED_HOSTS = (
    '*'
)
SITE_NAME = 'studlan dev'
STUDLAN_FROM_MAIL = 'example@example.net'
SUPPORT_MAIL = 'example@example.net'
ADMINS = (
    ('example', 'example@example.net'),
)
CSRF_COOKIE_DOMAIN = ''
CSRF_COOKIE_NAME = 'dev-csrftoken' # Avoid domain-subdomain site interference
CSRF_COOKIE_SECURE = False # Requires HTTPS
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SESSION_COOKIE_SECURE = False # Requires HTTPS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'studlan.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
SECRET_KEY = 'UKf79mPQPRngeH9Qh5ZUegFuiIa68ctkmqiR2aqH8pXEwmL5tUaP37orzA7Gkx4M' # Randomly generate
# Dummy e-mail backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Prints to console
# Stripe
STRIPE_PUBLIC_KEY = ''
STRIPE_PRIVATE_KEY = ''
# Cal src attribute from the google embedded iframe
GOOGLE_CAL_SRC = ''
# challonge credentials
CHALLONGE_INTERGRATION_ENABLED = False
CHALLONGE_API_USERNAME = ''
CHALLONGE_API_KEY = ''
