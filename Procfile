web: cd app && python3 ./manage.py migrate && python3 ./manage.py build_index && python3 ./manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:$PORT navigator.wsgi:application
