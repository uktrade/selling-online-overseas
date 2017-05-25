#!/bin/bash

set -a
source vars.env
set +a

if [ -z "${DEV_PORT}" ]; then 
  PORT=8000
else
  PORT=${DEV_PORT}
fi

npm run build
npm run watch &

cd app

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput 
python3 manage.py build_index
python3 manage.py runserver 0:${PORT}
