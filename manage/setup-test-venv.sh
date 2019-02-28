#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

manage/setup-base-venv.sh

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Install requirements inside venv
echo "Installing requirements ..."
pip install --upgrade -r requirements/test.txt

# Collect static files
echo "Collecting static files ..."
python manage.py collectstatic --noinput --clear
