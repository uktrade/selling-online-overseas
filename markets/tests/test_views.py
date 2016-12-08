from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from . import create_market, create_country


class MarketPublishingTests(TestCase):

    def setUp(self):
        self.market = create_market()

    def tearDown(self):
        self.market.delete()

    def _publish_market(self):
        self.market.published = True
        self.market.save()

    def test_list_markets(self):
        response = self.client.get(reverse('markets:list'))
        self.assertNotContains(response, self.market.name, status_code=200)
        markets = response.context_data['object_list']
        self.assertEqual(len(markets), 0)

        self._publish_market()

        response = self.client.get(reverse('markets:list'))
        self.assertContains(response, self.market.name, status_code=200)
        markets = response.context_data['object_list']
        self.assertEqual(len(markets), 1)
        self.assertEqual(markets[0], self.market)

    def test_filter_market_list_by_name(self):
        # Filter the list of markets on it's name, check we get 200 and the market in the response
        response = self.client.get(reverse('markets:list'), {'name': self.market.name})
        self.assertNotContains(response, self.market.name, status_code=200)

        self._publish_market()

        # Search for an incorrect name, check we get 200 and NOT the market we created
        response = self.client.get(reverse('markets:list'), {'name': "Amazing"})
        self.assertNotContains(response, self.market.name, status_code=200)

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
        self.assertEquals(response.status_code, 404)

        self._publish_market()

        # Search for an incorrect name, check we get 200 and NOT the market we created
        response = self.client.get(reverse('markets:detail', kwargs={'slug': self.market.slug}))
        self.assertContains(response, self.market.name, status_code=200)


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

    def test_list_markets(self):
        market = create_market()
        response = self.client.get(reverse('markets:list'))
        self.assertContains(response, market.name, status_code=200)
        markets = response.context_data['object_list']
        self.assertEqual(len(markets), 1)
        self.assertEqual(markets[0], market)

    def test_filter_market_list_by_name(self):
        # Create a market with a known name
        market = create_market(name="Amazon")

        # Filter the list of markets on it's name, check we get 200 and the market in the response
        response = self.client.get(reverse('markets:list'), {'name': market.name})
        self.assertContains(response, market.name, status_code=200)

        # Search for an incorrect name, check we get 200 and NOT the market we created
        response = self.client.get(reverse('markets:list'), {'name': "Amazing"})
        self.assertNotContains(response, market.name, status_code=200)

    def test_filter_market_list_by_related_property(self):
        # Create 2 markets with a specific countries
        uk = create_country('uk')
        fr = create_country('france')
        amazon = create_market(name="Amazon", countries_served=[uk])
        ebay = create_market(name="Ebay", countries_served=[uk, fr])

        # Filter the list of markets on country is uk, and check we get both markets
        response = self.client.get(reverse('markets:list'), {'countries_served': 'uk'})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Filter on country name is france, and check we get ebay, but not amazon
        response = self.client.get(reverse('markets:list'), {'countries_served': 'france'})
        self.assertNotContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Filter on an incorrect country name, we should get neither market
        response = self.client.get(reverse('markets:list'), {'countries_served': 'us'})
        self.assertNotContains(response, amazon.name, status_code=200)
        self.assertNotContains(response, ebay.name, status_code=200)

    def test_filter_market_list_complex(self):
        # Create 2 markets with a specific countries
        uk = create_country('uk')
        fr = create_country('france')
        amazon = create_market(name="Amazon", countries_served=[uk])
        ebay = create_market(name="Ebay", countries_served=[uk, fr])

        # Filter on a list of names, including an incorrect name, we should get back both markets
        response = self.client.get(reverse('markets:list'), {'name': ['Amazon', 'Ebay', 'Blah']})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Passing a GET arg of '*' should not filter results
        response = self.client.get(reverse('markets:list'), {'name': '*'})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Filter for both countries, and make sure we don't get duplicates
        response = self.client.get(reverse('markets:list'), {'countries_served': ['uk', 'france']})
        markets = response.context_data['object_list']
        self.assertEqual(len(markets), 2)
        self.assertIn(amazon, markets)
        self.assertIn(ebay, markets)

        # Filtering for a list including '*' does not return all, but the '*' simply gets ignored
        response = self.client.get(reverse('markets:list'), {'name': ['*', 'Amazon']})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertNotContains(response, ebay.name, status_code=200)

    def test_filter_market_list_non_string_types(self):
        """
        The form filtering should correctly infer the types of arguments passed, converting to ints, booleans, etc
        as necessary
        """

        amazon = create_market(name="Amazon", local_bank_account_needed=True, payment_terms_days=15)
        ebay = create_market(name="Ebay", local_bank_account_needed=False, payment_terms_days=30)

        # Filter for local_bank_account_needed True, we shoudl get back only Amazon
        response = self.client.get(reverse('markets:list'), {'local_bank_account_needed': True})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertNotContains(response, ebay.name, status_code=200)

        # Filtering using a string shoudl work the same, since True/False would be converted to 'True'/'False' in the
        # get request anyway, check that 'False' therefore only returns ebay
        response = self.client.get(reverse('markets:list'), {'local_bank_account_needed': 'False'})
        self.assertNotContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # We should be able to pass a list of these values, and get back both
        response = self.client.get(reverse('markets:list'), {'local_bank_account_needed': ['True', 'False']})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Perform the same tests with numbers
        response = self.client.get(reverse('markets:list'), {'payment_terms_days': 15})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertNotContains(response, ebay.name, status_code=200)

        response = self.client.get(reverse('markets:list'), {'payment_terms_days': '30'})
        self.assertNotContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        response = self.client.get(reverse('markets:list'), {'payment_terms_days': ['15', 30]})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)
