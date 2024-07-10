#!/bin/bash

python manage.py migrate

gunicorn --bind 0.0.0.0:80 --workers 4 --timeout 120 newsdrop.wsgi:application
