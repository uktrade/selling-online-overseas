from django.test import TestCase
from django import forms
from markets.models import Market
from ..forms import (QueryChoiceField, QueryMultipleChoiceField, QueryMultipleCheckboxField)
from . import (create_market, create_logo, create_country, load_sample_png)


class QueryChoicesMixinTests(object):

    def test_query_choices_populated(self):
        create_market(name="Amazon")
        create_market(name="Ebay")
        field = self.field(Market, 'name')
        self.assertListEqual(field.choices, [("Amazon", "Amazon"), ("Ebay", "Ebay")])

    def test_query_choices_distinct(self):
        uk = create_country('uk', 'Europe')
        fr = create_country('france', 'Europe')
        create_market(name="Amazon", countries_served=[uk])
        create_market(name="Ebay", countries_served=[uk, fr])

        field = self.field(Market, 'countries_served')
        self.assertListEqual(field.choices, [(uk.pk, "uk"), (fr.pk, "france")])


class QueryChoiceFieldTests(TestCase, QueryChoicesMixinTests):

    field = QueryChoiceField

    def test_query_choices_setup(self):
        field = self.field(Market, 'name')
        self.assertListEqual(field.choices, [])
        self.assertIsInstance(field.widget, forms.widgets.Select)
        self.assertFalse(field.widget.allow_multiple_selected)


class QueryMultipleChoiceFieldTests(TestCase, QueryChoicesMixinTests):

    field = QueryMultipleChoiceField

    def test_query_choices_empty(self):
        field = self.field(Market, 'name')
        self.assertListEqual(field.choices, [])
        self.assertIsInstance(field.widget, forms.widgets.Select)
        self.assertTrue(field.widget.allow_multiple_selected)


class QueryMultipleCheckboxFieldTests(TestCase, QueryChoicesMixinTests):

    field = QueryMultipleCheckboxField

    def test_query_choices_empty(self):
        field = self.field(Market, 'name')
        self.assertListEqual(field.choices, [])
        self.assertIsInstance(field.widget, forms.widgets.CheckboxSelectMultiple)
        self.assertTrue(field.widget.allow_multiple_selected)
