#!/bin/bash

# Backup script for studlan files and DB.
# The database is backed up only if running.
# Does not need to have the studlan dir as the PWD.

# Version 1.0.0

# Env vars
ARCHIVE_PREFIX="$ARCHIVE_PREFIX"        # (Required) Prefix for archive filename.
IN_LOCAL_DIR="$IN_LOCAL_DIR"            # (Required) studlan dir. The files are hardcoded in this script.
IN_EXTRA_FILES="$IN_EXTRA_FILES"        # (Optional) Space-separated list of extra files or dirs to include.
DB_CONTAINER_ID="$DB_CONTAINER_ID"      # (Optional) Docker container ID for database.
DB_USER="$DB_USER"                      # (Required if DB_CONTAINER_ID) Database user.
DB_NAME="$DB_NAME"                      # (Required if DB_CONTAINER_ID) Database name.
OUT_LOCAL_DIR="$OUT_LOCAL_DIR"          # (Required) Local archive directory for the backup file. The dir will have its permissions set to 0700.
MAX_LOCAL_BACKUPS="$MAX_LOCAL_BACKUPS"  # (Optional) Maximum of local backups to keep for the specified prefix.
OUT_S3_BUCKET="$OUT_S3_BUCKET"          # (Optional) AWS S3 bucket to copy the backup to, without "s3://" prefix.
OUT_S3_DIR="$OUT_S3_DIR"                # (Required if OUT_S3_BUCKET) Directory inside AWS S3 bucket.
AWS_PROFILE="$AWS_PROFILE"              # (Required if OUT_S3_BUCKET) AWS profile with credentials.
AWS_REGION="$AWS_REGION"                # (Required if OUT_S3_BUCKET) AWS S3 bucket region.

# Validate env vars
[[ -z $ARCHIVE_PREFIX ]] && echo "Env var ARCHIVE_PREFIX not set" 1>&2 && exit -1
[[ -z $IN_LOCAL_DIR ]] && echo "Env var IN_LOCAL_DIR not set" 1>&2 && exit -1
[[ -z $OUT_LOCAL_DIR ]] && echo "Env var OUT_LOCAL_DIR not set" 1>&2 && exit -1
if ! [[ -z $DB_CONTAINER_ID ]]; then
  [[ -z $DB_USER ]] && echo "Env var DB_CONTAINER_ID set but DB_USER not set" 1>&2 && exit -1
  [[ -z $DB_NAME ]] && echo "Env var DB_CONTAINER_ID set but DB_NAME not set" 1>&2 && exit -1
fi
if ! [[ -z $OUT_S3_BUCKET ]]; then
  [[ -z $OUT_S3_DIR ]] && echo "Env var OUT_S3_BUCKET set but OUT_S3_DIR not set" 1>&2 && exit -1
  [[ -z $AWS_PROFILE ]] && echo "Env var OUT_S3_BUCKET set but AWS_PROFILE not set" 1>&2 && exit -1
  [[ -z $AWS_REGION ]] && echo "Env var OUT_S3_BUCKET set but AWS_REGION not set" 1>&2 && exit -1
fi

set -eu # Fail on error and undefines var is error

timestamp="$(date +'%Y-%m-%d_%H-%M-%S')"
archive_file="$(basename ${ARCHIVE_PREFIX}-${timestamp}.tar.bz)"
encrypted_archive_file="${archive_file}.enc"

# Setup tmp dir
tmp_dir_parent="$(mktemp -d /tmp/backup-XXXXXXXX)"
trap "rm -rf $tmp_dir_parent" EXIT
chown root:root $tmp_dir_parent
chmod 0700 $tmp_dir_parent
tmp_dir_base="${ARCHIVE_PREFIX}"
tmp_dir="${tmp_dir_parent}/${tmp_dir_base}"
mkdir $tmp_dir

# Copy select files
cd $IN_LOCAL_DIR
mkdir $tmp_dir/doc
cp -r doc/.well-known $tmp_dir/doc/
cp -r doc/media $tmp_dir/doc/
mkdir $tmp_dir/main-scripts
cp *.sh $tmp_dir/main-scripts
cp -r extra-scripts $tmp_dir/extra-scripts
cp settings.py $tmp_dir/
cp docker-compose.yml $tmp_dir/
# DB dump not added yet
mkdir -p $tmp_dir/db

# Copy extra files
mkdir $tmp_dir/extra-files
for x in $IN_EXTRA_FILES; do
  cp -r $x $tmp_dir/extra-files/
done

# Backup DB if running
if [[ -z $DB_CONTAINER_ID ]]; then
  echo "Warning: Database details not provided, not backing up database" 1>&2
elif [[ ! $(docker ps -a | grep $DB_CONTAINER_ID) ]]; then
  echo "Warning: Database not running, not backing up database" 1>&2
else
  docker exec -t $DB_CONTAINER_ID pg_dump --username=$DB_USER --dbname=$DB_NAME > $tmp_dir/db/db.dump \
    || (echo "Failed to dump database, Docker exec returned non-zero value" 1>&2 && exit -1)
fi

# Archive and encrypt files
cd $tmp_dir_parent
tar cjf $archive_file $tmp_dir_base
chmod 600 $archive_file

# Copy to local archive dir
mkdir -p $OUT_LOCAL_DIR
chmod 0700 $OUT_LOCAL_DIR
cp $archive_file $OUT_LOCAL_DIR/

# Copy to AWS S3 bucket
if [[ ! -z $OUT_S3_BUCKET ]]; then
  aws s3 --profile=$AWS_PROFILE --region=$AWS_REGION --only-show-errors cp $archive_file s3://${OUT_S3_BUCKET}/${OUT_S3_DIR}/
else
  echo "Warning: AWS S3 bucket not specified, not backing up remotely" 1>&2
fi

# Delete expired local backups
if [[ -z $MAX_LOCAL_BACKUPS ]]; then
  echo "Warning: Local expiry time not set, not purging expired local backups" 1>&2
elif [[ ! $MAX_LOCAL_BACKUPS =~ ^[0-9-]+$ ]] || (( $MAX_LOCAL_BACKUPS <= 0 )); then
  echo "Error: MAX_LOCAL_BACKUPS is not a positive integer" 1>&2
else
  find $OUT_LOCAL_DIR -mindepth 1 | sort -r | tail -n +$(($MAX_LOCAL_BACKUPS + 1)) | xargs rm -f
fi
