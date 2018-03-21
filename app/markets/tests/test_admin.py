from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Market, PublishedMarket
from . import create_market, get_market_data


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
        response = self.client.post(reverse('admin:markets_market_add'),
                                    market_data)

        self.assertRedirects(response,
                             reverse('admin:markets_market_changelist'))
        self.assertEquals(Market.objects.count(), 1)
        self.assertEquals(PublishedMarket.objects.count(), 0)

    def test_publish_button(self):
        market = create_market()
        self._add_permission(self.publish_perm)
        self._add_permission(self.change_perm)
        response = self.client.get(
            reverse('admin:markets_market_change', args=[market.pk]))
        self.assertContains(response, 'name="_publish"')

    def test_no_publish_button(self):
        market = create_market()
        self._add_permission(self.change_perm)
        response = self.client.get(
            reverse('admin:markets_market_change', args=[market.pk]))
        self.assertNotContains(response, 'name="_publish"')

    def test_publish(self):
        market = create_market()
        self._add_permission(self.publish_perm)
        self._add_permission(self.change_perm)

        self.assertEquals(PublishedMarket.objects.count(), 0)

        # Try and publish, but validation will mean it won't publish
        response = self.client.post(
            reverse('admin:publish_market', args=[market.pk]))
        self.assertRedirects(response, reverse('admin:markets_market_change',
                                               args=[market.pk]))
        self.assertEquals(Market.objects.count(), 1)
        # XXX: CAn I test the redirected page contains
        # "Failed to publish Market" as a user message?
        self.assertEquals(PublishedMarket.objects.count(), 0)

    def test_admin_restricted(self):
        with self.settings(RESTRICT_ADMIN=True):
            self._add_permission(self.add_perm)
            self._add_permission(self.change_perm)
            self.assertEquals(Market.objects.count(), 0)

            market_data = get_market_data()
            response = self.client.post(
                reverse('admin:markets_market_add'),
                market_data,
                **{'HTTP_X_FORWARDED_FOR': '74.125.224.72'}
            )
            self.assertEqual(response.status_code, 404)
