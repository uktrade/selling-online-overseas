from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
ADMINS = (('David Downes', 'david@downes.co.uk'),)

MIDDLEWARE_CLASSES += [
    'core.middleware.IpRestrictionMiddleware',
]

ip_check = os.environ.get('RESTRICT_IPS', False)
RESTRICT_IPS = ip_check == 'True' or ip_check == '1'

ALLOWED_IPS = []
ALLOWED_IP_RANGES = ['165.225.80.0/22', '193.240.203.32/29', '94.119.64.0/24', '178.208.163.0/24']
