release: python manage.py migrate --noinput
web: gunicorn --workers=3 demo.app.wsgi:application
