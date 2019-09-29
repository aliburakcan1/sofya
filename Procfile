release: python manage.py migrate --noinput
web: gunicorn --worker=1 --thread=1 demo.app.wsgi:application
