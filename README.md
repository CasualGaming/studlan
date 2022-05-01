# studlan

[![GitHub release](https://img.shields.io/github/release/CasualGaming/studlan.svg)](https://github.com/CasualGaming/studlan/releases)
[![Build status](https://github.com/CasualGaming/studlan/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/CasualGaming/studlan/actions/workflows/ci-cd.yml)
[![Quality Gate status](https://sonarcloud.io/api/project_badges/measure?branch=master&project=CasualGaming_studlan&metric=alert_status)](https://sonarcloud.io/dashboard?id=CasualGaming_studlan)

LAN-party event management system.

* [Demo](https://studlan.casualgaming.dev)
* [Docker Hub](https://hub.docker.com/r/casualgaming/studlan)
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
