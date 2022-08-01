#!/bin/bash

# Setup for running the full application.

set -eu -o pipefail

LOCAL_DIR=".local/docker-full"
LOG_DIR="$LOCAL_DIR/log"
CONFIG_FILE="$LOCAL_DIR/local.py"
CONFIG_TEMPLATE_FILE="setup/local.docker.py"
DB_FILE="$LOCAL_DIR/db/db.sqlite3"
DC_FILE="setup/docker-compose.full.yml"
DC="docker-compose -f $DC_FILE"

mkdir -p "$LOCAL_DIR"
mkdir -p "$LOG_DIR"

# Add config file and exit if missing
if [[ ! -e $CONFIG_FILE ]]; then
    echo "Creating new config file ..."
    cp "$CONFIG_TEMPLATE_FILE" "$CONFIG_FILE"
fi

echo "Creating DB file ..."
mkdir -p "$(dirname "$DB_FILE")"
chmod 777 "$(dirname "$DB_FILE")"
touch "$DB_FILE"
chmod 666 "$DB_FILE"

# Add version file
echo "0.0.0-SNAPSHOT" > VERSION

echo
echo "Removing any previous Docker Compose setup ..."
$DC down

echo
echo "Building image ..."
$DC build studlan

echo
echo "Creating containers ..."
$DC up --no-start
