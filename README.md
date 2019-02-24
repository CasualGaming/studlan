Studlan
==========
[![Build Status](https://drone.casualgaming.no/api/badges/CasualGaming/studlan/status.svg)](https://drone.fap.no/CasualGaming/studlan)

# Setup
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
* Setup a mail relay such as Mailgun.

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
