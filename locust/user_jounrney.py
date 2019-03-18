import random
import time

from locust import HttpLocust, TaskSet, task

from data import search_options, market_slugs


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    @task(1)
    def start_page(self):
        self.client.get("/markets")

    @task(5)
    def search_page(self):
        self.client.get("/markets/filter")

    @task(10)
    def search_categories(self):
        self._perform_search('/products/api', search_options['categories'])

    @task(10)
    def search_countries(self):
        self._perform_search('/geography/api', search_options['countries'])

    @task(4)
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

        url = "{0}?{1}&{2}".format(base_url, category_filter, country_filter)
        self.client.get(url, name=base_url)

    @task(3)
    def details_page(self):
        base_url = '/selling-online-overseas/markets/details'

        slug = random.choice(market_slugs)
        url = '{0}/{1}'.format(base_url, slug)
        self.client.get(url, name=base_url)

    def _perform_search(self, base_url, options):
        min_delay = 20
        max_delay = 500

        search_term = random.choice(options)
        query = ""

        for letter in search_term:
            query += letter
            self.client.get("{0}?q={1}".format(base_url, query), name=base_url)
            delay = random.randint(min_delay, max_delay) / 1000.0
            time.sleep(delay)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
