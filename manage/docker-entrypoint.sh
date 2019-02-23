#!/usr/bin/env sh

set -e # Exit on error
set -u # Treat undefined variables as errors

# Check if settings exist
APP_SETTINGS_FILE=studlan/settings/local.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "App settings not found: $APP_SETTINGS_FILE" 1>&2
    exit 1
fi

# Run migration, but skip initial if matching table names already exist
python manage.py migrate --fake-initial

# Validate
python manage.py check --deploy --fail-level=ERROR

# Chown all files (this may fail for read-only volumes)
set +e
chown -R studlan:studlan .
set -e

# Run Django server using uWSGI
exec uwsgi --ini uwsgi.ini
