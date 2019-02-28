#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

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

# Create empty required files and directories
[[ ! -e studlan.db ]] && touch studlan.db
[[ ! -e log ]] && mkdir -p log

# Add dev app settings
APP_SETTINGS_FILE=studlan/settings/local.py
DEV_APP_SETTINGS_FILE=sample-configs/local-dev.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "Using sample local.py ..."
    cp $DEV_APP_SETTINGS_FILE $APP_SETTINGS_FILE
fi
