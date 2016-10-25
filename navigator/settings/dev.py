from .base import *

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]
