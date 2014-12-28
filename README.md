# Studlan #

## Features ##
* News
* Activites
		Used for having several competitions under the same activity (usually a game).
* Competitions
	* User or Team participation
			A competition can for either users or teams.
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
	* Automatic bracket creation/Tournament system.
			Takes seeding into account.
* Bootstrap 2.0 upgrade
* Non-fluid responsive layout

## Requirements ##
sudo apt-get install libpq-dev python-dev
pip install -r requirements.txt



## Initialization ##
1. python manage.py syncdb
2. python manage.py migrate

