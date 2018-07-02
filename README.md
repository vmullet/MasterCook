# MasterCook

**MasterCook** is a website developed with **Django framework** to share recipes across the world

## Project Structure

### Apps

As a Django Project, it is divided into multiple apps :

- **accounts** : An app to store everything related to users / profiles (login,signup,change password, dashboard...)
- **ingredients** : An app to store everything related to ingredients (only models)
- **recipes** : An app to store everything related to Recipes
- **utils** : An app to store everything which is not directly related to any apps such as generic models (Country,Currency...) or which can be used in any apps (template tags...)

With apps, you have also other folders which are :

- **assets** : Folder to store css / js / img files for the front of the website
- **locale** : Folder to store translations for the website
- **media** : Folder where are stored all uploaded medias
- **mastercook** : Folder where are stored main elements for the project (settings, urls configuration)

### Templates

Every apps has its own templates folder. For every templates folder, you will have :

- Main templates with names starting by **[APP_NAME]_xxxx.html** at the root of the templates folder
- Forms subfolder : Template for forms used by this app with names starting by **[_form]_xxxx.html**
- Parts subfolder : Template fragments used by main templates with names starting by **[_]xxxx.html**

At the root of the project, you have also a templates folder to store base templates for the main design of the website (menu,header,footer,css/js imports...)

The main template used everywhere in this website is **base_layout.html** in templates root folder

## Supported Features

Actually, the website supports the following features :

* General :
    * Two languages supported : **French and English** (main language set to English)
    * **Language switcher** in the main menu (see Languages section)
    * Models translation

* Users :
    * **login** / **signup** / **logout**
    * **change password**
    * **edit their own profile**
    * **consult other users' profiles**
    * **dashboard**
        * manage my recipes
        * manage my latest rates given to recipes

* Recipes :
    * **home page** with latest published recipes
    * **details page**
    * **rate recipes**
    * **create recipe**
    * **edit recipes** (only for the author)
        * edit main informations
        * add / delete photos
        * add / delete ingredients
        * add / delete / reorder steps
    * **delete recipes** (only for the author)


## Dependencies 

As any website, this django project has some dependencies on the two sides: front-end and back-end.
Indeed, they are managed internally so they wont't cause you any problems.

* Back-End :
    * **[Django](https://www.djangoproject.com/)** : No joke :p
    * **[Pillow](https://pillow.readthedocs.io/en/5.2.x/)** : A python library To handle image field in Django Models
    * **[Python-Slugify](https://github.com/un33k/python-slugify)** : A very useful package to slugify any string (UTF8 compatible)
    * **[Django-Modeltranslation](http://django-modeltranslation.readthedocs.io/en/latest/index.html) : A package to translate models**
    * **[Gettext](https://www.gnu.org/software/gettext/)** : Needed to make / compile translations ([windows version](https://mlocati.github.io/articles/gettext-iconv-windows.html) -> Download the latest binary)
    

* Front-End :
    * **[Bootstrap](https://getbootstrap.com/)**
    * **[Jquery](https://jquery.com/)**
    * **[Bootstrap-rating](https://github.com/kartik-v/bootstrap-star-rating)** : A very beautiful / simple library to represent star rating forms


## Installation

The installation of the project is very simple :

**Be sure that you have [gettext installed](https://www.gnu.org/software/gettext/) (or [gettext for windows](https://mlocati.github.io/articles/gettext-iconv-windows.html)) before executing the following actions !**

* For Mac / Linux Users **(just execute setup.sh)** :
```
git clone https://gitlab.com/LostArchives/MasterCook
cd MasterCook
chmod +x setup.sh
./setup.sh
```

* For Windows Users **(just execute setup.bat)** :
```
git clone https://gitlab.com/LostArchives/MasterCook
cd MasterCook
setup.bat
```

These scripts will do the following actions :

* create a virtualenv called env and activate it
* install pip dependencies (django, pillow, python-slugify, django-modeltranslation)
* migrate
* load fixtures
* compile translations
* runserver