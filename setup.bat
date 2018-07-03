@echo off
REM ######################################################
REM ############### MASTERCOOK SETUP SCRIPT ##############
REM ######################################################

pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixture.json
django-admin compilemessages
python manage.py runserver
 
 
