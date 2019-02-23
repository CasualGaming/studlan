#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

manage/setup-base-venv.sh

# Activate venv and deactivate on exit
source .venv/bin/activate
trap deactivate EXIT

# Install requirements inside venv
pip install --upgrade -r requirements/test.txt
