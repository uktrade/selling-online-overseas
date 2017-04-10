release: python manage.py migrate --noinput
web: python manage.py build_index && gunicorn navigator.wsgi
