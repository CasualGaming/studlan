#!/bin/bash

# Fixes permissions for studlan.
# Use 0600 (rw) for most files and 0700 (rwx) for most folders.
# Must be called with the studlan dir as the PWD.

# Base dir
chown root:root .
chmod 0700 .

# Main scripts
chown root:root *.sh
chmod 0700 *.sh

# Extra scripts
mkdir -p extra-scripts
chown root:root extra-scripts
chmod 0700 extra-scripts

# DB stuff, DB data dir inside
mkdir -p db
chown root:root db
chmod 0700 db

# Public web docs, accessable by nginx
mkdir -p doc
chown -R studlan:studlan doc
chmod 0755 doc

# Django import/export dir
mkdir -p import_export
chown -R studlan:studlan import_export
chmod 0700 import_export

# App logs
mkdir -p log
chown -R studlan:studlan log
chmod 0700 log

# DC file
chown root:root docker-compose.yml
chmod 0600 docker-compose.yml

# App/Django settings
chown studlan:studlan settings.py
chmod 0600 settings.py
