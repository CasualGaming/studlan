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

exec uwsgi --ini uwsgi.ini
