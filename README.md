[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

# Selling Online Overseas

Welcome to the Department of International Trade's Selling Online Overseas service.

This respository was originally named `navigator`, and within the repository the main django app and local database are still named `navigator`.
 
## Installation

Locally install:
- Python 3
- Postgres 9 [postgres](https://www.postgresql.org)
- Node 6 [node](https://nodejs.org/en/)
- Java 8 runtime [java](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html)
- Virtualenv [VirtualEnv](https://virtualenv.pypa.io)
- A database management app. On Mac a good option is [postgresapp](https://postgresapp.com/)

...And create a new Virtual Environment using ```$ virtualenv ENV``` in the project root folder.

### Add local environment variables

Add the following environment variables to your local environment.
```
DATABASE_URL=postgres://localhost/navigator
DJANGO_SETTINGS_MODULE=navigator.settings.dev
SECRET_KEY=REPLACE_ME_WITH_AN_ACTUAL_SECRET_KEY
STORAGE_TYPE=local
```

One approach is to add these to the `ENV/bin/activate` script. You will need to add environment variable setting at the bottom of the file and unsetting in the deactivate function.
```
  deactivate () {
    ...

    # Unset environment variables

    unset DATABASE_URL
    unset DJANGO_SETTINGS_MODULE
    unset SECRET_KEY
    unset STORAGE_TYPE
}

...

# Set environment variables

export DATABASE_URL=postgres://localhost/navigator
export DJANGO_SETTINGS_MODULE=navigator.settings.dev
export SECRET_KEY=lasdadslkdaslk
export STORAGE_TYPE=local
```

Activate the virtual environment using ```$ source env/bin/activate```. You will each time you start a new terminal window.

### Run the set up scripts

Start your local database management app.

Scripts to manage the project are inside the make file in the root folder.

Run ```$ make build_local``` to run the "build_local" script. If this raises any errors, you can debug by running the individual commands within this script which are listing or referenced in the make file.

### Run the local server

Run ```$ make run_local``` to run the local server. This will be available at [localhost:8008](http://localhost:8008)

### Run tests

The test script runs a pep8 style check, django tests and a coverage report.

```$ make test```

You are now in a position to contribute to the repository.

# Other Utilities

## Enabling Single Sign On (SSO)

To make the sso features work locally add the following to your machine's `/etc/hosts`:

| IP Adress | URL                  |
| --------  | -------------------- |
| 127.0.0.1 | buyer.trade.great    |
| 127.0.0.1 | supplier.trade.great |
| 127.0.0.1 | sso.trade.great      |
| 127.0.0.1 | api.trade.great      |
| 127.0.0.1 | profile.trade.great  |
| 127.0.0.1 | exred.trade.great    |

Then log into `directory-sso` via `sso.trade.great:8001`, and use `navigator` on `soo.trade.great:8008`

## Staff SSO

On local machine, SSO is turned off by default.
If you need to enable, set the `FEATURE_ENFORCE_STAFF_SSO_ENABLED` to `true`.
You also need to set:
```
STAFF_SSO_AUTHBROKER_URL
AUTHBROKER_CLIENT_ID
AUTHBROKER_CLIENT_SECRET
```

 Speak to webops or a team mate for the above values.


## Rebuilding the project

If you need to rebuild the project, wiping the database, run:
```$ make rebuild```

--------

# Legacy Documentation for Reference

These older instructions are kept here for reference as of 20 Feb 2019.

## Installation Instructions

It  either locally using virtual environments, or within Docker containers

### First-time setup

Languages/applications needed
- Python 3
- Docker & Docker Compose [docker](https://www.docker.com) (optional)
- Postgres 9 [postgres](https://www.postgresql.org) (required if NOT using docker)
- Node 6 [node](https://nodejs.org/en/) (required if NOT using docker)
- Java 8 runtime [java](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html) (required if NOT using docker)

### Docker

Create a local file to instruct `make` that you want to use docker:
```shell
echo "
NAV_BUILD_TYPE=docker
"> build.env
```

Create a local `.env` file with the development and testing ports you want to use:
```shell
echo "
DEV_PORT=8000
TEST_PORT=9000
"> .env
```

Create a local file to store your any custom environment variables, for starters, the Django settings module for the dev container to use:
```shell
echo "
DJANGO_SETTINGS_MODULE=navigator.settings.dev
"> vars.env
```

Set up the containers, build the project, and run the server:
```shell
make
```


## Legacy Virtual Env Installation Instructions

Create a local file to instruct make that you want to use local building:
```shell
echo "
NAV_BUILD_TYPE=local
"> build.env
```

Create a local file to store your desired environment variables:
```shell
echo "
DATABASE_URL=postgres://localhost/navigator
DJANGO_SETTINGS_MODULE=navigator.settings.dev
SECRET_KEY=REPLACE_ME_WITH_AN_ACTUAL_SECRET_KEY
STORAGE_TYPE=local
"> scripts/local/vars.env
```

To [install virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html), run
```shell
    [sudo] pip install virtualenv virtualenvwrapper
```

Make a virtual environment for this app:
```shell
    mkvirtualenv -p /usr/local/bin/python3 navigator
```

Install dependencies, set up the database, and run the project:
```shell
    make
```

## Legacy Running the project

To just run the project, execute the following (activating the virtual environment with `workon` is not necessary if using docker):
```shell
    workon navigator # Only required if running in virtualenv, not docker
    make run
```

Then visit [localhost:8008](http://localhost:8008)


## Helpful links
* [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)
* [Gitflow branching](https://uktrade.atlassian.net/wiki/spaces/ED/pages/737182153/Gitflow+and+releases)
* [GDS service standards](https://www.gov.uk/service-manual/service-standard)
* [GDS design principles](https://www.gov.uk/design-principles)
 ## Related projects:
https://github.com/uktrade?q=directory
https://github.com/uktrade?q=great


[code-climate-image]: https://codeclimate.com/github/uktrade/navigator/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/navigator

[circle-ci-image]: https://circleci.com/gh/uktrade/navigator/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/navigator/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/navigator/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/navigator

[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg
[calver]: https://calver.org
