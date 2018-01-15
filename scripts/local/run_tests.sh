#!/bin/bash
#
# Run project unit tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/local/run_tests.sh

set -o pipefail

set -a
source scripts/local/test.env
set +a

if [ -z "${TEST_PORT}" ]; then 
  export PORT=9000
else
  export PORT=${TEST_PORT}
fi

pip install -r requirements_for_test.txt

npm run build

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

# Run the webserver for running e2e tests
python app/manage.py runserver 0:${PORT} > /dev/null 2>&1 &
display_result $? 1 "Run Django server"

python app/manage.py build_index > /dev/null
display_result $? 2 "Build Whoosh index"

python app/manage.py collectstatic --noinput > /dev/null
display_result $? 3 "Collecting static"

pep8 app
display_result $? 4 "Code style check"

npm run test
display_result $? 5 "Front end code tested and style check"

cd app && python manage.py test --noinput && cd -
display_result $? 6 "Code coverage"

#deactivate end to end tests for now, since they dont run in CircleCI
#npm run e2e
#display_result $? 7 "End to end tests"
