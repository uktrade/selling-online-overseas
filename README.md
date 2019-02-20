# Selling Online Overseas

Welcome to the Department of International Trade's Selling Online Overseas service. This was originally internally called the "marketplace navigator".

## First-time setup

## Installation

You will need first to install
- Python 3
- Postgres 9 [postgres](https://www.postgresql.org)
- Node 6 [node](https://nodejs.org/en/)
- Java 8 runtime [java](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html)
- Virtualenv [Virtualenv] https://virtualenv.pypa.io

In terminal, in the main folder for this project, create a new Virtual Environment
```$ virtualenv ENV```

Add the following environment variables to your virtual environment:
```
DATABASE_URL=postgres://localhost/navigator
DJANGO_SETTINGS_MODULE=navigator.settings.dev
SECRET_KEY=REPLACE_ME_WITH_AN_ACTUAL_SECRET_KEY
STORAGE_TYPE=local
```

One approach to this without any further installation, is as follows. Inside the `ENV/bin/activate` script, add environment variable setting (at the bottom) and unsetting (in the deactivate function)
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

Each time you enter the repository in terminal, or start a new terminal window, you will need to activate the virtual environment using
```source env/bin/activate```

Next, run the scripts to set up the project. You will need a local database management app running, for example postgresapp on Mac [postgresapp](https://postgresapp.com/).

A set of scripts to manage the project are inside the make file. Running ```$ make build_local``` itself will run the "build_local" script inside make file that sets up the project. If this command raises any errors, you can debug this by reviewing and runing the individual commands within the make_file.

```$ make run_local``` will build and run the local server. This will be available in your browser at [localhost:8008](http://localhost:8008)

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

## Running tests

Tests include a pep8 style check, django test script and coverage report.

```$ make test```

## Rebuilding

If you need to rebuild the project, wiping the database, run:
```$ make rebuild```


## Links

[![CircleCI](https://circleci.com/gh/uktrade/navigator.svg?style=svg)](https://circleci.com/gh/uktrade/navigator)
[![codecov](https://codecov.io/gh/uktrade/navigator/branch/master/graph/badge.svg)](https://codecov.io/gh/uktrade/navigator)
[![gemnasium](https://gemnasium.com/badges/github.com/uktrade/navigator.svg)](https://gemnasium.com/github.com/uktrade/navigator)



# Legacy Installation Instructions, for Reference

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

These outdated instructions are kept here for reference as of 20 Feb 2019.

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

## Running the project

To just run the project, execute the following (activating the virtual environment with `workon` is not necessary if using docker):
```shell
    workon navigator # Only required if running in virtualenv, not docker
    make run
```

Then visit [localhost:8008](http://localhost:8008)