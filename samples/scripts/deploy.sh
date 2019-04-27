#!/bin/bash

# Deployment script for studlan.
# Must be called with the studlan dir as the PWD.

LOCK_DIR="deploy.lock"

PATH="$PATH:/usr/local/bin"

set -eu # Exit on error and error on undefined var

# mkdir uses atomic check-and-create
if ! mkdir $LOCK_DIR 2>/dev/null; then
  echo "Warning: Another app deployment for this instance is already running, returning instead" 1>&2
  exit -1
fi

trap "rm -rf $LOCK_DIR" EXIT

echo "Pulling images ..."
docker-compose pull --quiet

echo "Recreating containers ..."
docker-compose up -d --force-recreate --quiet-pull --no-color

echo "Fixing permissions ..."
./fix-permissions.sh
