import ipaddress
import logging

from django.conf import settings
from django import http
from django.core.urlresolvers import resolve

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
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    def process_request(self, request):
        if getattr(settings, 'RESTRICT_IPS', False):
            # Get the app name
            app_name = resolve(request.path).app_name
            authenticated = request.user.is_authenticated()

            # Allow access to the admin
            if app_name == 'admin' or authenticated:
                return None

            block_request = True
            # Get the incoming IP address
            request_ip_str = self.get_client_ip(request)
            request_ip = ipaddress.ip_address(request_ip_str)

            # If it's in the ALLOWED_IPS, don't block it
            if request_ip_str in settings.ALLOWED_IPS:
                block_request = False

            # If it's within a ALLOWED_IP_RANGE, don't block it
            for allowed_range in settings.ALLOWED_IP_RANGES:
                if request_ip in ipaddress.ip_network(allowed_range):
                    block_request = False
                    break

            # Otherwise, 403 Forbidden
            if block_request:
                return http.HttpResponseForbidden('<h1>Forbidden</h1>')

        return None
