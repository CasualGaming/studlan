#!/bin/bash

LOCAL_DIR=".local/venv"
MANAGE="manage/venv/manage.sh"

set -eu

echo "Making translation text file ..."
$MANAGE makemessages --no-location --no-wrap --locale=nb
