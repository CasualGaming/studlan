#!/bin/bash

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

set -eu # Exit on error and undefined var is error

[[ ! -e log ]] && mkdir -p log

# Run flake8 static code analysis
# Uses settings from .flake8
flake8
