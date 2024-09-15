#!/bin/bash
DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
DJANGO_SETTINGS_MODULE=core.settings
cd $DJANGODIR
source /app/core/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
exec python3 manage.py runserver 185.172.57.69:8000
