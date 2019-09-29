release: python manage.py migrate --noinput
web: gunicorn --thread=1 demo.app.wsgi:application
