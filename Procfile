web: gunicorn config.wsgi:application
worker: celery worker --app=wild_bills.taskapp --loglevel=info
