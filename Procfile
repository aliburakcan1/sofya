release: python manage.py migrate --noinput
web: gunicorn --thread=2 demo.app.wsgi:application
