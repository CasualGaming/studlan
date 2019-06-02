[![GitHub release](https://img.shields.io/github/release/CasualGaming/studlan.svg)](https://github.com/CasualGaming/studlan/releases)
[![Build Status](https://travis-ci.org/CasualGaming/studlan.svg?branch=master)](https://travis-ci.org/CasualGaming/studlan)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?branch=master&project=CasualGaming_studlan&metric=alert_status)](https://sonarcloud.io/dashboard?id=CasualGaming_studlan)

studlan
==========
LAN-party event management system.

* [Demo](https://studlan.casualgaming.dev)
* [Travis CI](https://travis-ci.org/CasualGaming/studlan)
* [Docker Hub](https://hub.docker.com/r/casualgaming/studlan)
* [SonarCloud](https://sonarcloud.io/dashboard?id=CasualGaming_studlan)

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

# Development Setup
## Tools
* [Git](https://git-scm.com) or [GitHub for Windows](https://windows.github.com/)
* Python 2.7 w/ pip and friends (see section below)
* Docker and Docker Compose (optional)
* Travis Tool (optional)

## Installing Virtualenv and Stuff
```
sudo pip install --upgrade pip virtualenv setuptools wheel
```

## Installing Travis Tool
Optional, used for encrypting Travis CI secrets and files and stuff.
```
sudo apt install ruby-dev rubygems
sudo gem install travis
```

## Configure Git
```
git config --global core.autocrlf false
git config --global user.name "<username>"
git config --global user.email <email-address>
```

Alternatively, on Windows, use the GitHub for Windows app to setup everything

# Running
## Run with Virtualenv
This approach is faster than running with Docker, plus it has colors. It will create dir `log`, dir `static`, file `studlan.db` and file `studlan/settings/local.py` inside the project directory, which are ignored in dockerignore and gitignore.
* Setup: `manage/setup-dev.sh` (first time or after project change)
* Run: `manage/run-dev.sh`

## Run with Docker
This approach takes more time to build, but is more similar to production. It places a settings file, the SQLite database file and the logs under `/tmp/studlan`.
* Build and run: `manage/run-docker-dev.sh`

If Docker starts to fill up your hard drive, run `docker system prune -a` to delete all local Docker stopped containers, unused networks, unused images and build cache.

## Testing and Validating
* Setup: `manage/setup-test.sh` (first time or after project change)
* Run basic tests: `manage/run-simple-test.sh`
* Run all tests and validations: `manage/run-full-test.sh`

## Miscellaneous
* Cleanup temporary files: `manage/clean.py`
* Enter venv: `manage/enter-venv.py`

## Upgrading dependencies
* This project uses pip-tools with all-dep pinning.
* Run `manage/update-deps.sh` to update dependencies.
* Go through all dep updates, read the changelogs and make sure they don't mess things up.

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
1. Run `travis encrypt --com -r <user>/<repo> <envvar>=<value>`.
1. Copy the output text to the `env.global` list in `.travis.yml` with a comment for the variable name.

Encrypt file:
Only one file can be encrypted. To encrypt multiple files, add them to an archive.
1. Run `travis encrypt-file --com -r <user>/<repo> <file>`.
1. Add the output command in `.travis.yml`.
1. Copy the encrypted file to the repo.
1. Optionally delete the unencrypted file.

## Deployment Site
* (Optional) Create a non-admin user which can login with pubkey alone (if deploying with CI/CD).
* Create a Django local settings file. Remember to add a randomly generated secret and disable debug mode.
* Create a Docker Compose file with appropriate volume bindings and network settings.
* Setup a database or use the built-in SQLite database or suggested PostgreSQL database.
* For PostgreSQL, use the sample `recreate-db.sh` script to setup or recreate the DB.
* Setup an Nginx reverse proxy to serve the site over TLS.
* Setup TLS certs with automatic renewal (Let's Encrypt).
* Setup a mail relay (Mailgun).
* Setup backup.
* Fix permissions to make sure unrelated users cannot read secret configs, and to prevent privilege escalation by replacing sudoable/setuided scripts.
* Run [Qualys' SSL Server Test](https://www.ssllabs.com/ssltest/) against the web server and fix any problems.
* Test both IPv4 and IPv6 reachability for the web server.
* To test Stripe, get your pair of testing (not live) keys from your Stripe account, and try to pay with a [testing card](https://stripe.com/docs/testing)

# Releasing
* Check for outdated dependencies (e.g. use the `manage/check-deps.sh` script).
* Double check that it actually works.
* Check that the changelog is updated, and add version and date to it.
* Create a [new release](https://github.com/CasualGaming/studlan/releases/new) based on the latest commit.
* (Check that CI/CD was triggered and that the production sites got updated and still work.)

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
