#!/bin/bash

# Run the full application.

set -eu

LOCAL_DIR=".local/docker-full"
CONFIG_FILE="$LOCAL_DIR/local.py"
DB_FILE="$LOCAL_DIR/db.sqlite3"
DC_FILE="setup/docker-compose.full.yml"
DC="docker-compose -f $DC_FILE"

# Check if config file exists
if [[ ! -e $CONFIG_FILE ]]; then
    echo "App config not found: $CONFIG_FILE" 1>&2
    exit -1
fi

# Check if DB file exists
if [[ ! -e $DB_FILE ]]; then
    echo "DB file not found: $DB_FILE" 1>&2
    exit -1
fi

$DC up
$DC down
