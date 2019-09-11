from directory_constants import urls
from django.conf import settings


def hosts(request):
    hosts = {
        'PROFILE_HOST': settings.PROFILE_HOST
    }

    return hosts
