#!/bin/bash

set -eu # Exit on error and undefined var is error

MANAGE="python manage.py"

# Check if settings exist
APP_SETTINGS_FILE=studlan/settings/local.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "App settings not found: $APP_SETTINGS_FILE" 1>&2
    exit 1
fi

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Collect static files
echo "Collecting static files ..."
$MANAGE collectstatic --no-input --clear

# Run migration, but skip initial if matching table names already exist
echo "Running migration ..."
$MANAGE migrate --fake-initial --no-input

# Check if new migrations can be made
$MANAGE makemigrations --dry-run --check --no-input

# Validate
echo "Checking validity ..."
$MANAGE check --deploy --fail-level=ERROR

# Run Django tests
$MANAGE test --no-input

# Run flake8 static code analysis
# Uses settings from .flake8
flake8
