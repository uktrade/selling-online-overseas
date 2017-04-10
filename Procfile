release: python manage.py migrate --noinput && python manage.py build_index
web: gunicorn navigator.wsgi
