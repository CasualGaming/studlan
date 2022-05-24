#!/bin/bash

# Runs linter.

set -eu

# Activate venv
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate-venv.sh"
set -u

# Run flake8 static code analysis
# Uses settings from .flake8
flake8
