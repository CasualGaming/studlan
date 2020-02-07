[![GitHub release](https://img.shields.io/github/release/CasualGaming/studlan.svg)](https://github.com/CasualGaming/studlan/releases)
[![Build Status](https://travis-ci.org/CasualGaming/studlan.svg?branch=master)](https://travis-ci.org/CasualGaming/studlan)
[![Snyk](https://snyk.io/test/github/CasualGaming/studlan/badge.svg)](https://snyk.io/test/github/CasualGaming/studlan)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?branch=master&project=CasualGaming_studlan&metric=alert_status)](https://sonarcloud.io/dashboard?id=CasualGaming_studlan)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FCasualGaming%2Fstudlan.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FCasualGaming%2Fstudlan?ref=badge_shield)

# studlan
LAN-party event management system.

* [Demo](https://studlan.casualgaming.dev)
* [Docker Hub](https://hub.docker.com/r/casualgaming/studlan)
* [Travis CI](https://travis-ci.org/CasualGaming/studlan)
* [Snyk](https://snyk.io/test/github/CasualGaming/studlan)
* [SonarCloud](https://sonarcloud.io/dashboard?id=CasualGaming_studlan)

## Docs
* [Development](docs/development.md)
* [Releasing](docs/releasing.md)
* [Deployment](docs/deployment.md)
* [Docker Image](docs/docker-image.md)

## Features
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

(This list may be slightly outdated.)


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FCasualGaming%2Fstudlan.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FCasualGaming%2Fstudlan?ref=badge_large)