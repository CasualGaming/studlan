#!/bin/bash

set -e # Exit on error
set -u # Undefined var is error

IMAGE_ID="studlan:dev"
CONTAINER_ID="studlan-dev"
HOST_PWD=$(pwd)
VM_PWD="/srv/studlan"

# Add persistent files
mkdir -p tmp
touch tmp/studlan.db
mkdir -p tmp/log
cp studlan/settings/local.py tmp/settings.py

# Build image
docker build -t "$IMAGE_ID" .

# Run temporary container from built image
docker run --rm \
    --name "$CONTAINER_ID" \
    -v "$HOST_PWD/tmp/settings.py:$VM_PWD/studlan/settings/local.py:ro" \
    -v "$HOST_PWD/tmp/studlan.db:$VM_PWD/tmp/studlan.db:rw" \
    -v "$HOST_PWD/tmp/log:$VM_PWD/tmp/log:rw" \
    -p "8080:8080" \
    "$IMAGE_ID"
