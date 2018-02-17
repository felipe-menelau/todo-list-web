# README #

TODO List Web backend.

Running on Python 3.6 and Django 2.0

## Development ##

Clone the repository and make sure you have **pipenv** and **pyenv** installed

```
pip install pipenv pyenv
```

Make sure you have a running **Postgres** in your machine 

Then install every dependency

```
pipenv install
```

Activate the virtualenv

```
pipenv shell
```

Copy and rename *.env.exemple* to *.env*, edit your new *.env* filling all the empty fields, including the DB fields and allowed hosts (usually 0.0.0.0 for development)

Apply all migrations with

```
python manage.py migrate
```

To run tests do

```
python manage.py test
```

To run the server in development do
```
python manage.py runserver 0.0.0.0:8000 
```

## Production ##

To deploy with Heroku create a new branch called production, refer to [heroku documentation](https://devcenter.heroku.com/articles/deploying-python)

```
git checkout -b production
```

Tweak the .env file and settings.py file to fit the production enviroment, then commit changes to the production branch **DO NOT PUSH THEM TO REMOTE**
```
git add .
git commit -m "Production ready"
```

Push changes to your heroku app
```
git push heroku production:master
```

Make migrations and migrate
```
heroku run python manage.py makemigrations
heroku run python manage.py migrate 
```

You're done! You can find the api at apiary

## LICENSE ##

Todo list web runs under (MIT License)[https://opensource.org/licenses/MIT]
