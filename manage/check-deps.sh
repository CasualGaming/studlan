#!/bin/bash

set -eu # Exit on error and undefined var is error

# Setup virtual environment to install packages and stuff inside
if [[ ! -d .venv ]]; then
    echo "Creating venv ..."
    # Don't use symlinks if in VirtualBox shared folder
    if ( df -t vboxsf . 1>/dev/null 2>/dev/null ); then
        echo "VirtualBox shared folder detected"
        virtualenv -p $(which python2) --always-copy .venv
    else
        virtualenv -p $(which python2) .venv
    fi
fi

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

echo "Installing all dependencies ..."
pip install -r requirements/development.txt
pip install -r requirements/production.txt
pip install -r requirements/test.txt

echo && echo "Checking for outdated dependencies (among all installed packages) ..."
pip-review
