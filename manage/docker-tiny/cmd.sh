#!/bin/bash

# Run basic stuff.
# Accepts commands as one command per arguments.

set -eu

LOCAL_DIR=".local/docker-tiny"
CONFIG_FILE="$LOCAL_DIR/local.py"
DB_FILE="$LOCAL_DIR/db.sqlite3"
DC_FILE="setup/docker-compose.tiny.yml"
DC="docker-compose -f $DC_FILE"

cmds=""
for cmd in "$@"; do
    cmds="$cmds"$'\n'
    cmds="$cmds$cmd"
done

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

$DC run --rm app <<< "$cmds"

echo
echo "Success (seemingly)!"
