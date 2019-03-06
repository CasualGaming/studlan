#!/bin/bash

set -eu # Fail on error and undefines var is error

CONTAINER_ID="studlan-EXAMPLE-db"
DB_USER="studlan_EXAMPLE"
DB_NAME="studlan_EXAMPLE"
OUT_DIR="db/dump"

timestamp="$(date +'%Y-%m-%d_%H-%M-%S')"
out_file="${OUT_DIR}/${DB_NAME}_${timestamp}.gz"

mkdir -p $OUT_DIR
chown root:root $OUT_DIR
chmod 0700 $OUT_DIR

docker exec -t $CONTAINER_ID pg_dump --username=$DB_USER --dbname=$DB_NAME | gzip > $out_file
