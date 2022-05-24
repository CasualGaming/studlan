#!/bin/bash

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

echo "Temporarily updating requirements files ..."
python -m pip cache purge
pip-compile --quiet --upgrade --output-file requirements/all.tmp.txt requirements/all.in

echo "Dependency updates:"
diff requirements/all.old.txt requirements/all.tmp.txt || true

rm -f requirements/all.old.txt
rm -f requirements/all.tmp.txt
