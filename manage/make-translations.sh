#!/bin/bash

LOCAL_DIR=".local/venv"
MANAGE="manage/manage.sh"

set -eu

echo "Making translation text file ..."
$MANAGE makemessages --no-location --locale=nb

echo "Done, now edit it and run manage/compile-translations.sh afterwards."
