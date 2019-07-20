#!/bin/bash

LOCAL_DIR=".local/docker"
CONFIG_FILE="studlan/settings/local.docker.py"
CONFIG_TEMPLATE_FILE="setup/local.docker.dev.py"
DB_FILE="$LOCAL_DIR/db.sqlite3"
DC_FILE="setup/docker-compose.dev.yml"
DC="docker-compose -f $DC_FILE"

set -eu

mkdir -p $LOCAL_DIR

# Add config file and exit if missing
if [[ ! -e $CONFIG_FILE ]]; then
    echo "Creating new config file ..."
    cp $CONFIG_TEMPLATE_FILE $CONFIG_FILE
fi

# Create DB file so Docker doesn't make it a directory
if [[ ! -e $DB_FILE ]]; then
    echo "Creating DB file ..."
    touch $DB_FILE
fi

echo
echo "Removing any previous Docker Compose setup ..."
$DC down

echo
echo "Building image ..."
$DC build app

echo
echo "Creating containers ..."
$DC up --no-start
