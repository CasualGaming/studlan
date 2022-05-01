# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security


## [v1.9.1] - 2022-05-01

### Fixed

- Added missing ticket purchase date to Excel export.


## [v1.9.0] - 2021-09-20

### Added

- Added required checkboxes on the ticket checkout page for accepting the LAN rules and confirming that the user information is correct.
- Added separate page for tickets, including a navbar entry.

### Changed

- Changed which news labels are shown on front page and archive page.
- Updated default seatmap colors.

### Fixed

- Replaced the outdated pychal library with pychallonge (pychal was a fork of pychallonge but was since merged back into it).
- Fixed ugly percentage formatting in statistics and remove percentage from competition statistics.

### Security

- Upgraded vulnerable dependencies.

## [v1.8.1] - 2020-12-09

### Security

- Upgraded vulnerable dependencies.

## [v1.8.0] - 2020-09-09

### Added

- Added feature for sending emails to multiple users.
- Added optional URL slug for LANs.
- Added arrivals table filter for ticket/paid type.
- Added user admin panel filter for users with custom permissions.
- Added LAN participant statistics page.
- Added separate option for LAN media on front page.
- Added user info on ticket purchase page, to force users to check their info.
- Added LAN option for allowing manual payments on arrivals page.
- Added partner relation descriptions, in addition to the existing partner descriptions.
- Added poll app.

### Changed

- Replaced the old email backend "django-mailgun" with "django-anymail". (Configuration compatibility code has been added to avoid breaking existing Mailgun configurations.)
- Made the front page LAN header clickable.
- Reversed previous LAN lists so newest is on top.
- Prevented changing arrivals and manually register users for ended LANs.
- Made news cards a little prettier and added "read more" link if the content was cut.
- Made news date optional.
- Improve line and paragraph spacing in LAN descriptions, articles, etc.
- Change LAN ticket list visually from tabs to panels.

### Fixed

- Fixed after-login and after-logout redirect, including unsafe redirecting.

## [v1.7.0] - 2020-02-21

### Added

- Added LAN list for seatings.
- Added LAN list for schedules.

### Changed

- Made message severities more appropriate.
- Made arrivals toggle error messages more verbose.
- Separated sponsor list into different LANs.
- Renamed "sponsor" to "partner".
- Show users with tickets or seats on arrivals page even if they haven't attended.
- Replaced LAN banner video with LAN banner media which supports images as well.
  It is also shown on the front page together with the usual brief LAN info.

### Fixed

- Removed duplicates in sponsor sidebar for when the same sponsor is related to multiple upcoming LANs.
- Fixed users with multiple tickets or seats causing error 500.
- Fixed ticket paid status in arrivals being clickable.
- Fixed enter-to-submit for ticket purchase form.
- Fixed ticket purchase form not getting disabled when submitted with valid data.
- Fixed Markdown images in the LAN descriptions and article contents not being contained.
- Fixed news archive pagination.

### Security

- Fixed alias CSRF vulnerability.
- Fixed logout CSRF vulnerability.
- Fixed LAN attendance CSRF vulnerability.

## [v1.6.1] - 2019-10-17

### Fixed

- Fixed server error when viewing team competition page when not logged in.
- Fixed sponsor title text wrapping.

## [v1.6.0] - 2019-10-16

### Added

- Added list of participants and winners on lottery page.
- Added buttons to open and close raffles, including a permission to do so.
- Added optional payment enforcement to lotteries.- Added more info to compo page info tables and compo list.
- Added list of sponsored LANs to sponsor panels on sponsor page.
- Added confirm dialogs for arrival toggle buttons.
- Added filters on arrivals page for paid and arrived statuses.
- Added more info to compo page info tables and compo list.
- Added permission for showing team invites, regardless of membership status.
- Added config option to show version and default to hidden.
- Added Stripe payment descriptions for tickets.

### Changed

- Merged lottery info page and draw page.
- Made login, register, recover and set-password pages narrow.
- Centered narrow pages.
- Improved sponsorbar responsiveness.
- Left-aligned articles and LANs (they were block-aligned).
- Made tickets for a LAN always visible.
- Don't auto close compos when all spots are taken.
- Order competitions by status and then start time.
- Changed "competitions" in the navbar to "esports".
- Swapped positions for seating and esports in the navbar.
- Show team invitations to team members and staff only.
- Hide attend button on finished LANs.
- Enforce disabled ticket sale when the LAN is over.
- Enforce closed ticket sale when all tickets are sold.
- Redirect users to the LAN page when trying to reserve a seat without any ticket.
- Changed seating sidebar appearance and added list of applicable ticket types.

### Removed

- Removed link to lottery drawing from navbar.

### Fixed

- Fixed misaligned site logo.
- Fixed navbar overflowing into two rows on medium screens when logged out.
- Fixed unfair sponsor banner sizes, where some appeared larger than others.
- Fixee errors during payment being suppressed.
- Fixed compo sign-up as solo bypassing payment enforcement.
- Fixed ordering of LANs on front page for multiple active LANs.
- Fixed ordering of LANs on competition page for multiple active LANs.
- Fixed seating map rendering crashing if any seat objects are missing.
- Fixed seating map client script triggering on pressing inactive seats.
- Fixed LAN history list for users only including history with reserved seats.

### Security

- Fixed lottery CSRF vulnerability.

## [1.5.1] - 2019-08-01

### Changed

- Removed sponsor sidebar from sponsor page.

### Fixed

- Fixed missing LAN translations on LAN admin page.
- Fixed reversed order for sponsor priority.

## [1.5.0] - 2019-07-31

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
- Added help texts to competition fields tournament format and Challonge URL.
- Added new translations.
- Added ticket payment page, accessible from the LAN page.
- Added attendee to admin panel.

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
- Made schedule use current time zone instead of a hardcoded one.
- Made stream description optional.
- (Breaking change) Changed stream link type from entire iframe to just the link.
- Changed stream description from HTML to markdown.
- Made seating layout generator use relative coordinates instead of pixels.
- Made exported seating list and map prettier and i18n'd.
- Moved team invitation accept and decline links from invitation message to buttons on team page.
- Made error log rotating.
- Made activity description optional.
- Made LAN directions description optional.
- Made stream description optional.
- Update stripe integration to use payment intents and Stripe.js v3 to support SCA.

### Removed

- Removed unique email check from register form, since email addresses are non-unique.
- Removed unused sponsor logo field.
- Removed (moved) sidebar from top of page on small screens.
- Removed admin arror emails (it was broken anyways, and super spamming).

### Fixed

- Fixed HTML DOM bug (unclosed tag) in the seating app template.
- Fixed seating map size inconsistency across browsers.
- Fixed account recovery sending recovery emails to only one account for a certain email address.
- Fixed schedule failing to load.
- Fixed old translations not being compiled and used.
- (Breaking change) Fixed spelling of Challonge integration configuration.
- Fixed bug in match reporting for Challonge integration.
- Fixed old translations being deactivated/removed.
- Fixed admin panel crashing when trying to forcefully log out users.
- Fixed seating tabs not showing which tab is active.
- Fixed seating client script breaking if width and height of the SVG seating layout is not set.
- Users must now attend a lan before buying a ticket.
- Users cannot remove attendance from a lan if they have paid.

### Security

- Fixed seating CSRF vulnerability.
- Fixed team join/leave/etc. CSRF vulnerability.
- Fixed ticket release date not being properly enforced.

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
