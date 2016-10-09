Deploy
========

This is where you describe how the project is deployed in production.


Heroku
^^^^^^^

First time you create the site

::

    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:backups schedule --at '02:00 America/Panama' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:hobby-dev

    heroku addons:create mailgun

    heroku config:set DJANGO_ADMIN_URL="$(openssl rand -base64 32)"
    heroku config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)"
    heroku config:set DJANGO_SETTINGS_MODULE='config.settings.production'
    heroku config:set DJANGO_ALLOWED_HOSTS='.herokuapp.com'

    heroku config:set DJANGO_MAILGUN_SERVER_NAME=YOUR_MALGUN_SERVER
    heroku config:set DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY
    heroku config:set MAILGUN_SENDER_DOMAIN=YOUR_MAILGUN_SENDER_DOMAIN

    heroku config:set PYTHONHASHSEED=random
    heroku config:set DJANGO_ADMIN_URL=\^somelocation/

    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open

After the first deploy::

    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
