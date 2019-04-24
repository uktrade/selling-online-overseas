from datetime import datetime
import logging

from django.db.models import Q
from django.conf import settings
from django.core.cache import cache
from django.utils.crypto import constant_time_compare
from django.utils.decorators import decorator_from_middleware

from mohawk import Receiver
from mohawk.exc import HawkFail
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet

from markets.models import PublishedMarket

logger = logging.getLogger(__name__)

NO_CREDENTIALS_MESSAGE = 'Authentication credentials were not provided.'
INCORRECT_CREDENTIALS_MESSAGE = 'Incorrect authentication credentials.'
MAX_PER_PAGE = 250

# --- Hawk Authorisation Helper Functions ---


def lookup_credentials(access_key_id):
    """Raises a HawkFail if the passed ID is not equal to
    settings.ACTIVITY_STREAM_ACCESS_KEY_ID
    """
    if not constant_time_compare(access_key_id,
                                 settings.ACTIVITY_STREAM_ACCESS_KEY_ID):
        raise HawkFail('No Hawk ID of {access_key_id}'.format(
            access_key_id=access_key_id,
        ))

    return {
        'id': settings.ACTIVITY_STREAM_ACCESS_KEY_ID,
        'key': settings.ACTIVITY_STREAM_SECRET_ACCESS_KEY,
        'algorithm': 'sha256',
    }


def seen_nonce(access_key_id, nonce, _):
    """Returns if the passed access_key_id/nonce combination has been
    used within 60 seconds
    """
    cache_key = 'activity_stream:{access_key_id}:{nonce}'.format(
        access_key_id=access_key_id,
        nonce=nonce,
    )

    # cache.add only adds key if it isn't present
    seen_cache_key = not cache.add(
        cache_key, True, timeout=60,
    )

    if seen_cache_key:
        logger.warning('Already seen nonce {nonce}'.format(nonce=nonce))

    return seen_cache_key


def authorise(request):
    """Raises a HawkFail if the passed request cannot be authenticated"""
    return Receiver(
        lookup_credentials,
        request.META['HTTP_AUTHORIZATION'],
        request.build_absolute_uri(),
        request.method,
        content=request.body,
        content_type=request.content_type,
        seen_nonce=seen_nonce,
    )


# --- Hawk Authorisation Middleware ---


class ActivityStreamAuthentication(BaseAuthentication):

    def authenticate_header(self, request):
        """This is returned as the WWW-Authenticate header when
        AuthenticationFailed is raised. DRF also requires this
        to send a 401 (as opposed to 403)
        """
        return 'Hawk'

    def authenticate(self, request):
        """Authenticates a request using Hawk signature

        If either of these suggest we cannot authenticate, AuthenticationFailed
        is raised, as required in the DRF authentication flow
        """

        return self.authenticate_by_hawk(request)

    def authenticate_by_hawk(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            raise AuthenticationFailed(NO_CREDENTIALS_MESSAGE)

        try:
            hawk_receiver = authorise(request)
        except HawkFail as e:
            logger.warning('Failed authentication {e}'.format(e=e))
            raise AuthenticationFailed(INCORRECT_CREDENTIALS_MESSAGE)

        return (None, hawk_receiver)


class ActivityStreamHawkResponseMiddleware:
    """Adds the Server-Authorization header to the response, so the originator
    of the request can authenticate the response
    """

    def process_response(self, viewset, response):
        response['Server-Authorization'] = viewset.request.auth.respond(
            content=response.content,
            content_type=response['Content-Type'],
        )
        return response


# --- Activity Stream Business Logic ---


class ActivityStreamViewSet(ViewSet):
    """List-only view set for the activity stream"""

    authentication_classes = (ActivityStreamAuthentication,)
    permission_classes = ()

    @staticmethod
    def _parse_after(request):
        after = request.GET.get('after', '0.000000_0')
        after_ts_str, after_id_str = after.split('_')
        after_ts = datetime.fromtimestamp(float(after_ts_str))
        after_id = int(after_id_str)
        return after_ts, after_id

    @staticmethod
    def _build_after(request, after_ts, after_id):
        return (
            request.build_absolute_uri(
                reverse('activity-stream')
            ) + '?after={}_{}'.format(
                str(after_ts.timestamp()),
                str(after_id)
            )
        )

    @staticmethod
    def _build_market_objects(request, markets):
        market_objects = []
        for market in markets:
            market_objects.append({
                'id': (
                    'dit:navigator:Market:' + str(market.id) + ':Create'
                ),
                'type': 'Create',
                'published': market.last_modified.isoformat('T'),
                'object': {
                    'type': 'Market',
                    'dit:greatDomesticUI:searchResultType': 'Market',
                    'id': 'dit:navigator:Market:' + str(market.id),
                    'name': market.name,
                    'content': market.e_marketplace_description,
                    'url': request.build_absolute_uri(reverse('markets:detail', kwargs={'slug': market.slug}))
                },
            })
        return market_objects

    @decorator_from_middleware(ActivityStreamHawkResponseMiddleware)
    def list(self, request):
        """A single page of activities"""
        after_ts, after_id = self._parse_after(request)
        market_qs_all = PublishedMarket.objects.filter(
            Q(last_modified=after_ts, id__gt=after_id) | Q(last_modified__gt=after_ts)
        ).order_by('last_modified', 'id')

        market_qs = market_qs_all[:MAX_PER_PAGE]
        markets = list(market_qs)
        market_objects = self._build_market_objects(request, markets)

        items = {
            '@context': 'https://www.w3.org/ns/activitystreams',
            'type': 'Collection',
            'orderedItems': market_objects
        }

        if markets:
            next_page = {
                'next': self._build_after(request, markets[-1].last_modified,
                                          markets[-1].id)
            }
        else:
            next_page = {}

        return Response({
            **items,
            **next_page,
        })
