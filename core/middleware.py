import ipaddress

from django.conf import settings
from django import http


class IpRestrictionMiddleware(object):
    """
    Simple middlware to allow and/or block IP addresses via settings variables ALLOWED_IPS, ALLOWED_IP_RANGES,
    BLOCKED_IPS, and BLOCKED_IP_RANGES.

    The settings must have RESTRICT_IPS = True for IP checking to perform, else the middlware does nothing.
    """

    def process_request(self, request):
        if getattr(settings, 'RESTRICT_IPS', False):
            if request.META['REMOTE_ADDR'] not in settings.ALLOWED_IPS:
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')
            if request.META['REMOTE_ADDR'] in settings.BLOCKED_IPS:
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')

            request_ip = ipaddress.ip_address(request.META['REMOTE_ADDR'])

            for allowed_range in ALLOWED_IP_RANGES:
                if request_ip not in ipaddress.ip_network(allowed_range):
                    return http.HttpResponseForbidden('<h1>Forbidden</h1>')

            for blocked_range in BLOCKED_IP_RANGES:
                if request_ip in ipaddress.ip_network(blocked_range):
                    return http.HttpResponseForbidden('<h1>Forbidden</h1>')

        return None
