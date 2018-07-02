#!/usr/bin/env bash

# Setup environment

mkvirtualenv mastercook-env
workon mastercook-env

# Install pip dependencies
pip install django
pip install Pillow
pip install python-slugify

# Generate Database
python manage.py migrate

# Load Initial data
python manage.py loaddata

# Compile messages for translations (getText must be installed)
django-admin compilemessages

# Run the server
python manage.py runserver

# Open project in the web browser
python -mwebbrowser http://127.0.0.1:8000/