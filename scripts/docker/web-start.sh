#!/bin/bash

set -a
source vars.env
set +a

npm run build
npm run watch &

cd app

python manage.py migrate --noinput
python manage.py collectstatic --noinput 
python manage.py build_index
python manage.py runserver 0:8000
