from .base import *

DEBUG = False

ALLOWED_HOSTS = ['selling-online-overseas.export.staging.uktrade.io',
                 'selling-online-overseas.export.great.staging.uktrade.io',
                 'selling-online-overseas.export.great.uat.uktrade.io',
                 'selling-online-overseas.export.great.dev.uktrade.io',
                 'great.dev.uktrade.io',
                 'great.staging.uktrade.io',
                 'great.uat.uktrade.io',
                 'great.dev.uktrade.digital',
                 'great.staging.uktrade.digital',
                 'great.uat.uktrade.digital',
                 'great-magna.dev.uktrade.digital',
                 'great-magna.staging.uktrade.digital',
                 'great-magna.uat.uktrade.digital',
                 'navigator-dev.london.cloudapps.digital',
                 'navigator-uat.london.cloudapps.digital',
                 'navigator-staging.london.cloudapps.digital']

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat'
]

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
