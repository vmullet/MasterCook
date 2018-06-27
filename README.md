# MasterCook

- First, you have to install Django

```
pip install django
pip install Pillow
pip install python-slugify
```
https://github.com/un33k/python-slugify

- Then, you must have getText installed for translations

https://mlocati.github.io/articles/gettext-iconv-windows.html

## Set up

- Then, you have to apply some migrations

```
python manage.py makemigrations generic
python manage.py migrate generic
```

```
python manage.py makemigrations accounts
python manage.py migrate accounts
```

```
python manage.py makemigrations ingredients
python manage.py migrate ingredients
```

```
python manage.py makemigrations recipes
python manage.py migrate recipes
```

```
python manage.py migrate
```


## Start Project

- Once you have done that, simply run the server

```
django-admin compilemessages
python manage.py runserver
```