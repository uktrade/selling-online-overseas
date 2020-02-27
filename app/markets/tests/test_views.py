from unittest.mock import patch, Mock
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import PublishedMarket
from . import create_market


class MarketViewsTests(TestCase):

    def setUp(self):
        market = create_market()
        market.publish()
        published_market = PublishedMarket.objects.get(id=market.id)
        self.market = published_market

    def tearDown(self):
        self.market.delete()

    def test_market_homepage(self):
        with patch('directory_cms_client.client.cms_api_client') as cms_client:
            cms_client.return_value = Mock(**{'lookup_by_slug.return_value': {
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
            }})
            response = self.client.get(reverse('home'))
            self.assertEqual(response.status_code, 200)

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
