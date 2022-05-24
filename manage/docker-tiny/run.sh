#!/bin/bash

DC_FILE="setup/docker-compose.tiny.yml"
DC="docker-compose -f $DC_FILE"

$DC up
