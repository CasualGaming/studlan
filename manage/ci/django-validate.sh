#!/bin/bash

set -eu -o pipefail

LOCAL_DIR=".local/ci"
LOG_DIR="$LOCAL_DIR/log"
CONFIG_FILE="studlan/settings/local.py"
CONFIG_TEMPLATE_FILE="setup/local.ci.py"
DB_FILE="$LOCAL_DIR/db/db.sqlite3"
MANAGE="python manage.py"

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

mkdir -p "$LOCAL_DIR"
mkdir -p "$LOG_DIR"

# Add config file and exit if missing
if [[ ! -e $CONFIG_FILE ]]; then
    echo "Creating new config file ..."
    cp "$CONFIG_TEMPLATE_FILE" "$CONFIG_FILE"
fi

# Create DB file so Docker doesn't make it a directory
if [[ ! -e $DB_FILE ]]; then
    echo "Creating DB file ..."
    mkdir -p "$(dirname "$DB_FILE")"
    chmod 777 "$(dirname "$DB_FILE")"
    touch "$DB_FILE"
    chmod 666 "$DB_FILE"
fi

# Add version file
echo "0.0.0-SNAPSHOT" > VERSION

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

# Run Django tests
$MANAGE test
