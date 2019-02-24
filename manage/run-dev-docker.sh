#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

IMAGE_ID="studlan:dev"
CONTAINER_ID="studlan-dev"
HOST_PWD=$(pwd)
VM_PWD="/srv/studlan"

# Add persistent files
[[ ! -e tmp ]] && mkdir -p tmp
[[ ! -e tmp/studlan.db ]] && touch tmp/studlan.db
[[ ! -e log ]] && mkdir -p log
[[ ! -e tmp/settings.py ]] && cp sample-configs/local-dev.py tmp/settings.py

# Build image
docker build -t "$IMAGE_ID" .

# Run temporary container from built image
echo "Starting web server with log file"
docker run --rm \
    --name "$CONTAINER_ID" \
    -v "$HOST_PWD/tmp/settings.py:$VM_PWD/studlan/settings/local.py:ro" \
    -v "$HOST_PWD/tmp/studlan.db:$VM_PWD/tmp/studlan.db:rw" \
    -v "$HOST_PWD/log:$VM_PWD/log:rw" \
    -p "8080:8080" \
    "$IMAGE_ID"
