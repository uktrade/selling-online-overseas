from django.core.urlresolvers import reverse
from django.test import TestCase
from ..models import Market, PublishedMarket
from . import create_market


class MarketModelTests(TestCase):

    def test_blank_works(self):
        # We have 0 markets
        markets = Market.objects.all()
        self.assertEqual(len(markets), 0)

        # Add one
        name = "Amazon"
        market = create_market(name=name)
        self.assertEqual(name, str(market))

        # Check we have 1 market
        markets = Market.objects.all()
        self.assertEqual(len(markets), 1)

    def test_publish_model(self):
        # We have 0 markets and published markets
        markets = Market.objects.all()
        published_markets = PublishedMarket.objects.all()
        self.assertEqual(len(markets), 0)
        self.assertEqual(len(published_markets), 0)

        # Add a market, but don't publish yet
        name = "Amazon"
        market = create_market(name=name)
        self.assertEqual(name, str(market))

        # Check we have 1 market, and still 0 published markets
        markets = Market.objects.all()
        published_markets = PublishedMarket.objects.all()
        self.assertEqual(len(markets), 1)
        self.assertEqual(len(published_markets), 0)

        # Publish the market and check we have 1 of each now
        market.publish()
        markets = Market.objects.all()
        published_markets = PublishedMarket.objects.all()
        self.assertEqual(len(markets), 1)
        self.assertEqual(len(published_markets), 1)
        # Make sure the market and it's published market share the same pk
        self.assertEqual(markets[0].pk, published_markets[0].pk)

    def test_market_delete(self):
        # Create 3 markets and publish 2 of them
        market1 = create_market()
        market2 = create_market()
        market3 = create_market()
        market2.publish()
        market3.publish()

        # Check we have 3 markets, and 2 published markets
        markets = Market.objects.all()
        published_markets = PublishedMarket.objects.all()
        self.assertEqual(len(markets), 3)
        self.assertEqual(len(published_markets), 2)

        # Delete a market, ensure that the corresponding published market was deleted
        market2.delete()
        markets = Market.objects.all()
        published_markets = PublishedMarket.objects.all()
        self.assertEqual(len(markets), 2)
        self.assertEqual(len(published_markets), 1)
        # and that the remaining publsihed market is the correct one
        self.assertEqual(published_markets[0].pk, market3.pk)

        # Delete the unpublished market, and just make sure everything is still fine with the published one
        market1.delete()
        markets = Market.objects.all()
        published_markets = PublishedMarket.objects.all()
        self.assertEqual(len(markets), 1)
        self.assertEqual(len(published_markets), 1)
        published_market = published_markets[0]
        market = markets[0]
        self.assertEqual(market.pk, market3.pk)
        self.assertEqual(market.pk, published_market.pk)
