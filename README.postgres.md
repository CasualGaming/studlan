# Studlan #

## README.postgres ##

Install notes if you want to use Postgresql when deploying Studlan. 

## Basic for any install ##

1. apt-get build-dep python-psycopg2 (non Debian/Ubuntu need to fix headers for psycopg2 python bindings and postgresql themself!)

2. source virtualenv (which is a «virtualenv --no-site-packages»)

3. pip install egenix-mx-base (fixes: django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 module: can't import mx.DateTime module for Django version < 1.4. Not bad to have for latest django either ...)

## Django 1.4>= ##

1. pip install psycopg2 

## Django Django1.3 or less ##

* TODO: Figure out how to pass "-I/virtualenv/full/path/site-packages/mx" so psycopg2 builds postgres python adapter with bindings from egenix-mx-base (mx.DateTime) in our virtualenv.

* WARNING: Wont work before TODO fixed for Django1.3... be free to figure it out or just be a good boy and use lateast Django 1.4!

* DOH: Shouldn't really care about this issue as it is Django 1.2 in Debian Squeeze (current stable) and Debian Wheezy which is next stable will have Django 1.4 anyway!

1. pip install psycopg2==2.4.1
