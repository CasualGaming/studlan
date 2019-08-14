#!/bin/bash

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

set -eu # Exit on error and undefined var is error

MANAGE="python manage.py"

[[ ! -e log ]] && mkdir -p log

# Add temporary config
cp setup/local.ci.test.py studlan/settings/local.py

# Validate
$MANAGE check --deploy --fail-level=ERROR

# Collect static files
echo "Collecting static files ..."
$MANAGE collectstatic --no-input --clear

# Apply migrations, but skip initial if matching table names already exist
$MANAGE migrate --fake-initial --no-input

# Check if new migrations can be made
$MANAGE makemigrations --dry-run --check --no-input

# Compiling translations
$MANAGE compilemessages --locale=nb
