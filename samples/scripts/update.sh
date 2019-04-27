#!/bin/bash

# Update script for studlan.
# Does not need to have the studlan dir as the PWD.
# Suggested cron line: */5 * * * * root /srv/studlan-dev/update.sh

# Version 1.0.0

LOCAL_DIR="$LOCAL_DIR"  # (Required) studlan dir.
CONTAINER="$CONTAINER"  # (Required) studlan app container name.

# Local env vars
LOG_FILE="update.log"
LOCK_DIR="update.lock"
BACKUP_SCRIPT="./backup.sh"
DEPLOY_SCRIPT="./deploy.sh"

# Validate env vars
[[ -z $LOCAL_DIR ]] && echo "Env var LOCAL_DIR not set" 1>&2 && exit -1
[[ -z $CONTAINER ]] && echo "Env var CONTAINER not set" 1>&2 && exit -1

set -eu

timestamp="$(date "+%Y-%m-%d %H:%M:%S")"

function log {
    echo "$timestamp $1" >> $LOG_FILE
}

cd $LOCAL_DIR

# Lock (mkdir uses atomic check-and-create)
if ! mkdir $LOCK_DIR 2>/dev/null; then
    log "Another update already running"
    exit -1
fi
trap "rm -rf $LOCK_DIR" EXIT

# Check if container is running
if ! docker inspect -f '{{.State.Running}}' $CONTAINER &> /dev/null; then
    log "Container not running"
    exit -1
fi

# Get image repo and tag
repo_plus_tag=$(docker inspect $CONTAINER | jq -r .[0].Config.Image)
if [[ -z $repo_plus_tag ]]; then
    log "Failed to get image repo and tag"
    exit -1
elif ! [[ $repo_plus_tag == *":"* ]]; then
    log "Failed to get image repo and tag, got this instead: $repo_plus_tag"
    exit -1
fi

# Get image ID from running container
current_id=$(docker inspect $CONTAINER | jq -r .[0].Image)
if [[ -z $current_id ]]; then
    log "Failed to get image ID from container"
    exit -1
fi

# Pull image
pull_output=$(docker pull $repo_plus_tag 2>&1)
if (( $? != 0 )); then
    log "Failed to pull image:"
    log "$pull_output"
    exit -1
fi

# Get newest image ID
new_id=$(docker images $repo_plus_tag --quiet --no-trunc)
if [[ -z $new_id ]]; then
    log "Failed to get new ID, image not found locally"
    exit -1
fi

# Compare IDs
if [[ $current_id == $new_id ]]; then
    exit 0
fi

log "New ID found"

log "Running backup script ..."
$BACKUP_SCRIPT > $LOG_FILE 2>&1
if (( $? != 0 )); then
    log "Backup script failed!"
    exit -1
fi

log "Running deploy script ..."
$DEPLOY_SCRIPT > $LOG_FILE 2>&1
if (( $? != 0 )); then
    log "Deploy script failed!"
    exit -1
fi

log "Success!"
