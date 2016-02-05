Studlan
==========

Requirements
------------

Download the latest versions of the following software

* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](http://downloads.vagrantup.com/)
* [Git](http://git-scm.com)
    * the [GitHub for Windows](http://windows.github.com/) app is probably the easiest way to install and use Git on Windows
* SSH - On Windows SSH is included with Git/GitHub for Windows.

Installation
------------

# Git and repository setup
```bash
$ git config --global core.autocrlf false
$ git config --global user.name "<your github username>"
$ git config --global user.email <your.github@email.com>
$ git clone --recursive git@github.com:casualgaming/studlan.git
$ cd studlan
```

Alternatively on Windows, use the GitHub for Windows app to setup everything

Vagrant
=======

This will create a virtual machine with all that is required to start developing

* see the Vagrantfile for special VM configuration options and
* see the vagrantbootstrap.sh script for provisioning options

```bash
$ vagrant up
```

If anything goes wrong
```bash
$ vagrant reload # will re-up the machine without destroying it
$ vagrant destroy -f # delete everything to start from scratch
$ vagrant provision # re-run the provisioning (vagrantbootstrap.sh) task
```

After the machine is up and provisioned you can SSH to the instance to run a server
```bash
$ vagrant ssh # if prompted for a password just type 'vagrant'
$ workon studlan # this is the virtualenv
$ cd /vagrant # this is the mounted shared folder of the project root
$ python manage.py runserver 0.0.0.0:8000 # this will bind to all interfaces on port 8000 (forwarded as 8001)
```

Site should be available at http://localhost:8001

To suspend/resume the VM
```bash
$ vagrant suspend studlan
$ vagrant resume studlan
```

## Features ##
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
	

## Planned features ##
* Teams
	* Match history
	* Seeding (for any activity)
* Competitions
	* Challonge integration with Automatic bracket creation/Tournament system that takes seeding into account.
* Non-fluid responsive layout


## Requirements ##
sudo apt-get install libpq-dev python-dev
pip install -r requirements.txt


## Initialization ##
1. python manage.py syncdb
2. python manage.py migrate

