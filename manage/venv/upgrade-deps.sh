#!/bin/bash

# Note: Make sure you have only the Python 2 version of pip-tools installed.
# If you only have the Python 3 version, the deps will get messed up without errors.

export CUSTOM_COMPILE_COMMAND="manage/update-deps.sh"

set -eu

# Activate venv
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate-venv.sh"
set -u

# Install pip-tools (needs to be inside venv to prevent conflict between the Python 2 and 3 versions)
python -m pip install pip-tools

[[ ! -f requirements/all.txt ]] && touch requirements/all.txt
cp requirements/all.txt requirements/all.old.txt

echo "Updating requirements files ..."
python -m pip cache purge
pip-compile --quiet --upgrade requirements/development.in
pip-compile --quiet --upgrade requirements/production.in
pip-compile --quiet --upgrade requirements/test.in
pip-compile --quiet --upgrade requirements/all.in

# Create requirements.txt for dependency analyzers etc.
echo "#" > requirements.txt
echo "# This file contains all requirements and is meant for dependency analyzers etc." >> requirements.txt
echo "# Do not use this file to install requirements, use one of the \"requirements/*.txt\" files instead." >> requirements.txt
cat requirements/all.txt >> requirements.txt

echo "Dependency changes:"
diff requirements/all.old.txt requirements/all.txt || true
rm -f requirements/all.old.txt
