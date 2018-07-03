#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixture.json
django-admin compilemessages
python manage.py runserver