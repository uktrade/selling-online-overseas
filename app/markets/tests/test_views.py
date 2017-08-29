from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

from ..models import Market, PublishedMarket
from . import create_market, create_country, create_category, get_market_data


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
        markets = response.context_data['markets_list']
        self.assertNotIn(self.market, markets)

        self._publish_market()

        response = self.client.get(reverse('markets:list'), {'name': self.market.name})
        markets = response.context_data['markets_list']
        self.assertIn(self.market, markets)

        # Search for an incorrect name, check we get 200 and NOT the market we created
        response = self.client.get(reverse('markets:list'), {'name': "Amazing"})
        markets = response.context_data['markets_list']
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
        amazon = create_market(name="Amazon", operating_countries=[uk])
        ebay = create_market(name="Ebay", operating_countries=[uk, fr])

        # Filter the list of markets on country is uk, and check we get both markets
        response = self.client.get(reverse('markets:list'), {'operating_countries': 'uk'})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Filter on country name is france, and check we get ebay, but not amazon
        response = self.client.get(reverse('markets:list'), {'operating_countries': 'france'})
        self.assertNotContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Filter on an incorrect country name, we should get neither market
        response = self.client.get(reverse('markets:list'), {'operating_countries': 'us'})
        self.assertNotContains(response, amazon.name, status_code=200)
        self.assertNotContains(response, ebay.name, status_code=200)

    def test_filter_market_list_complex(self):
        # Create 2 markets with a specific countries
        uk = create_country('uk')
        fr = create_country('france')
        amazon = create_market(name="Amazon", operating_countries=[uk])
        ebay = create_market(name="Ebay", operating_countries=[uk, fr])

        # Filter on a list of names, including an incorrect name, we should get back both markets
        response = self.client.get(reverse('markets:list'), {'name': ['Amazon', 'Ebay', 'Blah']})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Passing a GET arg of '*' should not filter results
        response = self.client.get(reverse('markets:list'), {'name': '*'})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Filter for both countries, and make sure we don't get duplicates
        response = self.client.get(reverse('markets:list'), {'operating_countries': ['uk', 'france']})
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

        amazon = create_market(name="Amazon", product_exclusivity_required=True, sale_to_payment_duration=15)
        ebay = create_market(name="Ebay", product_exclusivity_required=False, sale_to_payment_duration=30)

        # Filter for payment_terms_rate_fixed True, we shoudl get back only Amazon
        response = self.client.get(reverse('markets:list'), {'product_exclusivity_required': True})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertNotContains(response, ebay.name, status_code=200)

        # Filtering using a string shoudl work the same, since True/False would be converted to 'True'/'False' in the
        # get request anyway, check that 'False' therefore only returns ebay
        response = self.client.get(reverse('markets:list'), {'product_exclusivity_required': 'False'})
        self.assertNotContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # We should be able to pass a list of these values, and get back both
        response = self.client.get(reverse('markets:list'), {'product_exclusivity_required': ['True', 'False']})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Perform the same tests with numbers
        response = self.client.get(reverse('markets:list'), {'sale_to_payment_duration': 15})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertNotContains(response, ebay.name, status_code=200)

        response = self.client.get(reverse('markets:list'), {'sale_to_payment_duration': '30'})
        self.assertNotContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        response = self.client.get(reverse('markets:list'), {'sale_to_payment_duration': ['15', 30]})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

    def test_market_ordering(self):
        # Create some countries and some categories
        uk = create_country('uk')
        fr = create_country('france')
        de = create_country('germany')
        sport = create_category('sport')
        food = create_category('food')

        # Create 4 markets with differing numbers of countries and categories
        country_vertical = create_market(operating_countries=[uk], product_categories=[sport])
        global_vertical = create_market(operating_countries=[uk, fr, de], product_categories=[sport])
        country_generalist = create_market(operating_countries=[uk], product_categories=[sport, food])
        global_generalist = create_market(operating_countries=[uk, fr, de], product_categories=[sport, food])

        # Searching one category and one country should return all markets with those items
        # But ordered by country-specific vertical first
        _filter = {'operating_countries': ['uk'], 'product_categories': ['sport']}
        response = self.client.get(reverse('markets:list'), _filter)
        markets = response.context_data['object_list']

        # Country vertical should be first - perfect match on both terms
        self.assertEqual(markets[0], country_vertical)
        # ... then country generalist - since there are more countries than categories, meaning the global is de-ranked
        self.assertEqual(markets[1], country_generalist)
        # ... then the global vertical - since it matches perfectly on category but loosely on country
        self.assertEqual(markets[2], global_vertical)
        # ... finally the global generalist - since it matches loosley on both
        self.assertEqual(markets[3], global_generalist)

        # Searching on only category should bring the globals back first
        _filter = {'product_categories': ['sport']}
        response = self.client.get(reverse('markets:list'), _filter)
        markets = response.context_data['object_list']

        self.assertEqual(markets[0], global_vertical)
        self.assertEqual(markets[1], global_generalist)
        # ... then country specific markets, but with single category matches first
        self.assertEqual(markets[2], country_vertical)
        self.assertEqual(markets[3], country_generalist)

        # Searching on only country should bring the country markets first (generalists first)
        _filter = {'operating_countries': ['uk']}
        response = self.client.get(reverse('markets:list'), _filter)
        markets = response.context_data['object_list']

        self.assertEqual(markets[0], country_generalist)
        self.assertEqual(markets[1], country_vertical)
        # ... then global markets, but with single category matche first
        self.assertEqual(markets[2], global_generalist)
        self.assertEqual(markets[3], global_vertical)

        # Searching for nothing
        response1 = self.client.get(reverse('markets:list'))
        markets1 = response.context_data['object_list']
        # ... should be the same as searching for everything
        {'operating_countries': ['uk', 'france', 'germany'], 'product_categories': ['sport', 'food']}
        response2 = self.client.get(reverse('markets:list'), _filter)
        markets2 = response.context_data['object_list']

        self.assertEqual(markets1, markets2)


class MarketAdminTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.username = 'testuser'
        cls.password = '12345'
        cls.user = User.objects.create(username=cls.username)
        cls.user.set_password('12345')
        cls.user.is_staff = True
        cls.user.save()
        cls.change_perm = Permission.objects.get(codename='change_market')
        cls.add_perm = Permission.objects.get(codename='add_market')
        cls.publish_perm = Permission.objects.get(codename='can_publish')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def _add_permission(self, permission):
        self.user.user_permissions.add(permission)
        self.user = User.objects.get(username=self.username)
        self.client.logout()
        self.client.login(username=self.user.username, password=self.password)

    def setUp(self):
        self.client.login(username=self.user.username, password=self.password)

    def tearDown(self):
        self.user.user_permissions.clear()
        self.client.logout()

    def test_add_no_publish(self):
        self._add_permission(self.add_perm)
        self._add_permission(self.change_perm)
        self.assertEquals(Market.objects.count(), 0)

        market_data = get_market_data()
        response = self.client.post(reverse('admin:markets_market_add'), market_data)

        self.assertRedirects(response, reverse('admin:markets_market_changelist'))
        self.assertEquals(Market.objects.count(), 1)
        self.assertEquals(PublishedMarket.objects.count(), 0)

    def test_publish_button(self):
        market = create_market()
        self._add_permission(self.publish_perm)
        self._add_permission(self.change_perm)
        response = self.client.get(reverse('admin:markets_market_change', args=[market.pk]))
        self.assertContains(response, 'name="_publish"')

    def test_no_publish_button(self):
        market = create_market()
        self._add_permission(self.change_perm)
        response = self.client.get(reverse('admin:markets_market_change', args=[market.pk]))
        self.assertNotContains(response, 'name="_publish"')

    def test_publish(self):
        market = create_market()
        self._add_permission(self.publish_perm)
        self._add_permission(self.change_perm)

        self.assertEquals(PublishedMarket.objects.count(), 0)

        # Try and publish, but validation will mean it won't publish
        response = self.client.post(reverse('admin:publish_market', args=[market.pk]))
        self.assertRedirects(response, reverse('admin:markets_market_change', args=[market.pk]))
        self.assertEquals(Market.objects.count(), 1)
        # XXX: CAn I test the redirected page contains "Failed to publish Market" as a user message?
        self.assertEquals(PublishedMarket.objects.count(), 0)

        # XXX: TODO Fill in all the required market attributes for publishing
