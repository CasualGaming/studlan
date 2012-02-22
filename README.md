# Studlan #

## Features ##
* News
* Activites
  _Used for having several competitions under the same activity (usually a game)._
* Competitions
	* User or Team participation
	  _A competition can for either users or teams._
* Teams
	* Team Leader
		* Can add members
		* Can sign the team up for competitions, leave or forfeit them.
	* Members

## Planned features ##
* Teams
	* History
	* Seeding (for any activity)
* Competitions
	* Automatic bracket creation/Tournament system. Takes seeding into account.
* Bootstrap 2.0 upgrade
* Non-fluid responsive layout

## Requirements ##
* Django 1.3
* South

## Initialization ##

1. comment all apps's (news, competition, misc) modules in settings.py and run python manage.py syncdb
2. python manage.py createsuperuser
3. uncomment the modules you commented in step one in settings.py
4. python manage.py schemamigration news --initial
5. python manage.py schemamigration competition --initial
6. python manage.py schemamigration misc --initial
7. python manage.py migrate news
8. python manage.py migrate competition
9. python manage.py migrate misc
