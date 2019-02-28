#!/usr/bin/env sh

set -e # Exit on error
set -u # Treat undefined variables as errors

# Constants
MANAGE="python manage.py"
STUDLAN_USER="studlan"
STUDLAN_GROUP="studlan"

# Optional env vars
STUDLAN_UID=${STUDLAN_UID:=}
STUDLAN_GID=${STUDLAN_GID:=}
SUPERUSER_USERNAME=${SUPERUSER_USERNAME:=}
SUPERUSER_EMAIL=${SUPERUSER_EMAIL:=}
SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD:=}
SUPERUSER_INACTIVE=${SUPERUSER_PASSWORD:=}

# Check if settings exist
APP_SETTINGS_FILE=studlan/settings/local.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "Django settings not found: $APP_SETTINGS_FILE" 1>&2
    exit -1
fi

# Run migration, but skip initial if matching table names already exist
echo "Migrating database ..."
$MANAGE migrate --fake-initial
echo

# Collect static files
$MANAGE collectstatic --noinput --clear

# Optionally add superuser
# Warning: These should be trusted to avoid code injection
if [[ ! -z $SUPERUSER_USERNAME ]]; then
    echo "Adding superuser ..."
    # FIXME disable superiser
    if [[ $SUPERUSER_INACTIVE == "true" ]]; then
        SUPERUSER_ACTIVE="False"
    else
        SUPERUSER_ACTIVE="True"
    fi
    $MANAGE shell << END
# Python 2
from django.contrib.auth import get_user_model;

superuser_usernane = "${SUPERUSER_USERNAME}"
superuser_email = "${SUPERUSER_EMAIL}"
superuser_password = "${SUPERUSER_PASSWORD}"
superuser_active = not ${SUPERUSER_ACTIVE}

if not superuser_usernane:
    print "Error: Username not specified"
    quit()

User = get_user_model();
if User.objects.filter(username=superuser_usernane).exists():
    print "User with specified username already exists. Not adding superuser."
elif not superuser_email or not superuser_password:
    print "User with specified username does not exist, but all credentials were not specified. Not adding superuser."
else:
    print "User with specified username does not exist and all credentials were provided. Adding superuser with is_active=%s." % superuser_active
    User.objects.create_superuser(username=superuser_usernane, email=superuser_email, password=superuser_password, is_active=superuser_active)

quit()
END
    echo
    echo "If a superuser was created, please change its password in the app"
fi

# Validate
echo "Checking validity ..."
$MANAGE check --deploy --fail-level=ERROR
echo

# Add group and user to run the app
if ! grep -q "^${STUDLAN_GROUP}:" /etc/group; then
    if [[ ! -z $STUDLAN_GID ]]; then
        groupadd -r -g "$STUDLAN_GID" $STUDLAN_GROUP
    else
        groupadd -r $STUDLAN_GROUP
    fi
fi
if ! grep -q "^${STUDLAN_USER}:" /etc/passwd; then
    if [[ ! -z $STUDLAN_UID ]]; then
        useradd -r -g studlan -u "$STUDLAN_UID" $STUDLAN_USER
    else
        useradd -r -g $STUDLAN_GROUP $STUDLAN_USER
    fi
    echo "Added user: $(id studlan)"
fi

# Setup permissions and stuff
# Note: Volumes from vboxsf cannot be chowned
set +e
echo "Chowning all files ..."
chown -R $STUDLAN_USER:$STUDLAN_GROUP .
set -e

# Run uWSGI server
echo "Done. Starting server ..."
exec uwsgi --ini uwsgi.ini
