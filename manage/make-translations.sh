#!/bin/bash

LOCAL_DIR=".local/venv"
MANAGE="manage/manage.sh"

set -eu

echo "Making translation text file ..."
$MANAGE makemessages --no-location --locale=nb
