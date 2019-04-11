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

[[ ! -f requirements/all.txt ]] && touch requirements/all.txt
cp requirements/all.txt requirements/all.old.txt

echo "Temporarily updating requirements files ..."
pip-compile --quiet --upgrade --output-file requirements/all.tmp.txt requirements/all.in

echo "Dependency updates:"
diff requirements/all.old.txt requirements/all.tmp.txt || true

rm -f requirements/all.old.txt
rm -f requirements/all.tmp.txt
