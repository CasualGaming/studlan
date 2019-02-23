#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

# Check if settings exist
APP_SETTINGS_FILE=studlan/settings/local.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "App settings not found: $APP_SETTINGS_FILE" 1>&2
    exit 1
fi

[[ ! -e tmp ]] && mkdir -p tmp
[[ ! -e tmp/studlan.db ]] && touch tmp/studlan.db
[[ ! -e tmp/log ]] && mkdir -p tmp/log

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Run migration, but skip initial if matching table names already exist
python manage.py migrate --fake-initial

exec uwsgi --ini uwsgi.ini
