#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

manage/setup-base-venv.sh

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Install requirements inside venv
echo "Installing requirements ..."
pip install --upgrade -r requirements/development.txt

# Collect static files
echo "Collecting static files ..."
python manage.py collectstatic --noinput --clear

# Run migration, but skip initial if matching table names already exist
echo "Running migration ..."
python manage.py migrate --fake-initial

# Add superuser
echo "Adding superuser ..."
echo "Press CTRL+C to cancel"
python manage.py createsuperuser
