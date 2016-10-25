from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

WHOOSH_INDEX_DIR = os.path.join(BASE_DIR, 'whoosh_index_test')
