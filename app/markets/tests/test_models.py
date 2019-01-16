from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import (
    Market, PublishedMarket, SupportChannel, UploadMethod, Currency, Brand,
    SellerModel, LogisticsModel, Language, Type
)
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

    def test_unpublish_model(self):
        # Add a market, and publish it
        name = "Amazon"
        market = create_market(name=name)
        self.assertEqual(name, str(market))
        market.publish()

        # Check we have 1 market, and 1 published markets
        markets = Market.objects.all()
        published_markets = PublishedMarket.objects.all()
        self.assertEqual(len(markets), 1)
        self.assertEqual(len(published_markets), 1)

        # Unpublish the market and check we have 1 of each now
        market.unpublish()

        # Check we have 1 market, and 0 published markets
        markets = Market.objects.all()
        published_markets = PublishedMarket.objects.all()
        self.assertEqual(len(markets), 1)
        self.assertEqual(len(published_markets), 0)

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

    def test_special_terms(self):
        # Create a market, without special terms, and check that the special terms is a known phrase
        known_phrase = "We’re working hard to get a deal in place."
        market = create_market()
        self.assertEquals(market.special_terms, known_phrase)

        # Add some special terms to the actual field
        market.dit_special_terms = "Some special terms"
        self.assertEquals(market.special_terms, "Some special terms")

        # Add some empty special terms, and check that it ignores it, and uses the predetermined phrase again
        market.dit_special_terms = "     "
        self.assertEquals(market.special_terms, known_phrase)

        # The special terms also supports HTML, check that it strips the HTML and still detects empty special terms
        market.dit_special_terms = " <p>  <i> &nbsp; </i> \r\n \n </p>  "
        self.assertEquals(market.special_terms, known_phrase)

    def test_market_publishing_validation(self):
        # Create a market and check that it produces ValidationErrors
        market = create_market()
        with self.assertRaises(ValidationError):
            market.validate_for_publishing()

        # Set all the simple attributes
        market.number_of_registered_users = 'number_of_registered_users'
        market.customer_support_hours = 'customer_support_hours'
        market.seller_support_hours = 'seller_support_hours'
        market.customer_demographics = 'customer_demographics'
        market.marketing_merchandising = 'marketing_merchandising'
        market.sale_to_payment_duration = 'sale_to_payment_duration'
        market.dit_advisor_tip = 'dit_advisor_tip'
        market.explore_the_marketplace = 'http://explore_the_marketplace.com'

        # Still raises errors
        with self.assertRaises(ValidationError):
            market.validate_for_publishing()

        # Create the models required to link to the marketplace
        logistics_structure = LogisticsModel(name='logistics_structure')
        product_positioning = Type(name='product_positioning', sort_order=1)
        currency_of_payments = Currency(code='currency_of_payments')
        seller_model = SellerModel(name='seller_model')
        famous_brand_on_marketplace = Brand(name='famous_brands_on_marketplace')
        support_channel = SupportChannel(name='support_channel')
        product_details_upload_method = UploadMethod(name='product_details_upload_method')
        language = Language(name='language')
        logistics_structure.save()
        product_positioning.save()
        currency_of_payments.save()
        seller_model.save()
        famous_brand_on_marketplace.save()
        support_channel.save()
        product_details_upload_method.save()
        language.save()

        # Set all the ForeignKey and ManyToMany fields
        market.language = language
        market.currency_of_payments = (currency_of_payments,)
        market.logistics_structure = (logistics_structure,)
        market.product_positioning = (product_positioning,)
        market.seller_model = (seller_model,)
        market.famous_brands_on_marketplace = (famous_brand_on_marketplace,)
        market.customer_support_channels = (support_channel,)
        market.seller_support_channels = (support_channel,)
        market.product_details_upload_method = (product_details_upload_method,)

        # Now it no longer raises a ValidationError
        market.validate_for_publishing()
