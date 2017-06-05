[![CircleCI](https://circleci.com/gh/uktrade/navigator.svg?style=svg)](https://circleci.com/gh/uktrade/navigator)
[![dependencies Status](https://david-dm.org/uktrade/navigator/status.svg)](https://david-dm.org/uktrade/navigator)
[![devDependencies Status](https://david-dm.org/uktrade/navigator/dev-status.svg)](https://david-dm.org/uktrade/navigator?type=dev)

# navigator

Department of International Trade marketplace navigator.

## Features of this application

 - To be added??

## First-time setup

Languages/applications needed
- Python 3.5
- Postgres [postgres](https://www.postgresql.org)
- Heroku Toolbelt [heroku](https://toolbelt.heroku.com)


The app runs within a virtual environment. To [install virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html), run
```shell
    [sudo] pip install virtualenv
```

Install virtualenvwrapper
```shell
    [sudo] pip install virtualenvwrapper
```

Create a local environment.sh file containing the following:
```shell
echo "
export DJANGO_SETTINGS_MODULE='navigator.settings.dev'
export DATABASE_URL='postgres://localhost/navigator'
export SECRET_KEY='REPLACE ME WITH AN ACTUAL SECRET KEY'
export STORAGE_TYPE='local'
"> environment.sh
```

Make a virtual environment for this app:
```shell
    mkvirtualenv -p /usr/local/bin/python3.5 navigator
```

Install dependencies
```shell
    ./scripts/bootstrap.sh
```

## Running the application

Running with django runserver:
```shell
    workon navigator
    python manage.py runserver
```
Then visit [localhost:8000](http://localhost:8000)

Or through heroku:
```shell
    workon navigator
    heroku local
```
Then visit [localhost:5000](http://localhost:5000)

## Running tests

Tests include a pep8 style check, django test script and coverage report.

```shell
    workon navigator
    ./scripts/run_tests.sh
```

####To run end to end tests locally

Install the webdriver
```shell
    gulp webdriver_update
```

Run the tests
```shell
    gulp protractor:e2e
```