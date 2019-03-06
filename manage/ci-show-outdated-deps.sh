#!/bin/bash

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

set -eu # Exit on error and undefined var is error

echo "Installing all dependencies ..."
pip install --upgrade -r requirements/development.txt
pip install --upgrade -r requirements/production.txt
pip install --upgrade -r requirements/test.txt

echo
echo "Checking for outdated dependencies ..."
pip-review
