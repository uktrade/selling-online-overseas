#!/bin/bash
#
# Run project end-to-end tests
#
# NOTE: This script expects to be run from the project root via the run_tests.sh script

# Start the django server in the background
python manage.py runserver
nohup python manage.py runserver & > /dev/null 2>&1

# Test for django to come up using curl
echo -n "Waiting for django "
until $(curl --output /dev/null --silent --head --fail http://localhost:8000); do
    printf '.'
    sleep 0.2
done

echo " Django started"

# Run the end-to-end tests and save the exist status
gulp e2e
res=$?

# Kill the most recent python process (django)
pkill -n python

# Exit with the status of the tests
exit $?
