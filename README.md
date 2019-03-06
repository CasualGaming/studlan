Studlan
==========
[![Build Status](https://travis-ci.org/CasualGaming/studlan.svg?branch=master)](https://travis-ci.org/CasualGaming/studlan)

* [Travis CI](https://travis-ci.org/CasualGaming/studlan)
* [Docker Hub](https://hub.docker.com/r/casualgaming/studlan)

# Features
* News
* Activites
	* Used for having several competitions under the same activity (usually a game).
* Competitions
	* Single User or Team participation
	* Lotteries with automated drawing
* Teams
	* Team Leader
		* Can invite members
		* Can sign the team up for competitions or leave them.
	* Members
		* Can decline or accept invitations and leave teams
* Tickets and seating
	* Online payment supported through Stripe
	* Participants with pre purchased tickets can reserve seats
		* Seating arrangements are fully customizable through SVG layouts.
	* Export details of participants per event

## Planned features
* Teams
	* Match history
	* Seeding (for any activity)
* Competitions
	* Challonge integration with Automatic bracket creation/Tournament system that takes seeding into account.
* Non-fluid responsive layout

# Development Setup
## Tools
* [Git](http://git-scm.com) (the [GitHub for Windows](http://windows.github.com/) app is probably the easiest way to install and use Git on Windows)
* Python 2.7 w/ pip
* Virtualenv (from pip)
* Docker and Docker Compose (optional)
* Travis Tool (optional)

### Installing Virtualenv and Stuff
```
sudo pip install --upgrade pip virtualenv setuptools wheel
```

### Installing Travis Tool
```
sudo apt install ruby-dev rubygems
sudo gem install travis
```

## Configure Git
```bash
git config --global core.autocrlf false
git config --global user.name "<username>"
git config --global user.email <email-address>
```

Alternatively, on Windows, use the GitHub for Windows app to setup everything

## Clone the Repo
The following sections assume you are inside the cloned repo.

# Running
## Run with Virtualenv
This approach is faster than running with Docker, plus it has colors. It will create dir `log`, dir `static`, file `studlan.db` and file `studlan/settings/local.py` inside the project directory, which are ignored in dockerignore and gitignore.
* Setup: `manage/setup-dev.sh` (first time or after project change)
* Run: `manage/run-dev.sh`

## Run with Docker
This approach takes more time to build, but is more similar to production. It places a settings file, the SQLite database file and the logs under `/tmp/studlan`.
* Build and run: `manage/run-docker-dev.sh`

If Docker starts to fill up your hard drive, run `docker system prune -a` to delete all local Docker data.

# Testing and Validating
* Setup: `manage/setup-test.sh` (first time or after project change)
* Run basic tests: `manage/run-simple-test.sh`
* Run all tests and validations: `manage/run-full-test.sh`

# Misc
## Cleanup
* Cleanup after venv, Docker, etc.: `manage/clean.py`
* Enter venv: `manage/enter-venv.py`

# Deployment
## Docker Hub Registry
Make sure your personal or organizational user exists. Copy the username and password to Travis, so that it can log in.

## Travis CI
Connect your personal or organizational Travis CI user to your GitHub account. Add any required encorinment variables. Setup periodic builds using Cron jobs in case dependencies or parent images are updated.

### Encrypting Files and Values for Travis CI
The recommended way secure sensitive data.

Login and logout with `travis login --com` and `travis logout`.

Encrypt environment variable values:
The value can be an arbitrary string, but is commonly an environment variable value pair.
1. Run `travis encrypt --com -r <user>/<repo> <envvar>=<value>`
1. Copy the output text to the `env.global` list in `.travis.yml` with a comment for the variable name

Encrypt file:
Only one file can be encrypted. To encrypt multiple files, add them to an archive.
1. Run `travis encrypt-file --com -r <user>/<repo> <file>`
1. Add the output command in `.travis.yml`
1. Copy the encrypted file to the repo
1. Optionally delete the unencrypted file

## Remote Site
* Create a non-admin user which can login with pubkey alone.
* Create a Django local settings file. Remember to add a randomly generated secret.
* Create a Docker Compose file with appropriate volume bindings and network settings.
* Setup a database or use the built-in SQLite database.
* Setup an Nginx reverse proxy to serve the site over TLS.
* Setup TLS cert with automatic renewal.
* Setup a mail relay such as Mailgun.
* Setup backup.
* Fix permissions to make sure unrelated users cannot read secret configs, and to prevent privilege escalation by replacing sudoable/setuided scripts.
* Run [Qualys' SSL Server Test](https://www.ssllabs.com/ssltest/) against the web server and fix any problems.
* Test both IPv4 and IPv6 reachability for the web server.

### PostgreSQL Initial Setup
Run this procedure for every instance of the app, with unique IDs and an actual password.
1. Enter the postgres container from the host: `docker exec -it studlan-db bash`
1. Log into the postgres user and automatically enter the DBMS tool: `su - postgres -c psql postgres`
1. `CREATE DATABASE studlan_example;`
1. `CREATE USER studlan_example WITH PASSWORD 'example_password';` (quotes required)
1. `ALTER ROLE studlan_example SET client_encoding TO 'utf8';`
1. `ALTER ROLE studlan_example SET default_transaction_isolation TO 'read committed';`
1. `ALTER ROLE studlan_example SET timezone TO 'Europe/Oslo';`
1. `GRANT ALL PRIVILEGES ON DATABASE studlan_example TO studlan_example;`
1. Exit the DBMS tool: `\q`
1. Disconnect from the container.
1. Update the Django settings.

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
* `/srv/studlan/studlan.db`: Example location for SQLite database, if configured to use it. The actual path depends on what is configured in the `local.py` config.
* `/srv/studlan/import_export/`: Directory for `import.json.gz` and `export.json.gz` if `IMPORT_DATABASE=true` or `EXPORT_DATABASE=true`.
