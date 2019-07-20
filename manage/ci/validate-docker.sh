#!/bin/bash

DC="docker-compose -f setup/docker-compose.test.yml"

set -eu

if [[ $CI != "true" ]]; then
    echo "Error: This isn't a CI environment" 2>&1
    exit -1
fi

$DC build

# Don't exit if "up" fails
set +e
$DC up --exit-code-from=app
$DC down
