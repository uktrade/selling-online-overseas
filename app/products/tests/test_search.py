import os
import shutil

from django.test import TestCase
from django.core import management
from django.conf import settings

from ..models import Category
from ..search import perform_category_query


test_csvfilename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_taxonomy.csv')


class SearchTests(TestCase):

    def test_index_creation(self):
        if os.path.exists(settings.WHOOSH_INDEX_DIR):
            shutil.rmtree(settings.WHOOSH_INDEX_DIR)

        self.assertFalse(os.path.exists(settings.WHOOSH_INDEX_DIR))

        management.call_command('build_index', inputfile=test_csvfilename)
        self.assertTrue(os.path.exists(settings.WHOOSH_INDEX_DIR))

    def test_perform_query(self):
        categories, suggestions = perform_category_query('Food')
        self.assertEqual(categories, {'Food': ['Food']})

        categories, suggestions = perform_category_query('Chocolate')
        self.assertEqual(categories, {'Food': ['Chocolate']})

        categories, suggestions = perform_category_query('Cadbury')
        self.assertEqual(categories, {'Food': ['Cadbury']})
