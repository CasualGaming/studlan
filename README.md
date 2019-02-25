Studlan
==========
(Outdated) [![Build Status](https://drone.casualgaming.no/api/badges/CasualGaming/studlan/status.svg)](https://drone.fap.no/CasualGaming/studlan)

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

### Installing Virtualenv
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
This approach is faster than running with Docker, plus it has colors. It will create dir `log`, dir `static`, file `studlan.db` and file `studlan/settings/local.py` inside the project directory, which are ignored in dockerignore and gitignore. Run `manage/clean.sh` to clean up after venv.
```
# First time only:
manage/setup-dev-venv.sh
manage/run-dev-venv.sh
```

## Run with Docker
This approach takes more time to build, but is more similar to production. It places a settings file, the SQLite database file and the logs under `/tmp/studlan`.
```
manage/run-dev-docker.sh
```

If Docker starts to fill up your hard drive, run `docker system prune -a` to delete all local Docker data.

# Testing
```
# First time only:
manage/setup-test-venv.sh
manage/run-test-venv.sh
```

# Deployment
## Docker Hub Registry
Make sure your personal or organizational user exists. Copy the username and password to Travis, so that it can log in.

## Travis CI
Connect your personal or organizational Travis CI user to your GitHub account. Add any required encorinment variables.

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
1. Log into the postgres user and automatically enter the DBMS tool: `su - postgres`
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
## Environment Variables
* `STUDLAN_UID=<UID>`: UID to use for the `studlan` user. Has effect only for the first start of the container.
* `STUDLAN_GID=<GID>`: Same as `STUDLAN_UID`, but for GID.
* `EXTRACT_STATIC=""`: If collected static files should be copied to the internal folder `/srv/studlan/static-out`. This folder can be mounted, so that extracted files can be served by the reverse proxy web server.

## Internal Directories and Files
* `/srv/studlan/studlan/settings/local.py`: (Required) Settings file for the Django app.
* `/srv/studlan/log`: Log directory for the uWSGI server hosting the Django app.
* `/srv/studlan/static-out`: If `EXTRACT_STATIC` is set, static files are copied to this folder when the container starts.
* `/srv/studlan/studlan.db`: Example location for SQLite database, if configured to use it. The actual path depends on what is configured in the `local.py` config.
