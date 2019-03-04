#!/bin/bash

# This script simply creates/recreated all the containers.
# If running for the first time, make sure you setup the directories and config files first.

docker-compose pull
docker-compose up -d --force-recreate
