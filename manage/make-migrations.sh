#!/bin/bash

LOCAL_DIR=".local/venv"
MANAGE="manage/manage.sh"

set -eu

# Activate venv and deactivate on exit
# Allow undefined vars
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate-venv.sh"
trap deactivate EXIT
set -u

echo "Making migrations ..."
$MANAGE makemigrations
