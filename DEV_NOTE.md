# Dev Note

## important commands

### Start Project from bash

```
mkdir ./core/templates/
mkdir ./core/templates/core
pip freeze > requirements.txt
echo. > README.md
```
### Run first time in bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
py manage.py runserver

### Run project in bash
source .venv/Scripts/activate
py manage.py runserver

### Migration + Migrate
py manage.py makemigrations
py manage.py migrate


## Sources

    1. https://github.com/SteinOveHelset/exploredjangocustomusermodel 
    2. user permission -> https://youtu.be/WuyKxdLcw3w?si=vLcKJ853uy3rb2MM
