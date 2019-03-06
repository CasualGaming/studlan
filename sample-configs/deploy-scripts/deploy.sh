#!/bin/bash

# This script is meant to be run as root and not directly from the CI/CD tool.
# It assumes the app stack is already set up with all required directories and config files.
# It may be run in a detached screen to make sure it isn't aborted by user disconnects and such.
# Suggested name: /srv/studlan-EXAMPLE/deploy.sh

# ID of service in DC file
LOCK_DIR="deploy.lock"

set -eu # Exit on error and error on undefined var

# mkdir uses atomic check-and-create
if mkdir $LOCK_DIR 2>/dev/null; then
    trap "rm -rf $LOCK_DIR" EXIT
    echo "Pulling images ..."
    docker-compose pull --quiet
    echo "Recreating containers ..."
    docker-compose up -d --force-recreate --quiet-pull --no-color

    echo "Fixing permissions ..."
    ./fix-permissions.sh
else
    echo "Warning: Another app deployment for this instance is already running, returning instead" 1>&2
fi
