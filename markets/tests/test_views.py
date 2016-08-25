from django.core.urlresolvers import reverse
from django.test import TestCase
from . import create_market


class MarketListTests(TestCase):

    def test_list_markets(self):
        # XXX: remove test until assets are in place
        return
        market = create_market()
        response = self.client.get(reverse('markets:list'))
        self.assertContains(response, market.name, status_code=200)
