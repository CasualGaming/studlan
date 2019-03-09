#!/bin/bash

set -eu # Fail on error and undefines var is error

CONTAINER_ID="studlan-EXAMPLE-db"
DB_USER="studlan_EXAMPLE"
DB_NAME="studlan_EXAMPLE"

read -p "Enter gzipped database dump file to restore: " in_file
if [[ -z $in_file ]]; then
    echo "Error: No filename provided"
    exit -1
fi
if [[ ! -f $in_file ]]; then
    echo "Input file not found: $in_file" 1>&2
    exit -1
fi

echo
echo "Have you stopped any applications using the DB?"
read -p "Press ENTER to continue or Ctrl+C to cancel"

echo
echo "Have you cleared/recreated the database?"
read -p "Press ENTER to continue or Ctrl+C to cancel"

echo
echo "Is the database running?"
read -p "Press ENTER to continue or Ctrl+C to cancel"

zcat $in_file | docker exec -i $CONTAINER_ID psql --username=$DB_USER --dbname=$DB_NAME > /dev/null
