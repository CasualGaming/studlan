# Development
## Setup
### Tools
* [Git](https://git-scm.com) or [GitHub for Windows](https://windows.github.com/)
* Python 2.7 w/ pip and friends (see section below)
* Docker and Docker Compose (optional)
* Travis Tool (optional)

### Installing Python 2 Virtualenv
Download and install Python 2.7 and Python 2 pip.
Be careful with `python` and `pip` on Windows, as both Python 2 and 3 use the same names for the programs.

```
# Linux
sudo pip install --upgrade pip virtualenv setuptools wheel
# Windows
py -2 -m pip install --upgrade pip virtualenv setuptools wheel
```

### Configuring Git
If using CLI (not some GUI app):
```
git config --global core.autocrlf false
git config --global user.name <username>
git config --global user.email <email-address>
```

### Installing and Configuring Docker
Install both Docker and Docker Compose (combined app on Windows).
On Linux, add yourself to the `docker` group and then re-log, so that you can run Docker commands as non-root.

### Installing Travis Tool
Optional, used for encrypting Travis CI secrets and files and stuff.
```
sudo apt install ruby-dev rubygems
sudo gem install travis
```

Alternatively, on Windows, use the GitHub for Windows app to setup everything

## Running
### Run with Virtualenv
This is the intended way to run the app and most scripts in `manage/`.

* Setup: `manage/setup.sh` (first time or after project change)
* Run server: `manage/run.sh`

### Tools
Most of these use venv and therefore requires `manage/setup.sh` to be run first (once).

* Cleanup some unimportant local files (Python caches, logs, ...): `manage/clean-lightly.py`
* Cleanup all local files (DB, config, Python caches, logs, ...): `manage/clean-all.py`
* Run linter (check source formatting): `manage/lint.py`
* Run tests: `manage/test.py`
* Run some checks (like the linter, tests, some validation): `manage/check.py`
* Make migrations (after model changes): `manage/make-migrations.py`

### Run with Docker
This way is intended just for testing Docker stuff.

* Setup: `manage/docker/setup.sh` (first time or after project change)
* Run server: `manage/docker/run.sh`

## Making Changes
* If you're committing code changes, run `manage/check.sh` first to make sure the formatting is correct and that tests still pass.
* If you're adding/changing/fixing features, add it to the changelog.
