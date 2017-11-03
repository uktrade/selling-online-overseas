from django.conf import settings


def hosts(request):
    hosts = {
        'SOO_HOST': settings.SOO_HOST,
        'HELP_HOST': settings.HELP_HOST,
        'SSO_HOST': settings.SSO_HOST,
        'PROFILE_HOST': settings.PROFILE_HOST
    }

    return hosts
