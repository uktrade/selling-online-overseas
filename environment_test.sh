#!/bin/bash

export DJANGO_SETTINGS_MODULE='navigator.settings.prod'
export DATABASE_URL='postgres://@localhost/navigator'
export PHANTOMJS_BIN='node_modules/phantomjs/bin/phantomjs'
