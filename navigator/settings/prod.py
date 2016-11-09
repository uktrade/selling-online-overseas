from .base import *

DEBUG = False
ALLOWED_HOSTS = ['selling-online-overseas.export.great.gov.uk']
ADMINS = (('David Downes', 'david@downes.co.uk'),)

MIDDLEWARE_CLASSES += [
    'core.middleware.IpRestrictionMiddleware',
]

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

ip_check = os.environ.get('RESTRICT_IPS', False)
RESTRICT_IPS = ip_check == 'True' or ip_check == '1'

ALLOWED_IPS = []
ALLOWED_IP_RANGES = ['165.225.80.0/22', '193.240.203.32/29']

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
