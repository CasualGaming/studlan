#!/bin/bash

# Run the dev server with hot reload. Uses either specified endpoint or localhost:8000 by default.

LOCAL_DIR=".local/venv"
MANAGE="manage/manage.sh"
DEFAULT_ENDPOINT="localhost:8000"

set -eu

if (( $# > 0 )); then
    ENDPOINT="$1"
else
    ENDPOINT="$DEFAULT_ENDPOINT"
fi

echo "Starting Django dev server ..."
$MANAGE runserver "$ENDPOINT"
