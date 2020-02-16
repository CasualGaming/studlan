# Deployment

## Docker Hub Registry

Make sure your personal or organizational user exists. Copy the username and password to Travis, so that it can log in.

## Travis CI

Connect your personal or organizational Travis CI user to your GitHub account. Add any required encorinment variables. Setup periodic builds using Cron jobs in case dependencies or parent images are updated.

### Encrypting Files and Values for Travis CI

The recommended way secure sensitive data.

Login and logout with `travis login --com` and `travis logout`.

Encrypt environment variable values:
The value can be an arbitrary string, but is commonly an environment variable value pair.
1. Run `travis encrypt --com -r <user>/<repo> <envvar>=<value>`.
1. Copy the output text to the `env.global` list in `.travis.yml` with a comment for the variable name.

Encrypt file:
Only one file can be encrypted. To encrypt multiple files, add them to an archive.
1. Run `travis encrypt-file --com -r <user>/<repo> <file>`.
1. Add the output command in `.travis.yml`.
1. Copy the encrypted file to the repo.
1. Optionally delete the unencrypted file.

## Deployment Site

* (Optional) Create a non-admin user which can login with pubkey alone (if deploying with CI/CD).
* Create a Django local settings file. Remember to add a randomly generated secret and disable debug mode.
* Create a Docker Compose file with appropriate volume bindings and network settings.
* Setup a database or use the built-in SQLite database or suggested PostgreSQL database.
* For PostgreSQL, use the sample `recreate-db.sh` script to setup or recreate the DB.
* Setup an Nginx reverse proxy to serve the site over TLS.
* Setup TLS certs with automatic renewal (Let's Encrypt).
* Test TLS: [Qualys' SSL Server Test](https://www.ssllabs.com/ssltest/)
* Setup a mail relay (Mailgun).
* Setup backup.
* Fix permissions to make sure unrelated users cannot read secret configs, and to prevent privilege escalation by replacing sudoable/setuided scripts.
* Test both IPv4 and IPv6 reachability for the web server.
* To test Stripe, get your pair of testing (not live) keys from your Stripe account, and try to pay with a [testing card](https://stripe.com/docs/testing)
