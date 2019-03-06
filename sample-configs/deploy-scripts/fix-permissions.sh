#!/bin/bash

# Use 0600 (rw) for most files and 0700 (rwx) for most folders

chown root:root db
chmod 0700 db

chown -R studlan:studlan deploy-log/
chmod 0700 deploy-log/

# doc has public static files and must be world readable
chown -R studlan:studlan doc/
chmod 0755 doc

chown -R studlan:studlan import_export/
chmod 0700 import_export/

chown -R studlan:studlan log/
chmod 0700 log/

chown root:root docker-compose.yml
chmod 0600 docker-compose.yml

chown studlan:studlan settings.py
chmod 0600 settings.py
