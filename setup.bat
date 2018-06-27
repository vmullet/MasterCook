REM ######################################################
REM ############### MASTERCOOK SETUP SCRIPT ##############
REM ######################################################

@echo off

REM Migrations for generic app

echo Start Migrations...

python manage.py makemigrations generic
python manage.py migrate generic

REM Migrations for accounts app

python manage.py makemigrations accounts
python manage.py migrate accounts

REM Migrations for ingredients app

python manage.py makemigrations ingredients
python manage.py migrate ingredients

REM Migrations for recipes app

python manage.py makemigrations recipes
python manage.py migrate recipes

REM Global migrations for project

python manage.py makemigrations
python manage.py migrate

REM Load Initial data
REM python manage.py loaddata

REM Compile messages for translations (getText must be installed)

django-admin compilemessages

REM Run the server

echo Server Starting...

python manage.py runserver

REM Open web browser

start "" http://127.0.0.1:8000/