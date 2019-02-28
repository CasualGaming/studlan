#!/bin/bash
# Syntax: deploy-travis.sh <main_tag> [extra_tag]*
# Environment variables: DOCKER_REPO, DOCKER_USERNAME, DOCKER_PASSWORD

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

if (( $# < 1 )); then
    echo "Error: Missing main tag" 2>&1
    exit -1
fi

set -e # Exit on error
set -u # Undefined var is error

IMAGE=$DOCKER_REPO
MAIN_TAG="$1"
EXTRA_TAGS="${@:2}"

echo "Logging into Docker Hub"
echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin

echo "Building and deploying with tag"
docker build -t "$IMAGE:$MAIN_TAG" .
docker push "$IMAGE:$MAIN_TAG"

for extra_tag in "$EXTRA_TAGS"; do
    echo "Deploying with tag $extra_tag"
    docker tag "$IMAGE:$MAIN_TAG" "$IMAGE:$extra_tag"
    docker push "$IMAGE:$extra_tag"
done
