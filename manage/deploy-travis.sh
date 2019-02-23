#!/bin/bash

# Syntax: deploy-travis.sh [extra_tag]*

if [[ $TRAVIS_BRANCH != "true" ]]; then
    echo "Error: This isn't Travis!"
fi

set -e # Exit on error
set -u # Undefined var is error

IMAGE=$DOCKER_REPO
MAIN_TAG=$TRAVIS_COMMIT

echo "Logging into Docker Hub"
echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin

echo "Building and deploying with unique tag"
docker build -t "$IMAGE:$MAIN_TAG" .
docker push "$IMAGE:$MAIN_TAG"

for extra_tag in "$@"; do
    echo "Deploying with extra tag $extra_tag"
    docker tag "$IMAGE:$MAIN_TAG" "$IMAGE:$extra_tag"
    docker push "$IMAGE:$extra_tag"
done
