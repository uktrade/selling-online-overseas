#!/bin/bash

set -e -o pipefail

while read service_name addon plan app status
do
  if [ $app = $CF_APP_NAME -a "$status" = "create succeeded" ]
  then
    echo "Postgres service already bound"
    exit 0
  fi
done < <(cf services | grep $CF_APP_NAME)

echo "Finding available postgres service"

cf services
while read service_name addon plan status
do
  if [ "$status" = "create succeeded" ]
  then
    break
  fi
done < <(cf services | grep "navigator-review")

if [ "$status" != "create succeeded" ]
then
  echo "No unbound postgres service found"
  exit 1
fi

echo "Binding to postgres $service"
cf bind-service $CF_APP_NAME $service_name
