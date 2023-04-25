import random

from locust import HttpLocust, TaskSet, task

from data import search_options


class UserBehavior(TaskSet):

    @task(1)
    def listing_page(self):
        base_url = '/selling-online-overseas/markets/results'

        category_count = random.randint(0, 5)
        categories = []
        for _ in xrange(category_count):
            categories.append(random.choice(search_options['categories']))

        country_count = random.randint(0, 5)
        countries = []
        for _ in xrange(country_count):
            countries.append(random.choice(search_options['countries']))

        category_filter = 'product_category={0}'.format('&product_category='.join(categories))
        country_filter = 'operating_countries={0}'.format('&operating_countries='.join(countries))

        url = '{0}?{1}&{2}'.format(base_url, category_filter, country_filter)
        self.client.get(url, name=base_url)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
