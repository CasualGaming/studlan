#!/bin/bash

LOCAL_DIR=".local/venv"
CONFIG_FILE="studlan/settings/local.py"
CONFIG_TEMPLATE_FILE="setup/local.venv.dev.py"
MANAGE="manage/manage.sh"

set -eu

# Activate venv
set +u
source "$(dirname "$BASH_SOURCE[0]")/activate-venv.sh"
set -u

echo "Installing requirements ..."
python -m pip install -r requirements/development.txt

# Add config file and exit if missing
if [[ ! -e $CONFIG_FILE ]]; then
    echo
    echo "Creating new config file ($CONFIG_FILE) ..."
    cp $CONFIG_TEMPLATE_FILE $CONFIG_FILE
fi

# Add version file
echo "0.0.0-SNAPSHOT" > VERSION

echo
echo "Running migration ..."
$MANAGE migrate --fake-initial

echo
echo "Compiling translations ..."
$MANAGE compilemessages --locale=nb

echo
echo "Adding superuser ..."
    $MANAGE shell << END
# Python 2
from django.contrib.auth import get_user_model;

superuser_username = "batman"
superuser_email = "batman@localhost"
superuser_password = "manbat"
superuser_active = "True"

User = get_user_model();
if not User.objects.filter(username=superuser_username).exists():
    User.objects.create_superuser(username=superuser_username, email=superuser_email, password=superuser_password, is_active=superuser_active)
else:
    print "Superuser already exists."

quit()
END
