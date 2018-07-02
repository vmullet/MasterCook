#!/usr/bin/env bash

# Setup environment

pip install virtualenvwrapper

mkvirtualenv mastercook-env
workon mastercook-env

# Install Requirements
pip install -r requirements.txt

# Generate Database structure
python manage.py migrate

# Load Initial data
python manage.py loaddata

# Compile messages for translations (getText must be installed)
django-admin compilemessages

# Run the server
python manage.py runserver

# Open project in the web browser
python -mwebbrowser http://127.0.0.1:8000/