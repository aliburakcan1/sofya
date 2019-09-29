release: python manage.py migrate --noinput
web: gunicorn --workers=1 --thread=1 demo.app.wsgi:application
