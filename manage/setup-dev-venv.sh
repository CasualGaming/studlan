#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

# Install basic requirements
pip install --upgrade pip virtualenv setuptools wheel

# Remove old venv
if [[ -e "venv" ]]; then
    echo "Removing old venv"
    rm -rf venv
fi

# Setup virtual environment to install packages and stuff inside
# Don't use symlinks if in VirtualBox shared folder
if ( df -t vboxsf . 1>/dev/null 2>/dev/null ); then
    echo "VirtualBox shared folder detected"
    virtualenv -p $(which python2) --always-copy venv
else
    virtualenv -p $(which python2) venv
fi

# Activate venv and deactivate on exit
source venv/bin/activate
trap deactivate EXIT

# Install requirements inside venv
pip install --upgrade -r requirements/development.txt
