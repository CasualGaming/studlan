#!/bin/bash

set -eu # Exit on error and undefined var is error

MANAGE="python manage.py"

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Run flake8 static code analysis
# Uses settings from .flake8
flake8
