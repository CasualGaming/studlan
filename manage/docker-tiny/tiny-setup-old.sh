#!/bin/bash

# Setup simple Docker image with requirements pre-installed to speed up simple dev commands.
# Run this command before running any "non-full" Docker management commands in here and rerun it after changing the requirements.

LOCAL_DIR=".local/docker"
LOG_DIR="$LOCAL_DIR/log"
CONFIG_FILE="studlan/settings/local.docker.py"
CONFIG_TEMPLATE_FILE="setup/local.docker.dev.py"
DB_FILE="$LOCAL_DIR/db.sqlite3"
DOCKER_FILE="setup/Dockerfile.dev"
DOCKER_IMAGE="studlan-tiny"

set -eu

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
    touch "$DB_FILE"
fi

# Add version file
echo "0.0.0-SNAPSHOT" > VERSION

echo
echo "Creating tiny Docker image ..."
docker build -f "$DOCKER_FILE" -t "$DOCKER_IMAGE" .
