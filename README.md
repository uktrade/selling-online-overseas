[![CircleCI](https://circleci.com/gh/uktrade/navigator.svg?style=svg)](https://circleci.com/gh/uktrade/navigator)
[![dependencies Status](https://david-dm.org/uktrade/navigator/status.svg)](https://david-dm.org/uktrade/navigator)
[![devDependencies Status](https://david-dm.org/uktrade/navigator/dev-status.svg)](https://david-dm.org/uktrade/navigator?type=dev)

# navigator

Department of International Trade marketplace navigator.

## First-time setup

Languages/applications needed
- Python 3
- Docker & Docker Compose [docker](https://www.docker.com) (optional)
- Postgres 9 [postgres](https://www.postgresql.org) (required if NOT using docker)
- Node 6 [node](https://nodejs.org/en/) (required if NOT using docker)
- Java 8 runtime [java](http://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html) (required if NOT using docker)

## Installation

The project runs either locally using virtual environments, or within Docker containers

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

### Virtualenv

Ensure you have [Postgres](https://www.postgresql.org), and [Node](https://nodejs.org/en/) installed locally.

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

Then visit [localhost:8000](http://localhost:8000)

## Running tests

Tests include a pep8 style check, django test script and coverage report.

```shell
    workon navigator # Only required if running in virtualenv, not docker
    make test
```

## Rebuilding

If you need to rebuild the project, wiping the database, run:
```shell
    make rebuild
```
