release: python manage.py migrate --noinput
web: gunicorn --workers=3 --thread=2 demo.app.wsgi:application
