from django.core.urlresolvers import reverse
from django.test import TestCase
from . import create_market, create_country


class MarketListTests(TestCase):

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
        uk = create_country('uk', 'Europe')
        fr = create_country('france', 'Europe')
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
        uk = create_country('uk', 'Europe')
        fr = create_country('france', 'Europe')
        amazon = create_market(name="Amazon", countries_served=[uk])
        ebay = create_market(name="Ebay", countries_served=[uk, fr])

        # Filter on a list of names, including an incorrect name, we should get back both markets
        response = self.client.get(reverse('markets:list'), {'name': ['Amazon', 'Ebay', 'Blah']})
        self.assertContains(response, amazon.name, status_code=200)
        self.assertContains(response, ebay.name, status_code=200)

        # Filter on a property of a related model, to a related model of the Market
        # Filter for Europe region, we should get both markets
        response = self.client.get(reverse('markets:list'), {'region': 'Europe'})
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
