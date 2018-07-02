#!/usr/bin/env bash

# Setup environment

pip install virtualenv
virtualenv env
source env/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata fixture.json && django-admin compilemessages && python manage.py runserver