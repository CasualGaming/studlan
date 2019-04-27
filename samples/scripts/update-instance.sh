#!/bin/bash

# Configures and calls the update script for studlan.
# Must be called with the studlan dir as the PWD.

set -eu

SCRIPT="/srv/studlan-common/update.sh"

export LOCAL_DIR="/srv/studlan-dev"
export CONTAINER="studlan-dev-app"

$SCRIPT
