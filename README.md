# About
This project is a Django Rest Framework backend to support the my_currency project.

# Getting Started
## Prerequisites

- Python 3.11.10

## Initialize environment
- For initialize environment, you need to install venv, ignore if already have
    `sudo apt install python3.11-venv`
- Create env
    `python3.11 -m venv env`
- Activate env
    `source env/bin/activate`


## Initialize requirements
- For initialize requirements, enter the following command
    `pip install -r requirements.txt`


## Initialize environment variables

`.env` file needs to be generated in the my_currency root directory with the same level as .evn.template:
- create a file `.env` at the same level as `.env.template`
- Copy all variables from `.env.template` to `.env`

## Initialize database
- For this project, `postgres` database has been used, if you don't have postgres install it in you system - `https://www.postgresql.org/download/` or you can use sqlite3 also 
- For using sqlite3 you need to update the `DB_NAME` to `local`
- For `postgres`, after installation create a database, and a user and update the following snippet in `.env`
```
DB_NAME=
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_PORT=
```


## Create superuser
- For creating super user, enter the following command
    `python manage.py createsuperuser`
- After that enter all the data and the super user will be created


## Start server
```
python manage.py runserver
```
should show the admin login page if it is running properly

rest of endpoints are here `http://0.0.0.0:8000/api/v1/<endpoint>`
# my_currency
my_currency
