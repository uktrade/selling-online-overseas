from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*.herokuapp.com']

WHOOSH_INDEX_DIR = os.path.join(BASE_DIR, 'whoosh_index_test')
