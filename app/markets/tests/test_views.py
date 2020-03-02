import pytest
from unittest import mock
import requests
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import PublishedMarket
from . import create_market


def _create_response(json_body={}, status_code=200, content=None):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_body
    response._content = content
    return response


@pytest.mark.django_db
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_homepage(mock_cms_page, client):
    mock_cms_page.return_value = _create_response({'featured_case_studies': []})
    response = client.get(reverse('home'))

    assert response.status_code == 200
    assert response.context_data['page_type'] == 'LandingPage'
    assert 'Selling online overseas' in str(response.content)


@pytest.mark.django_db
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_homepage_case_studies_cms(mock_cms_page, client):
    mock_cms_page.return_value = _create_response({
        'featured_case_studies': [
            {
                'meta': {'slug': 'the-slug-one'},
                'hero_image_thumbnail': {'url': 'hero.png'},
                'title': 'Title one',
                'teaser': 'Lorem ipsum one',
            },
            {
                'meta': {'slug': 'the-slug-two'},
                'hero_image_thumbnail': {'url': 'hero.png'},
                'title': 'Title two',
                'teaser': 'Lorem ipsum two',
            },
        ]
    })

    response = client.get(reverse('home'))

    assert response.status_code == 200
    assert 'Title one' in str(response.content)
    assert 'Title two' in str(response.content)


@pytest.mark.django_db
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_homepage_case_studies_cms_404(mock_cms_page, client):
    mock_cms_page.return_value = _create_response(status_code=404)

    response = client.get(reverse('home'))

    assert response.status_code == 200


class MarketViewsTests(TestCase):

    def setUp(self):
        market = create_market()
        market.publish()
        published_market = PublishedMarket.objects.get(id=market.id)
        self.market = published_market

    def tearDown(self):
        self.market.delete()

    def test_market_list(self):
        response = self.client.get(reverse('markets:list'))
        self.assertContains(response, self.market.name, status_code=200)
        markets = response.context_data['market_list']
        self.assertEqual(len(markets), 1)
        self.assertEqual(markets[0], self.market)

        paginator = response.context_data['pagination_page']
        self.assertEqual(paginator.paginator.per_page, 6)
        self.assertEqual(paginator.paginator.object_list, markets)

    def test_market_detail_page(self):
        response = self.client.get(reverse('markets:detail', kwargs={'slug': 'amazon'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['page_type'], 'MarketplacePage')

    def test_markets_detail_404(self):
        response = self.client.get(reverse('markets:detail', kwargs={'slug': 'does_not_exist'}))
        self.assertEqual(response.status_code, 404)
