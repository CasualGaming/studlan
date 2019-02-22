Studlan
==========
[![Build Status](https://drone.casualgaming.no/api/badges/CasualGaming/studlan/status.svg)](https://drone.fap.no/CasualGaming/studlan)

# Setup
## Tools
* [Git](http://git-scm.com) (the [GitHub for Windows](http://windows.github.com/) app is probably the easiest way to install and use Git on Windows)
* SSH (On Windows, SSH is included with Git/GitHub for Windows)
* Python 2.7 w/ pip
* Docker and Docker Compose

## Git
```bash
git config --global core.autocrlf false
git config --global user.name "<username>"
git config --global user.email <email-address>
```

Alternatively on Windows, use the GitHub for Windows app to setup everything

## Clone the Repo
No instructions should be needed here. The following sections assume you are inside the repo.

## Python virtualenv
```
manage/setup-dev-venv.sh
```

## Django
```
# Setup DB and migrate to newest version
python manage.py migrate --fake-initial
```

## Making New Migrations
**TODO**
Enter venv first.

Dry run:
```
python manage.py makemigrations --dry-run
```

# Running
## Run with Virtualenv
This approach is faster than running with docker.
```
manage/run-dev-venv.sh
```

### Entering Virtualenv
Manually:
```
source venv/bin/activate
# Do stuff
deactivate
```
Using subshell:
```
manage/enter-venv.sh
```

## Run with Docker
This approach takes more time to build, but is more similar to production. Persistent files such as the SQLite DB, the Django local settings and log file are stores in the `tmp` dir.
```
manage/run-dev-docker.sh
```

# Testing
## Validate Config and Database
```
python manage.py check --deploy
```
## Run Unit Tests
**TODO**
```
tox test
```

# Deployment
## Setup
**TODO**
* Create a (`studlan/settings/local.py`) settings file for every instance of the app
* Create a Docker Compose file for all instances of the app, including bindings for the settings files

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
