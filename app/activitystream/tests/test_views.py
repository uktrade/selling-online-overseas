import datetime
import math
import environ

import mohawk
import pytest
from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.conf import settings

from markets.tests.factories import PublishedMarketFactory
from activitystream import views

env = environ.Env()

# --- Helper Functions ---


@pytest.fixture
def api_client():
    return APIClient()


def _url():
    return env.str('STATIC_DOMAIN', '') + reverse('activity-stream')


def _url_incorrect_domain():
    return 'http://incorrect' + reverse('activity-stream')


def _url_incorrect_path():
    return (
        env.str('STATIC_DOMAIN', '') + reverse('activity-stream') + 'incorrect/'
    )


def market_attribute(activity, attribute):
    return activity['object'][attribute]


def _empty_collection():
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'type': 'Collection',
        'orderedItems': [],
    }


def _auth_sender(key_id=settings.ACTIVITY_STREAM_ACCESS_KEY_ID,
                 secret_key=settings.ACTIVITY_STREAM_SECRET_ACCESS_KEY,
                 url=_url, method='GET', content='', content_type=''):
    credentials = {
        'id': key_id,
        'key': secret_key,
        'algorithm': 'sha256',
    }

    return mohawk.Sender(
        credentials,
        url(),
        method,
        content=content,
        content_type=content_type,
    )


# --- Authentication tests ---


@pytest.mark.django_db
def test_empty_object_returned_with_authentication(api_client):
    """If the Authorization and X-Forwarded-For headers are correct, then
    the correct, and authentic, data is returned
    """
    sender = _auth_sender()
    response = api_client.get(
        _url(),
        content_type='',
        HTTP_AUTHORIZATION=sender.request_header,
        HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == _empty_collection()

    # sender.accept_response will raise an error if the
    # inputs are not valid
    sender.accept_response(
        response_header=response['Server-Authorization'],
        content=response.content,
        content_type=response['Content-Type'],
    )
    with pytest.raises(mohawk.exc.MacMismatch):
        sender.accept_response(
            response_header=response['Server-Authorization'] + 'incorrect',
            content=response.content,
            content_type=response['Content-Type'],
        )
    with pytest.raises(mohawk.exc.MisComputedContentHash):
        sender.accept_response(
            response_header=response['Server-Authorization'],
            content='incorrect',
            content_type=response['Content-Type'],
        )
    with pytest.raises(mohawk.exc.MisComputedContentHash):
        sender.accept_response(
            response_header=response['Server-Authorization'],
            content=response.content,
            content_type='incorrect',
        )


@pytest.mark.django_db
def test_authentication_fails_if_url_mismatched(api_client):
    """Creates a Hawk header with incorrect domain"""
    sender = _auth_sender(url=_url_incorrect_domain)
    response = api_client.get(
        _url(),
        content_type='',
        HTTP_AUTHORIZATION=sender.request_header,
        HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    """Creates a Hawk header with incorrect path"""
    sender = _auth_sender(url=_url_incorrect_path)
    response = api_client.get(
        _url(),
        content_type='',
        HTTP_AUTHORIZATION=sender.request_header,
        HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_if_61_seconds_in_past_401_returned(api_client):
    """If the Authorization header is generated 61 seconds in the past, then a
    401 is returned
    """
    past = datetime.datetime.now() - datetime.timedelta(seconds=61)
    with freeze_time(past):
        auth = _auth_sender().request_header
    response = api_client.get(
        reverse('activity-stream'),
        content_type='',
        HTTP_AUTHORIZATION=auth,
        HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    error = {'detail': 'Incorrect authentication credentials.'}
    assert response.json() == error


# --- Content tests ---


@pytest.mark.django_db
def test_lists_published_markets_in_stream_in_date_then_seq_order(api_client):

    # Create the market
    with freeze_time('2012-01-14 12:00:02'):
        market_a = PublishedMarketFactory(
            name='eBay', e_marketplace_description='online shop',
            last_modified=datetime.datetime.now(), slug='ebay')

    with freeze_time('2012-01-14 12:00:02'):
        market_b = PublishedMarketFactory(
            name='Amazon', e_marketplace_description='online shop',
            last_modified=datetime.datetime.now(), slug='amazon')

    with freeze_time('2012-01-14 12:00:01'):
        market_c = PublishedMarketFactory(
            name='Alibaba', e_marketplace_description='online shop',
            last_modified=datetime.datetime.now(), slug='alibaba')

    sender = _auth_sender()
    response = api_client.get(
        _url(),
        content_type='',
        HTTP_AUTHORIZATION=sender.request_header,
        HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
    )
    items = response.json()['orderedItems']

    id_prefix = 'dit:navigator:Market:'

    assert len(items) == 3
    assert items[0]['published'] == '2012-01-14T12:00:01+00:00'
    assert market_attribute(items[0], 'name') == 'Alibaba'
    assert market_attribute(items[0], 'id') == id_prefix + str(market_c.id)
    assert market_attribute(items[0], 'content') == 'online shop'
    assert market_attribute(items[0], 'url') == 'http://testserver/selling-online-overseas/markets/details/alibaba/'
    assert items[1]['published'] == '2012-01-14T12:00:02+00:00'
    assert market_attribute(items[1], 'name') == 'eBay'
    assert market_attribute(items[1], 'id') == id_prefix + str(market_a.id)
    assert items[2]['published'] == '2012-01-14T12:00:02+00:00'
    assert market_attribute(items[2], 'name') == 'Amazon'
    assert market_attribute(items[2], 'id') == id_prefix + str(market_b.id)


@pytest.mark.django_db
def test_pagination(api_client, django_assert_num_queries):
    """The requests are paginated, ending on a page without a next key
    """

    with freeze_time('2012-01-14 12:00:02'):
        for i in range(0, 250):
            PublishedMarketFactory(
                name='market_' + str(i), e_marketplace_description='online shop',
                last_modified=datetime.datetime.now())

    with freeze_time('2012-01-14 12:00:01'):
        for i in range(250, 501):
            PublishedMarketFactory(
                name='market_' + str(i), e_marketplace_description='online shop',
                last_modified=datetime.datetime.now())

    items = []
    next_url = _url()
    num_pages = 0

    queries = math.ceil(500 / views.MAX_PER_PAGE) + 2

    with django_assert_num_queries(queries):
        while next_url:
            num_pages += 1
            sender = _auth_sender(url=lambda: next_url)
            response = api_client.get(
                next_url,
                content_type='',
                HTTP_AUTHORIZATION=sender.request_header,
                HTTP_X_FORWARDED_FOR='1.2.3.4, 123.123.123.123',
            )
            response_json = response.json()
            items += response_json['orderedItems']
            next_url = \
                response_json['next'] if 'next' in response_json else \
                None

    assert num_pages == queries
    assert len(items) == 501
    assert len(set([item['id'] for item in items])) == 501
    assert market_attribute(items[500], 'name') == 'market_249'
