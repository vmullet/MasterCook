#!/usr/bin/env bash

# Setup environment

pip install virtualenvwrapper
mkvirtualenv mastercook-env
workon mastercook-env && pip install -r requirements.txt && python manage.py migrate && python manage.py loaddata fixture.json && django-admin compilemessages && python manage.py runserver