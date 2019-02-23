#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

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

# Run (WARNING: Not restricted to localhost)
python manage.py runserver 0.0.0.0:8080
