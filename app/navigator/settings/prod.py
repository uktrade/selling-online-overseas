from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    'selling-online-overseas.export.great.gov.uk',
    'navigator.cloudapps.digital']
ADMINS = (('David Downes', 'david@downes.co.uk'),)

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Activity Stream API - to be set
ACTIVITY_STREAM_ACCESS_KEY_ID="access-key-123"
ACTIVITY_STREAM_SECRET_ACCESS_KEY="secret-key-123"