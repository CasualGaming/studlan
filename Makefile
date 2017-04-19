ENV=./env/bin
SHELL := /bin/bash
PYTHON=$(ENV)/python
PIP=$(ENV)/pip
MANAGE=$(PYTHON) manage.py

collect_static:
	$(MANAGE) collectstatic --noinput --clear --link

flake8:
	flake8

migrate:
	$(MANAGE) migrate


prod:
	$(PIP) install -r requirements/production.txt --upgrade

dev:
	$(PIP) install -r requirements/development.txt --upgrade

env:
	virtualenv -p `which python2` env

clean:
	pyclean .
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.egg-info

test:
	$(MANAGE) test

run:
	$(MANAGE) runserver 0.0.0.0:8000

# General
REPO=CasualGaming/studlan

sign:
	drone sign $(REPO)
