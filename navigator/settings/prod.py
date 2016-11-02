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
ALLOWED_IP_RANGES = ['165.225.80.0/22', '193.240.203.32/29', '94.119.64.0/24', '178.208.163.0/24']

SECURE_SSL_REDIRECT = True
