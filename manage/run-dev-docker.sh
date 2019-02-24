#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

IMAGE_ID="studlan:dev"
CONTAINER_ID="studlan-dev"
HOST_DIR=/tmp/studlan
VM_PWD="/srv/studlan"

# Add persistent files
[[ ! -e $HOST_DIR ]] && mkdir -p $HOST_DIR
[[ ! -e $HOST_DIR/studlan.db ]] && touch $HOST_DIR/studlan.db
[[ ! -e $HOST_DIR/log ]] && mkdir -p $HOST_DIR/log
[[ ! -e $HOST_DIR/settings.py ]] && cp sample-configs/local-dev.py $HOST_DIR/settings.py

# Build image
docker build -t "$IMAGE_ID" .

# Run temporary container from built image
docker run --rm \
    --name "$CONTAINER_ID" \
    -e STUDLAN_UID=950 -e STUDLAN_GID=950 \
    -v "$HOST_DIR/settings.py:$VM_PWD/studlan/settings/local.py:ro" \
    -v "$HOST_DIR/studlan.db:$VM_PWD/studlan.db:rw" \
    -v "$HOST_DIR/log:$VM_PWD/log:rw" \
    -p "8080:8080" \
    "$IMAGE_ID"
