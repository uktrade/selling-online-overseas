from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']
ADMINS = (('David Downes', 'david@downes.co.uk'),)

RESTRICT_IPS = True
ALLOWED_IPS = ['127.0.0.1', '2a02:c7f:763d:c900:20ea:3f49:412e:4dcb']
ALLOWED_IP_RANGES = ['165.225.80.0/22', '193.240.203.32/29']
BLOCKED_IPS = []
BLOCKED_IP_RANGES = []
