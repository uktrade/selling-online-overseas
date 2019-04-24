from directory_constants.constants import urls
from django.conf import settings


def hosts(request):
    hosts = {
        'SOO_HOST': urls.SERVICES_SOO,
        'HELP_HOST': urls.CONTACT_US,
        'SSO_HOST': urls.SERVICES_SSO,
        'SERVICES_GREAT_DOMESTIC': urls.SERVICES_GREAT_DOMESTIC,
        'PROFILE_HOST': settings.PROFILE_HOST
    }

    return hosts
