#!/usr/bin/env sh

set -e # Exit on error
set -u # Treat undefined variables as errors

STUDLAN_USER=studlan
STUDLAN_GROUP=studlan
STATIC_OUT_DIR=/srv/studlan/static-out

# Check if settings exist
APP_SETTINGS_FILE=studlan/settings/local.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "App settings not found: $APP_SETTINGS_FILE" 1>&2
    exit 1
fi

# Run migration, but skip initial if matching table names already exist
python manage.py migrate --fake-initial
echo

# Validate
python manage.py check --deploy --fail-level=ERROR
echo

# Add group and user to run the app
if ! grep -q "^${STUDLAN_GROUP}:" /etc/group; then
    STUDLAN_GID=${STUDLAN_GID:=}
    if [[ ! -z $STUDLAN_GID ]]; then
        groupadd -r -g "$STUDLAN_GID" $STUDLAN_GROUP
    else
        groupadd -r $STUDLAN_GROUP
    fi
fi
if ! grep -q "^${STUDLAN_USER}:" /etc/passwd; then
    STUDLAN_UID=${STUDLAN_UID:=}
    if [[ ! -z $STUDLAN_UID ]]; then
        useradd -r -g studlan -u "$STUDLAN_UID" $STUDLAN_USER
    else
        useradd -r -g $STUDLAN_GROUP $STUDLAN_USER
    fi
    echo "Added user: $(id studlan)"
fi

# Optionally copy static files to mountable dir
if [[ -v EXTRACT_STATIC ]]; then
    echo "Copying static files to $STATIC_OUT_DIR"
    if [[ ! -d $STATIC_OUT_DIR ]]; then
        mkdir -p $STATIC_OUT_DIR
    fi
    find $STATIC_OUT_DIR -mindepth 1 -delete
    cp -r static/. $STATIC_OUT_DIR
fi

# Setup permissions and stuff
# Note: Volumes from vboxsf cannot be chowned
set +e
chown -R $STUDLAN_USER:$STUDLAN_GROUP .
set -e

# Run uWSGI server
exec uwsgi --ini uwsgi.ini
