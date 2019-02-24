#!/usr/bin/env sh

set -e # Exit on error
set -u # Treat undefined variables as errors

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

# Add group and user
if [[ ! -z ${STUDLAN_GID:=} ]]; then
    groupadd -r -g "$STUDLAN_GID" studlan
else
    groupadd -r studlan
fi
if [[ ! -z ${STUDLAN_UID:=} ]]; then
    useradd -r -g studlan -u "$STUDLAN_UID" studlan
else
    useradd -r -g studlan studlan
fi
echo "Added user: $(id studlan)"
echo

# Setup permissions and stuff
# Note: Volumes from vboxsf cannot be chowned
set +e
chown -R studlan:studlan .
set -e

# Run Django server using uWSGI
exec uwsgi --ini uwsgi.ini
