#!/bin/bash

set -a
source scripts/local/vars.env
set +a

python app/manage.py runserver 0:8000
