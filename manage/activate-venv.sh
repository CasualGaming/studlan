#!/bin/bash

# Notes:
# - Do not use "set -u" before sourcing this script, virtualenv's activate script may trigger it.
# - Make sure the user bin dir is added to PATH

SYSTEM_PACKAGES="virtualenv setuptools wheel"
VENV_DIR=".venv"

# Windows uses "python" and "pip" for both Python 2 and 3
# Linux uses "python" and "pip" for Python 2 only
if [[ $(uname -s) == "MINGW"* ]]; then
    PIP2_CMD="py -2 -m pip"
    VENV_CMD="py -2 -m virtualenv"
    VENV_ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
else
    PIP2_CMD="pip"
    VENV_CMD="virtualenv -p \"$(which python)\""
    VENV_ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
fi

# Create venv if missing
if [[ ! -e $VENV_DIR ]]; then
    echo "Virtualenv not found, creating it ..."

    # Users need "--user", while CI doesn't allow it
    if [[ $CI == "true" ]]; then
        $PIP2_CMD install $SYSTEM_PACKAGES
    else
        $PIP2_CMD install --user $SYSTEM_PACKAGES --no-warn-script-location
    fi

    $VENV_CMD $VENV_DIR
fi

# Enter venv
source $VENV_ACTIVATE_SCRIPT
