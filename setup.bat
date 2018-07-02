REM ######################################################
REM ############### MASTERCOOK SETUP SCRIPT ##############
REM ######################################################

@echo off

REM Setup environment

REM mkvirtualenv mastercook-env
REM workon mastercook-env

REM Migrations for generic app

echo Start Migrations...

REM Generate Database

REM python manage.py migrate

REM Load Initial data
REM python manage.py loaddata

REM Compile messages for translations (getText must be installed)

REM django-admin compilemessages

REM Run the server

echo Server Starting...

REM python manage.py runserver

REM Open web browser

REM start "" http://127.0.0.1:8000/