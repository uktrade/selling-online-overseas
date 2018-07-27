#!/bin/bash
#
# Run project unit tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/local/run_tests.sh

set -o pipefail

set -a
source test.env
set +a

if [ -z "${TEST_PORT}" ]; then
  export PORT=9000
else
  export PORT=${TEST_PORT}
fi

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

# Build the frontend
npm run build
display_result $? 1 "Run frontend build"

# Run the webserver for running e2e tests
python3 app/manage.py runserver 0:${PORT} > /dev/null 2>&1 &
display_result $? 2 "Run Django server"

python3 app/manage.py build_index
display_result $? 3 "Build Whoosh index"

python3 app/manage.py collectstatic --noinput > /dev/null
display_result $? 4 "Collecting static"

pep8 app
display_result $? 5 "Code style check"

npm run test
display_result $? 6 "Front end code tested and style check"

pip install -r ./requirements_test.txt --src /usr/local/src

cd app && pytest . -vv --cov=. --cov-config=.coveragerc --capture=no --cov-report=html && cd -
display_result $? 7 "Unit tests"

npm run e2e
display_result $? 8 "End to end tests"
