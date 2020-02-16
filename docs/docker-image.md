# Docker Image

The Docker images are the intended way to run this application stack.

## Environment Variables

* `STUDLAN_UID=<uid>`: UID to use for the `studlan` user. Has effect only for the first start of the container.
* `STUDLAN_GID=<gid>`: Same as `STUDLAN_UID`, but for GID.
* `SUPERUSER_USERNAME=<username>`: If set, a superuser with the specified username is attempted created if a user with the specified username does not yet exist. `SUPERUSER_USERNAME`, `SUPERUSER_USERNAME` and `SUPERUSER_USERNAME` adds the superuser to the database, and can be removed after being set for one application start.
* `SUPERUSER_EMAIL=<email>`: Email address for the superuser to be created. Required if `SUPERUSER_USERNAME` is set and the user does not exist yet.
* `SUPERUSER_PASSWORD=<password>`: Password for the superuser to be created. Required if `SUPERUSER_USERNAME` is set and the user does not exist yet.
* `SUPERUSER_INACTIVE=[true]` (default: false): Deactivates the superuser if it was just created. (`User.is_active` is set to false.)
* `FLUSH_DATABASE=[true]`: Flushes the database. This happens before migration. Remember to disable afterwards.
* `IMPORT_DATABASE=[true]`: Attempts to load from `import_export/import.json.gz` (gzipped JSON). Should only be used with fresh or flushed databases. This happens after optionally flushing the database and migration, and before optionally adding a superuser and validating the settings. Remember to disable afterwards.
* `EXPORT_DATABASE=[true]`: Attempts to dump to `import_export/export.json.gz` (gzipped JSON). This could be used for backing up the database. This happens after optionally adding a superuser and validating the application. (This uses natural foreign keys, and excludes `contenttypes` and `auth.Permission`.)
* `NO_START=[true]`: If the uWSGI server should start or not at the end of the entrypoint script.

## Internal Directories and Files

* `/srv/studlan/studlan/settings/local.py`: (Required) Settings file for the Django app.
* `/srv/studlan/log`: Log directory for the uWSGI server hosting the Django app.
* `/srv/studlan/static`: Where static files are collected to on application start. Can be mounted to serve static files directly from reverse proxy.
* `/srv/studlan/db.sqlite`: Example location for SQLite database, if configured to use it. The actual path depends on what is configured in the `local.py` config.
* `/srv/studlan/import_export/`: Directory for `import.json.gz` and `export.json.gz` if `IMPORT_DATABASE=true` or `EXPORT_DATABASE=true`.
