#!/bin/bash

# Note: Make sure you have only the Python 2 version of pip-tools installed.
# If you only have the Python 3 version, the deps will get messed up without errors.

export CUSTOM_COMPILE_COMMAND="manage/update-deps.sh"

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

# Install pip-tools (needs to be inside venv to prevent conflict between the Python 2 and 3 versions)
pip install pip-tools

[[ ! -f requirements/all.txt ]] && touch requirements/all.txt
cp requirements/all.txt requirements/all.old.txt

echo "Updating requirements files ..."
pip-compile --quiet --upgrade requirements/development.in
pip-compile --quiet --upgrade requirements/production.in
pip-compile --quiet --upgrade requirements/test.in
pip-compile --quiet --upgrade requirements/all.in
# For dependency analyzers etc.
cp requirements/all.in requirements.txt

echo "Dependency changes:"
diff requirements/all.old.txt requirements/all.txt || true

rm -f requirements/all.old.txt
