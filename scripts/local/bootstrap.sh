#!/bin/bash
#
# Bootstrap virtualenv environment and postgres databases locally.
#
# NOTE: This script expects to be run from the project root with
# ./scripts/local/bootstrap.sh

set -o pipefail

set -a
source scripts/local/vars.env
set +a

# Install Python development dependencies
pip3 install -r requirements.txt

# Create Postgres databases
createdb navigator

# Upgrade database
python app/manage.py migrate

# Build search index
python app/manage.py build_index

# build front end assets
npm install && npm run build

# Udpate the webdriver
npm run webdriver_update

# Collect static
python app/manage.py collectstatic --noinput 
