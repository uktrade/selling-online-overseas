#!/bin/bash

export DJANGO_SETTINGS_MODULE='navigator.settings.test'
export DATABASE_URL='postgres://@localhost/navigator'
export PHANTOMJS_BIN='node_modules/phantomjs/bin/phantomjs'
export SECRET_KEY='TEST_SECRET_KEY'
export RESTRICT_IPS=false
export STORAGE_TYPE='local'
