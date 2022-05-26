#!/usr/bin/env sh

set -e # Exit on error
set -u # Treat undefined variables as errors
set -o pipefail # Don't ignore fails in pipe

# Constants
STUDLAN_USER="studlan"
STUDLAN_GROUP="studlan"
MANAGE="python manage.py"
MANAGE_AS_USER="runuser -u $STUDLAN_USER -g $STUDLAN_GROUP -- $MANAGE"
IMPORT_EXPORT_DIR="import_export"
IMPORT_FILE="$IMPORT_EXPORT_DIR/import.json.gz"
EXPORT_FILE="$IMPORT_EXPORT_DIR/export.json.gz"

# Optional env vars
STUDLAN_UID=${STUDLAN_UID:-}
STUDLAN_GID=${STUDLAN_GID:-}
SUPERUSER_USERNAME=${SUPERUSER_USERNAME:-}
SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-}
SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD:-}
SUPERUSER_INACTIVE=${SUPERUSER_INACTIVE:-}
FLUSH_DATABASE=${FLUSH_DATABASE:-}
IMPORT_DATABASE=${IMPORT_DATABASE:-}
EXPORT_DATABASE=${EXPORT_DATABASE:-}
NO_CHOWN=${NO_CHOWN:-}
NO_START=${NO_START:-}
DJANGO_DEV_SERVER=${DJANGO_DEV_SERVER:-}

echo "Starting studlan v$(cat VERSION)"
echo

# Check if settings exist
APP_SETTINGS_FILE=studlan/settings/local.py
if [[ ! -e $APP_SETTINGS_FILE ]]; then
    echo "Django settings not found: $APP_SETTINGS_FILE" 1>&2
    exit -1
fi

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

# Setup log dir and files
mkdir -p log
chown -R $STUDLAN_USER:$STUDLAN_GROUP log

# Collect static files (as root)
echo "Collecting static files ..."
mkdir static
chown -R $STUDLAN_USER:$STUDLAN_GROUP static
$MANAGE_AS_USER collectstatic --noinput --clear
chown -R root:root static
echo

# Optionally flush database
if [[ $FLUSH_DATABASE == "true" ]]; then
    echo "Flushing the database ..."
    $MANAGE_AS_USER flush --noinput
fi

# Run migration, but skip initial if matching table names already exist
echo "Migrating database ..."
$MANAGE_AS_USER migrate --fake-initial
echo

# Optionally import database
if [[ $IMPORT_DATABASE == "true" ]]; then
    echo "Importing from $IMPORT_FILE ..."
    if [[ -f $IMPORT_FILE ]]; then
        $MANAGE_AS_USER loaddata $IMPORT_FILE
    else
        echo "Error: Import file not found: $IMPORT_FILE" 1>&2
    fi
fi

# Clear expired sessions
$MANAGE_AS_USER clearsessions

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
    $MANAGE_AS_USER shell << END
# Python 2
from django.contrib.auth import get_user_model;

superuser_usernane = "${SUPERUSER_USERNAME}"
superuser_email = "${SUPERUSER_EMAIL}"
superuser_password = "${SUPERUSER_PASSWORD}"
superuser_active = ${SUPERUSER_ACTIVE}

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
$MANAGE_AS_USER check --deploy --fail-level=ERROR
echo

# Optionally export database
if [[ $EXPORT_DATABASE == "true" ]]; then
    echo "Exporting to $EXPORT_FILE ..."
    mkdir -p $IMPORT_EXPORT_DIR
    touch $EXPORT_FILE
    chmod 600 $EXPORT_FILE
    # Exclude contenttypes and auth.Permission while using natural foreign keys to prevent IntegrityError on import
    $MANAGE_AS_USER dumpdata --natural-foreign --exclude=contenttypes --exclude=auth.Permission --format=json --indent=2 | gzip > $EXPORT_FILE
fi

# Setup cron jobs
echo "0 0 * * * studlan cd '$PWD' && /usr/local/bin/python ./manage.py clearsessions >> log/cron-clearsessions.log 2>&1" > /etc/cron.d/studlan-clearsessions
echo "* * * * * studlan cd '$PWD' && /usr/local/bin/python ./manage.py sendmail >> log/cron-sendmail.log 2>&1" > /etc/cron.d/studlan-sendmail
echo

# Maybe don't start
if [[ $NO_START == "true" ]]; then
    echo "No-start enabled, stopping instead"
    exit 0
fi

echo "Starting cron daemon ..."
/etc/init.d/cron start

# Run prod or dev server
if [[ $DJANGO_DEV_SERVER != "true" ]]; then
    echo "Starting uWSGI server ..."
    exec uwsgi --ini uwsgi.ini
else
    echo "Starting Django dev server ..."
    echo "WARNING: Never use this in prod!"
    $MANAGE_AS_USER runserver 0.0.0.0:8080
fi
