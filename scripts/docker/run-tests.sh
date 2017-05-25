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
python app/manage.py runserver 0:8000 > /dev/null 2>&1 &

python app/manage.py build_index
display_result $? 1 "Build Whoosh index"

python app/manage.py collectstatic --noinput > /dev/null
display_result $? 2 "Collecting static"

pep8 app
display_result $? 3 "Code style check"

npm run test
display_result $? 4 "Front end code tested and style check"

cd app && coverage run manage.py test && cd -
display_result $? 5 "Code coverage"

npm run e2e
display_result $? 6 "End to end tests"
