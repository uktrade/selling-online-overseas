from .base import *

DEBUG = False

ALLOWED_HOSTS = ['selling-online-overseas.export.staging.uktrade.io',
                 'dit-navigator-staging.herokuapp.com',
                 'navigator-staging.cloudapps.digital',
                 'enav-navigator-dev.cloudapps.digital',
                 'navigator-dev.london.cloudapps.digital',
                 'navigator-uat.london.cloudapps.digital',
                 'navigator-staging.london.cloudapps.digital']

ADMINS = (('David Downes', 'david@downes.co.uk'),)

RESTRICT_IPS = True
ALLOW_AUTHENTICATED = True
ALLOW_ADMIN = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
