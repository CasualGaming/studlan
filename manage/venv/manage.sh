#!/bin/bash

MANAGE="python manage.py"
CONFIG_FILE="studlan/settings/local.py"
LOCAL_DIR=".local/venv"
LOG_DIR="$LOCAL_DIR/log"

# Check if settings exist
if [[ ! -e $CONFIG_FILE ]]; then
    echo "Config file not found: $CONFIG_FILE" 1>&2
    exit 1
fi

# Activate venv
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate-venv.sh"
set -u

mkdir -p $LOCAL_DIR
mkdir -p $LOG_DIR

$MANAGE $@
