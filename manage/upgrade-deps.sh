#!/bin/bash

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

echo "Copying *.txt to *.old.txt"
[[ ! -f requirements/development.txt ]] && touch requirements/development.txt
[[ ! -f requirements/production.txt ]] && touch requirements/production.txt
[[ ! -f requirements/test.txt ]] && touch requirements/test.txt
cp requirements/development.txt requirements/development.old.txt
cp requirements/production.txt requirements/production.old.txt
cp requirements/test.txt requirements/test.old.txt

echo "Updating requirements files ..."
pip-compile --quiet --upgrade requirements/development.in
pip-compile --quiet --upgrade requirements/production.in
pip-compile --quiet --upgrade requirements/test.in

echo; echo "Changes in development.txt:"
diff requirements/development.old.txt requirements/development.txt || true
echo; echo "Changes in production.txt:"
diff requirements/production.old.txt requirements/production.txt || true
echo; echo "Changes in test.txt:"
diff requirements/test.old.txt requirements/test.txt || true
