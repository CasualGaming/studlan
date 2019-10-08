#!/bin/bash

MANAGE="manage/manage.sh"

set -eu

echo "Running some checks. This will stop on the first error, or print \"success\" if no errors were caught."

echo
echo "Running linter ..."
manage/lint.sh

echo
echo "Checking migrations ..."
$MANAGE makemigrations --check --no-input --dry-run
$MANAGE migrate --fake-initial --no-input --fake

echo
echo "Compiling translations ..."
$MANAGE compilemessages --locale=nb

echo
echo "Checking validity ..."
$MANAGE check --deploy --fail-level=ERROR

echo
echo "Running tests ..."
manage/test.sh

echo
echo "Collecting static files ..."
# Ignore admin app, use theme instead
$MANAGE collectstatic -i admin --no-input --clear | egrep -v "^Deleting" || true

echo
echo "Success!"
