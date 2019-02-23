#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

# Setup virtual environment to install packages and stuff inside
if [[ ! -d .venv ]]; then
    # Don't use symlinks if in VirtualBox shared folder
    if ( df -t vboxsf . 1>/dev/null 2>/dev/null ); then
        echo "VirtualBox shared folder detected"
        virtualenv -p $(which python2) --always-copy .venv
    else
        virtualenv -p $(which python2) .venv
    fi
fi

# Add dev app settings
APP_SETTINGS_FILE=studlan/settings/local.py
DEV_APP_SETTINGS_FILE=sample-configs/local-dev.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    cp $DEV_APP_SETTINGS_FILE $APP_SETTINGS_FILE
fi
