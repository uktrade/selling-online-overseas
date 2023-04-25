from django.conf import settings


def hosts(request):
    hosts = {
        'PROFILE_HOST': settings.PROFILE_HOST
    }

    return hosts


def magna_header(request):
    return {
        'magna_header': settings.MAGNA_HEADER
    }
