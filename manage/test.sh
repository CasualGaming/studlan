#!/bin/bash

# Run Django tests.

MANAGE="manage/manage.sh"

set -eu

# Run all Django tests
$MANAGE test --no-input
