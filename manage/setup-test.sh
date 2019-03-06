#!/bin/bash

set -eu # Exit on error and undefined var is error

MANAGE="python manage.py"

manage/setup-base.sh

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Install requirements inside venv, and check for outdated packages
echo "Installing requirements ..."
pip install --upgrade -r requirements/test.txt
pip-review
