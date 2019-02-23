#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Validate
python manage.py check --deploy --fail-level=ERROR

# Run unit tests or whatever
python manage.py test

# Run tox
#if ( df -t vboxsf . 1>/dev/null 2>/dev/null ); then
#    echo "VirtualBox shared folder detected"
#    tox -c tox-vbox.ini
#else
#    tox -c tox.ini
#fi
