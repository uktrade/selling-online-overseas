from .base import *

DEBUG = False
ALLOWED_HOSTS = [
    'selling-online-overseas.export.great.gov.uk',
    'navigator.cloudapps.digital',
    'navigator.london.cloudapps.digital',
    'www.great.gov.uk']

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Activity Stream API
ACTIVITY_STREAM_ACCESS_KEY_ID = env.str('ACTIVITY_STREAM_ACCESS_KEY_ID')
ACTIVITY_STREAM_SECRET_ACCESS_KEY = env.str('ACTIVITY_STREAM_SECRET_ACCESS_KEY')
