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
  PORT=9000
else
  PORT=${TEST_PORT}
fi

# Build the frontend
npm run build
display_result $? 1 "Run frontend build"

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


python3 app/manage.py migrate --noinput
display_result $? 2 "Migrate Django DB"

python3 app/manage.py collectstatic --noinput 
display_result $? 3 "Collect static"

python3 app/manage.py build_index
display_result $? 4 "Build search index"

# Run the webserver for running e2e tests
python3 app/manage.py runserver 0:${PORT} > /dev/null 2>&1 &
display_result $? 5 "Run Django server"

python3 app/manage.py build_index
display_result $? 6 "Build Whoosh index"

python3 app/manage.py collectstatic --noinput > /dev/null
display_result $? 7 "Collecting static"

pep8 app
display_result $? 8 "Code style check"

npm run test
display_result $? 9 "Front end code tested and style check"

cd app && python3 manage.py test --noinput && cd -
display_result $? 10 "Unit tests"

npm run e2e
display_result $? 11 "End to end tests"
