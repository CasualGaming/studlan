ENV=./env/bin
SHELL := /bin/bash
PYTHON=$(ENV)/python
PIP=$(ENV)/pip
MANAGE=$(PYTHON) manage.py

collect_static:
	$(MANAGE) collectstatic

flake8:
	flake8

migrate:
	$(MANAGE) migrate


prod:
	$(PIP) install -r requirements.txt --upgrade

env:
	virtualenv -p `which python` env

clean:
	pyclean .
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.egg-info

test:
	$(MANAGE) test

run:
	$(MANAGE) runserver 0.0.0.0:8000

freeze:
	mkdir -p requirements
	$(PIP) freeze > requirements/base.txt
