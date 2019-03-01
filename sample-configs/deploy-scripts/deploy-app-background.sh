#!/bin/bash

# This script is meant to be run as root and not directly from the CI/CD tool.
# It starts the deployment script in a disconnected screen with a log file.
# Suggested name: /srv/studlan/deploy-background-app-EXAMPLE.sh

set -eu # Exit on error and error on undefined var

INSTANCE_NAME="app-EXAMPLE"
NEW_PWD=/srv/studlan
LOG_DIR="deploy-log"
LOG_FILE_PREFIX="${LOG_DIR}/${INSTANCE_NAME}_"
LOG_FILE_SUFFIX=".txt"
DEPLOY_CMD="./deploy-foreground-${INSTANCE_NAME}.sh"

timestamp="$(date +'%Y-%m-%d_%H-%M-%S')"
log_file="${LOG_FILE_PREFIX}${timestamp}${LOG_FILE_SUFFIX}"

cd $NEW_PWD
mkdir -p $LOG_DIR

# Ignore exit signals, run in background, and log output to file
nohup $DEPLOY_CMD > $log_file 2>&1 &

echo "Returning immediately while deployment is running in the background"
