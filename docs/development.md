# Development

## Setup

### Tools

* [Git](https://git-scm.com) or [GitHub for Windows](https://windows.github.com/)
* Python 2 w/ pip and friends (see section below)
* Docker and Docker Compose (optional)
* Travis Tool (optional)

### Installing Python 2 Virtualenv

Download and install Python 2 and Python 2 pip.
Be careful with `python` and `pip` since either version (2 or 3) may use the name without version and it's not consistent across OSes.

- Linux: ´sudo python -m pip install --upgrade pip virtualenv setuptools wheel´
- Windows: ´py -2 -m pip install --upgrade pip virtualenv setuptools wheel´

#### On Newer Systems without Python 2 Support

Python 2 w/ pip is no longer available on e.g. Arch Linux. To get around that, just do stuff inside an interactive Docker container instead.

```sh
# Debian 10 still has support
docker run --rm -it -v $PWD:/project debian:10

# Now inside the container
apt update
apt install python python2 gettext

# Project stuff
manage/setup.sh
```

### Configuring Git

If using CLI (not some GUI app):
```
git config --global core.autocrlf false
git config --global user.name <username>
git config --global user.email <email-address>
```

### (Optional) Installing and Configuring Docker

Install both Docker and Docker Compose (combined app on Windows).
On Linux, add yourself to the `docker` group and then log out and in.
This allows you to run Docker commands as non-root (don't do this on servers).

### (Optional) Installing Travis Tool

Optional, used for encrypting Travis CI secrets and files and stuff.
```
sudo apt install ruby-dev rubygems
sudo gem install travis
```

Alternatively, on Windows, use the GitHub for Windows app to setup everything

## Running

This method uses Virtualenv and does not require Docker. Run `manage/setup.sh` (to setup the virtual environment, add the temporary settings file, migrate the Django DB, add an admin user, etc.). The username and password of the added admin user is "batman" and "manbat". The DB file and log files are located in `.local/venv/`. The local settings file is located at `studlan/settings/local.py`.

## Tools

Most of these use venv and therefore require `manage/setup.sh` to be run first (once).

* Cleanup some unimportant local files (Python caches, logs, ...): `manage/clean-lightly.py`
* Cleanup all local files (DB, config, Python caches, logs, ...): `manage/clean-all.py`
* Run linter (check source formatting): `manage/lint.py`
* Run tests: `manage/test.py`
* Run some checks (like the linter, tests, some validation): `manage/check.py`
* Make migrations (after model changes): `manage/make-migrations.py`
* Make translations (updates `locale/nb/django.po`): `manage/make-translations.py`

## Upgrading Dependencies

* This project uses pip-tools with all-dep pinning.
* Run `manage/update-deps.sh` to update dependencies.
* Go through all dep updates (as shown in by the script or git diff), read the changelogs for the changes, and make sure they don't mess things up.

## Making Changes

* If you're committing code changes, run `manage/check.sh` first to make sure the formatting is correct and that tests still pass.
* If you're adding/changing/fixing features, add it to the changelog.

## Run with Docker

Building and running the app in Docker is intended just for testing Docker stuff.
Running the different tools still require Virtualenv to be set up.

* Setup: `manage/docker/setup.sh` (first time or after project change)
* Run server: `manage/docker/run.sh`
