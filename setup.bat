@echo off
REM ######################################################
REM ############### MASTERCOOK SETUP SCRIPT ##############
REM ######################################################

pip install virtualenv
virtualenv env
.\env\Scripts\activate & pip install -r requirements.txt & python manage.py migrate & python manage.py loaddata & django-admin compilemessages & python manage.py runserver
 
 
