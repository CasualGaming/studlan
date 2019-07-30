#!/bin/bash

# Configures and calls the backup script for studlan.
# Does not require the studlan dir as the PWD.
# Call this from a cron job for periodic backups.
# Also call this before drastic changes.

set -eu

SCRIPT="/srv/studlan-common/backup.sh"

export ARCHIVE_PREFIX="studlan-dev"
export IN_LOCAL_DIR="/srv/studlan-dev"
export IN_EXTRA_FILES="/srv/studlan-common/backup.sh"
export DB_CONTAINER_ID="studlan-dev-db"
export DB_USER="studlan_dev"
export DB_NAME="studlan_dev"
export OUT_LOCAL_DIR="/backup/studlan/dev"
export MAX_LOCAL_BACKUPS="10"
export OUT_S3_BUCKET="abc-studlan-backup"
export OUT_S3_DIR="dev"
export AWS_PROFILE="studlan-backup"
export AWS_REGION="eu-west-2"

$SCRIPT
