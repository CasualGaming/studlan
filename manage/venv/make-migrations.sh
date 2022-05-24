#!/bin/bash

LOCAL_DIR=".local/venv"
MANAGE="manage/venv/manage.sh"

set -eu

echo "Making migrations ..."
$MANAGE makemigrations
