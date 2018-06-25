#!/usr/bin/env bash

# Setup environment
#pip install django
pip install Pillow
pip install python-slugify

# Migrations for generic app
python manage.py makemigrations generic
python manage.py migrate generic

# Migrations for accounts app
python manage.py makemigrations accounts
python manage.py migrate accounts

# Migrations for ingredients app
python manage.py makemigrations ingredients
python manage.py migrate ingredients

# Migrations for recipes app
python manage.py makemigrations recipes
python manage.py migrate recipes

# Global migrations for project
python manage.py makemigrations
python manage.py migrate

# Load Initial data
python manage.py loaddata

# Compile messages for translations (getText must be installed)
django-admin compilemessages

# Run the server
python manage.py runserver