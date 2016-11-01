import ipaddress
import logging

from django.conf import settings
from django import http

logger = logging.getLogger(__name__)


class IpRestrictionMiddleware(object):
    """
    Simple middlware to allow and/or block IP addresses via settings variables ALLOWED_IPS, ALLOWED_IP_RANGES,
    BLOCKED_IPS, and BLOCKED_IP_RANGES.  Blocked IPs or ranges trump allowed ones.

    The settings must have RESTRICT_IPS = True for IP checking to perform, else the middlware does nothing.
    """

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip.strip()

    def process_request(self, request):
        if getattr(settings, 'RESTRICT_IPS', False):
            block_request = True

            request_ip_str = self.get_client_ip(request)
            request_ip = ipaddress.ip_address(request_ip_str)

            if request_ip_str in settings.ALLOWED_IPS:
                block_request = False

            for allowed_range in settings.ALLOWED_IP_RANGES:
                if request_ip in ipaddress.ip_network(allowed_range):
                    block_request = False
                    break

            if block_request:
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')

        return None
