#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

# Check if settings exist
APP_SETTINGS_FILE=studlan/settings/local.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "App settings not found: $APP_SETTINGS_FILE" 1>&2
    exit 1
fi

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Collect new static files
echo "Collecting new static files ..."
python manage.py collectstatic --noinput

# Run migration, but skip initial if matching table names already exist
echo "Running migration ..."
python manage.py migrate --fake-initial

# Validate
echo "Checking validity ..."
python manage.py check --deploy --fail-level=ERROR

# Run unit tests or whatever
echo "Running tests ..."
python manage.py test
