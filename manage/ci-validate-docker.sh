#!/bin/bash

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

set -eu # Exit on error and undefined var is error

IMAGE_ID="studlan:dev"

docker build -t "$IMAGE_ID" .

# Enable all the things to see if anything breaks
docker run --rm \
    -e STUDLAN_UID=950 -e STUDLAN_GID=950 \
    -e SUPERUSER_USERNAME="superman" -e SUPERUSER_EMAIL="superman@example.net" -e SUPERUSER_PASSWORD="loislane" -e SUPERUSER_INACTIVE=false \
    -e FLUSH_DATABASE=true -e IMPORT_DATABASE=true -e EXPORT_DATABASE=true \
    -e NO_START=true \
    -v "$PWD/samples/local-empty.py:/srv/studlan/studlan/settings/local.py:ro" \
    -p "8080:8080" \
    "$IMAGE_ID"
