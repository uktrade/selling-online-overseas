from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from ..models import PublishedMarket
from . import create_market, create_country


class MarketPublishingTests(TestCase):

    def setUp(self):
        self.market = create_market()

    def tearDown(self):
        self.market.delete()

    def _publish_market(self):
        self.market.publish()
        published_market = PublishedMarket.objects.get(id=self.market.id)
        self.market = published_market

    def test_list_markets(self):
        response = self.client.get(reverse('markets:list'))
        self.assertNotContains(response, self.market.name, status_code=200)
        markets = response.context_data['market_list']
        self.assertEqual(len(markets), 0)

        self._publish_market()

        response = self.client.get(reverse('markets:list'))
        self.assertContains(response, self.market.name, status_code=200)
        markets = response.context_data['market_list']
        self.assertEqual(len(markets), 1)
        self.assertEqual(markets[0], self.market)

        paginator = response.context_data['pagination_page']
        self.assertEqual(paginator.paginator.per_page, 6)
        self.assertEqual(paginator.paginator.object_list, markets)

    # TODO: remove
    def _test_filter_market_list_by_name(self):

        # Filter the list of markets on it's name, check we get 200 and the market in the response
        response = self.client.get(reverse('markets:list'), {'name': self.market.name})
        markets = response.context_data['market_list']
        self.assertNotIn(self.market, markets)

        self._publish_market()

        response = self.client.get(reverse('markets:list'), {'name': self.market.name})
        markets = response.context_data['market_list']
        self.assertIn(self.market, markets)

        # Search for an incorrect name, check we get 200 and NOT the market we created
        response = self.client.get(reverse('markets:list'), {'name': "Amazing"})
        markets = response.context_data['market_list']
        self.assertNotIn(self.market, markets)

    def test_count_markets(self):
        response = self.client.get(reverse('markets:count'))
        json = response.json()
        self.assertEqual(json['count'], 0)

        self._publish_market()

        response = self.client.get(reverse('markets:count'))
        json = response.json()
        self.assertEqual(json['count'], 1)

    def test_market_detail_404(self):
        response = self.client.get(reverse('markets:detail', kwargs={'slug': self.market.slug}))
        self.assertEqual(response.status_code, 404)

        self._publish_market()

        # Search for an incorrect name, check we get 200 and NOT the market we created
        response = self.client.get(reverse('markets:detail', kwargs={'slug': self.market.slug}))
        self.assertContains(response, self.market.name, status_code=200)

    def test_market_detail_united_kingdom_not_a_valid_option(self):
        self._publish_market()
        create_country('United Kingdom')
        response = self.client.get(reverse('markets:detail', kwargs={'slug': self.market.slug}))
        self.assertNotContains(response, 'United Kingdom', status_code=200)


class MarketTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = 'testuser'
        cls.password = '12345'
        cls.user = User.objects.create(username=cls.username)
        cls.user.set_password('12345')
        cls.user.is_superuser = True
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(username=self.user.username, password=self.password)

    def tearDown(self):
        self.client.logout()

    # FIXME: put filter functionality here
    def test_list_markets(self):
        market = create_market()
        response = self.client.get(reverse('markets:list'))
        self.assertContains(response, market.name, status_code=200)
        markets = response.context_data['market_list']
        self.assertEqual(len(markets), 1)
        self.assertEqual(markets[0], market)

    def test_market_detail_page(self):
        create_market(
            name="Ebay",
            product_exclusivity_required=False,
            sale_to_payment_duration=30)

        url = reverse('markets:detail', kwargs={'slug': 'ebay'})
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.context_data['page_type'] == 'MarketplacePage'
        assert 'Go directly to marketplace' not in str(response.content)
        assert 'Apply now' in str(response.content)

    def test_market_list_page(self):
        create_market(
            name="Ebay",
            product_exclusivity_required=False,
            sale_to_payment_duration=30)

        response = self.client.get(reverse('markets:list'))

        assert response.status_code == 200
        assert response.context_data['page_type'] == 'SearchResultsPage'
        assert 'Ebay' in str(response.content)

    def test_market_list_united_kingdom_not_a_valid_option(self):
        create_country('United Kingdom')
        response = self.client.get(reverse('markets:list'))
        self.assertNotContains(response, 'United Kingdom', status_code=200)
