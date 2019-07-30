#!/bin/bash

# Runs linter.

MANAGE="python manage.py"

set -eu

# Activate venv and deactivate on exit
# Allow undefined vars
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate-venv.sh"
trap deactivate EXIT
set -u

# Run flake8 static code analysis
# Uses settings from .flake8
flake8
