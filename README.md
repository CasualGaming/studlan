# Studlan #

## Initialization ##

* comment all apps's (news, competition, misc) modules in settings.py and run python manage.py syncdb
* python manage.py createsuperuser
* uncomment the modules you commented in step one in settings.py
* python manage.py schemamigration news --initial
* python manage.py schemamigration competition --initial
* python manage.py schemamigration misc --initial
* python manage.py migrate news
* python manage.py migrate competition
* python manage.py migrate misc
