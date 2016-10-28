from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']
ADMINS = (('David Downes', 'david@downes.co.uk'),)

RESTRICT_IPS = True
ALLOWED_IPS = ['127.0.0.1', '94.119.64.50']
ALLOWED_IP_RANGES = ['165.225.80.0/22', '193.240.203.32/29', '94.119.64.0/24', '178.208.163.0/24']
BLOCKED_IPS = []
BLOCKED_IP_RANGES = []
