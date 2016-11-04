#!/bin/bash
#
# Run project end-to-end tests
#
# NOTE: This script expects to be run from the project root via the run_tests.sh script

# Start the django server in the background
nohup python manage.py runserver & > /dev/null 2>&1

sleep_delay=0.2
time_limit_seconds=10

counter_limit=`bc <<< "$time_limit_seconds/$sleep_delay"`

# Test for django to come up using curl
echo "Waiting for django, limit to $counter_limit retries" 
# Set a counter that can be used to exit to stop the script running forever
counter=0
until $(curl --output /dev/null --silent --head --fail http://localhost:8000); do
    # Increment the counter and check it's not beyond a limit
    counter=$((counter+1))
    if (($counter>$counter_limit))
        then
        # Kill python
        pkill -n python
        # Print a user-friendly message and exit
        echo ""
        echo "Django failed to come up - exiting"
        exit 666
    fi
    printf '.'
    sleep $sleep_delay
done

echo " Django started"

# Run the end-to-end tests and save the exist status
gulp e2e
res=$?

# Kill the most recent python process (django)
pkill -n python

# Exit with the status of the tests
exit $?
