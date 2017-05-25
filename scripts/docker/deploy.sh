#!/bin/bash

set -e -o pipefail

if [ -z $CF_USERNAME] || [ -z $CF_PASSWORD ] || [-z $CF_APP_SPACE ] || [ -z $CF_APP_NAME ] || [ -z $CF_ORG ]
then
	echo "Must set environment variables: CF_USERNAME, CF_PASSWORD, CF_APP_SPACE, CF_APP_NAME, CF_ORG"
	exit 1
fi

cf login -a api.cloud.service.gov.uk -u $CF_USERNAME -p $CF_PASSWORD -s $CF_APP_SPACE -o $CF_ORG

npm run build

python3 app/manage.py build_index
python3 app/manage.py collectstatic --noinput

cf push $CF_APP_NAME --no-start

if [[ $CF_APP_NAME == *"navigator-review"* ]]
then
  echo "Review app detected"
  ./review_app_prepare.sh
fi

while read var; do
  varname="$(cut -d'=' -f1 <<< $var)"
  varval="$(cut -d'=' -f2 <<< $var)"
  if [[ $varname && $varval ]] 
    then cf set-env $CF_APP_NAME $varname "$varval"
  fi
done < vars.env

cf start $CF_APP_NAME
