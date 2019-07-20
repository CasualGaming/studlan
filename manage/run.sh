#!/bin/bash

LOCAL_DIR=".local/venv"
MANAGE="manage/manage.sh"
ENDPOINT="localhost:8000"

set -eu

# Activate venv and deactivate on exit
# Allow undefined vars
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate-venv.sh"
trap deactivate EXIT
set -u

echo "Starting Django dev server ..."
$MANAGE runserver $ENDPOINT
