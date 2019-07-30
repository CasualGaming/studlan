#!/bin/bash

LOCAL_DIR=".local/venv"
MANAGE="manage/manage.sh"
ENDPOINT="localhost:8000"

set -eu

echo "Starting Django dev server ..."
$MANAGE runserver $ENDPOINT
