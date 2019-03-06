#!/bin/bash

set -eu # Fail on error and undefines var is error

CONTAINER_ID="studlan-EXAMPLE-db"
DB_SUPERUSER="postgres"
DB_USER="studlan_EXAMPLE"
DB_NAME="studlan_EXAMPLE"

read -p "Enter DB password for app user: " db_password
if [[ -z $db_password ]]; then
    echo "Error: No password provided"
    exit -1
fi

echo
echo "Have you stopped any applications using the DB?"
read -p "Press ENTER to continue or Ctrl+C to cancel"

echo
echo "Is the database running?"
read -p "Press ENTER to continue or Ctrl+C to cancel"

docker exec -i $CONTAINER_ID psql --username=$DB_SUPERUSER > /dev/null << END
DROP DATABASE IF EXISTS $DB_NAME;
DROP USER IF EXISTS $DB_USER;
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$db_password';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'Europe/Oslo';
GRANT ALL PRIVILEGES ON DATABASE $DB_USER TO $DB_NAME;
END
