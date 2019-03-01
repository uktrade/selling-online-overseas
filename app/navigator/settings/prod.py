from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    'selling-online-overseas.export.great.gov.uk',
    'navigator.cloudapps.digital',
    'navigator.london.cloudapps.digital']

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
