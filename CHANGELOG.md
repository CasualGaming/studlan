# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Added
- Added version info to the app, shown in the site footer.
- Added video frame to LAN.
- Added link(s) to active LAN(s) on front page.
- Added links to both user profile and LAN seating in the arrivals list.
- Added LAN listing for competitions.
- Added instructions for changing email address and password.
- Lottery now throws out all participants (but keeps winners) if the lottery does not have multiple winnings.
- Added list of competitions a user has or is participating in.
- Added seating info to user LAN history.

### Changed
- Made footer prettier.
- Removed user info from sidebar.
- Made news list pages single-column and less wasteful of space.
- Made sponsor page prettier.
- Made breadcrumbs more consistent and changed which pages show them.
- Made page headers visually more consistent and appropriate.
- Made email templates slightly prettier and added HTML version.
- Replaced logo images with higher-definition versions (but same graphics).
- Replaced default sidebar with sponsorbar.
- Made seating layout generator use relative coordinated instead of pixels.
- Made exported seating list and map prettier.

### Deprecated

### Removed
- Removed unique email check from register form, since email addresses are non-unique.
- Removed unused sponsor logo field.
- Removed (moved) sidebar from top of page on small screens.

### Fixed
- Fixed HTML DOM bug in the seating app template.
- Fixed seating map size inconsistency across browsers.
- Fixed account recovery sending recovery emails to only one account for a certain email address.
- Fixed old translations being deactivated/removed.

### Security


## [1.4.3] - 2019-04-03
### Fixed
- Fixed internal error when accessing `/profile`.


## [1.4.2] - 2019-04-01
### Added
- Added button on arrivals page for exporting paying participants for a LAN to an Excel sheet.
- Added buttons on lottery pages to go between details and drawing pages.

### Changed
- Replaced all is-staff checks with permission checks.
- Updated dependencies: stripe

### Fixed
- Fixed wrong join time and last login time on user profiles.
- Fixed string encoding error when exporting paying participants for a LAN to an Excel sheet.
- Fixed internal errors when viewing non-existing lotteries.
- Fixed wrong font for username in top bar.


## [1.4.1] - 2019-03-10
### Added
- Added command in Docker startup script for deleting expired sessions.

### Changed
- Hide the full names of users where they aren't needed.

### Fixed
- Fixed join date on user profiles.

### Security
- Fix broken auth for the downloadable PDF files for the seating.
- Replace the drop-down list with all usernames in the team invite section with a text field.


## [1.4.0] - 2019-03-10
### Added
- Added changelog file.
- Added HON95/Håvard N. as maintainer.
- Added Docker image as release medium.
- Added sample configs and scripts for deployment.
- Added actions in the user admin panel to activate and deactivate selected users.
- Added action in the user admin panel to forcefully logout selected users.
- Added error log file.

### Changed
- Replaced build/test/CI/CD tools: Replace a bunch of scripts and stuff, remove Vagrant, remove tox, replace Drone CI with Travis CI, use Docker Hub as image repo.
- Updated Django from v1.10 to v1.11.
- Updated dependency Stripe PyPI package from v1 to v2.
- Changed the user profile slightly. The user's full name is no longer shown publicly.

### Fixed
- Invalid ZIP codes no longer cause crashes when trying to save.
- Phone numbers are now required to adhere to an appropriate format.

### Security
- Replaced lotto RNG with crypto RNG.
- Added a minimum password length of 8 characters.
