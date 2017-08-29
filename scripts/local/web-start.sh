#!/bin/bash

set -a
source scripts/local/vars.env
set +a

if [ -z "${DEV_PORT}" ]; then 
  PORT=8000
else
  PORT=${DEV_PORT}
fi

python app/manage.py runserver 0:${PORT}
