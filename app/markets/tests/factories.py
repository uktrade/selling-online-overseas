import factory
import factory.fuzzy

from markets.models import PublishedMarket
import datetime


class PublishedMarketFactory(factory.django.DjangoModelFactory):
    last_modified = factory.fuzzy.FuzzyNaiveDateTime(datetime.datetime.now())
    name = factory.fuzzy.FuzzyText(length=12)
    slug = factory.fuzzy.FuzzyText(length=12)
    e_marketplace_description = factory.fuzzy.FuzzyText(length=50)
    web_address = factory.LazyAttribute(
        lambda company: 'http://%s.example.com' % company.name)
    explore_the_marketplace = factory.LazyAttribute(
        lambda company: 'http://%s.example.com' % company.name)

    number_of_registered_users = factory.fuzzy.FuzzyInteger(100000)

    customer_support_hours = factory.fuzzy.FuzzyText(length=20)
    seller_support_hours = factory.fuzzy.FuzzyText(length=20)

    customer_demographics = factory.fuzzy.FuzzyText(length=50)

    class Meta:
        model = PublishedMarket
