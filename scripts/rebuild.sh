#!/bin/bash
#
# Nuke the database and reload the initial fixtures
#
# NOTE: This script expects to be run from the project root with
# ./scripts/rebuild.sh

set -o pipefail

# Drop Postgres databases
dropdb navigator

# re-bootstrap
./scripts/bootstrap.sh

# Load initial data fixtures
python manage.py loaddata initial_0001.json
