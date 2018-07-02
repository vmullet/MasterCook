REM ######################################################
REM ############### MASTERCOOK SETUP SCRIPT ##############
REM ######################################################

@echo off

REM Setup Environment...

pip install virtualenv
virtualenv env
.\env\activate

pip install -r requirements.txt

REM Generate Database...

python manage.py migrate

REM Load Fixtures...

python manage.py loaddata

REM Compile Translations

django-admin compilemessages

REM Server Starting...

python manage.py runserver

REM Open web browser

start "" http://127.0.0.1:8000/