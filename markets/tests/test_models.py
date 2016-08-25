from django.core.urlresolvers import reverse
from django.test import TestCase
from ..models import Market
from . import create_market


class MarketModelTests(TestCase):

    def test_blank_works(self):
        name = "Amazon"
        market = create_market(name=name)
        self.assertEqual(name, str(market))
