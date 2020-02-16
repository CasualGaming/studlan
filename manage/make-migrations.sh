#!/bin/bash

LOCAL_DIR=".local/venv"
MANAGE="manage/manage.sh"

set -eu

echo "Making migrations ..."
$MANAGE makemigrations
