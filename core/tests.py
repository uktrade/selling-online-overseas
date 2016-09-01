from django.test import TestCase
from django import forms
from .forms import (
    QueryChoiceField, QueryMultipleCheckboxField, QueryRadioField, QueryMultipleChoiceField, ModelQueryForm
)
from .models import TestModel1, TestModel2


class QueryFieldTests(TestCase):

    def test_query_choice_field(self):
        """
        Test that we can create a QueryChoiceField and that it pulls the unique values from the database
        """

        # Add a TestModel1 to the database with a known name, and create a QueryField on that model/attr
        TestModel1(name='foo').save()
        field = QueryChoiceField(TestModel1, 'name')

        # It should be a select widget, with choices that are the only value in the DB
        self.assertIsInstance(field.widget, forms.Select)
        self.assertEqual(field.choices, [('foo', 'foo')])

        # Add another model with a new name and test again
        TestModel1(name='bar').save()
        field = QueryChoiceField(TestModel1, 'name')
        # The new name comes first in the choices as they are sorted alphabetically
        self.assertEqual(field.choices, [('bar', 'bar'), ('foo', 'foo')])

        # Add another model, with a duplicated name
        TestModel1(name='foo').save()
        field = QueryChoiceField(TestModel1, 'name')
        # The same choices should be returned with no duplicates
        self.assertEqual(field.choices, [('bar', 'bar'), ('foo', 'foo')])

    def test_query_multiplechoice_field(self):
        """
        Basic test from above, but ensuring the widget is the correct type
        """

        # Create three models, 2 with duplicate names
        TestModel1(name='foo').save()
        TestModel1(name='foo').save()
        TestModel1(name='bar').save()

        # Initialise the field, and test it has the correct type, and 2 unique choices
        field = QueryMultipleChoiceField(TestModel1, 'name')
        self.assertIsInstance(field.widget, forms.SelectMultiple)
        self.assertEqual(field.choices, [('bar', 'bar'), ('foo', 'foo')])

    def test_query_multiplecheckbox_field(self):
        """
        Basic test from above, but ensuring the widget is the correct type
        """

        # Create three models, 2 with duplicate names
        TestModel1(name='foo').save()
        TestModel1(name='foo').save()
        TestModel1(name='bar').save()

        # Initialise the field, and test it has the correct type, and 2 unique choices
        field = QueryMultipleCheckboxField(TestModel1, 'name')
        self.assertIsInstance(field.widget, forms.CheckboxSelectMultiple)
        self.assertEqual(field.choices, [('bar', 'bar'), ('foo', 'foo')])

    def test_query_radio_field(self):
        """
        Basic test from above, but ensuring the widget is the correct type
        """

        # Create three models, 2 with duplicate names
        TestModel1(name='foo').save()
        TestModel1(name='foo').save()
        TestModel1(name='bar').save()

        # Initialise the field, and test it has the correct type, and 2 unique choices
        field = QueryRadioField(TestModel1, 'name')
        self.assertIsInstance(field.widget, forms.RadioSelect)
        self.assertEqual(field.choices, [('bar', 'bar'), ('foo', 'foo')])

    def test_query_choice_field_related(self):
        """
        Test that the QueryChoiceField correctly links through to related models
        """

        # Create a TestModel1 and a TestModel2
        test1 = TestModel1(name='foo', symbol="*")
        test1.save()
        test2 = TestModel2(name='bar')
        test2.save()
        # Add the TestModel1 as a one of the ManyToMany field ('other_model') on the TestModel2
        test2.other_model.add(test1)
        test2.save()

        # Set up QueryChoiceFields on the ManyToMany field, and on a property of the related model
        model_field = QueryChoiceField(TestModel2, 'other_model')
        name_field = QueryChoiceField(TestModel2, 'other_model__name')

        # Check we get the expected name choices for the linked model
        self.assertEqual(name_field.choices, [('foo', 'foo')])
        # And the related model choices should be represented by a tuples of pk and the str of the model
        self.assertEqual(model_field.choices, [(test1.pk, str(test1))])

        # Add a new TestModel1, but don't link it to the TestModel2
        test3 = TestModel1(name='spam', symbol="*")
        test3.save()
        # Recreate the fields
        model_field = QueryChoiceField(TestModel2, 'other_model')
        name_field = QueryChoiceField(TestModel2, 'other_model__name')

        # Despite not being linked, we should still get the new related model coming through
        self.assertEqual(name_field.choices, [('foo', 'foo'), ('spam', 'spam')])
        self.assertEqual(model_field.choices, [(test1.pk, str(test1)), (test3.pk, str(test3))])

        # Create a field for the symbol, and still make sure we only get the 1 (unique) choice
        symbol_field = QueryChoiceField(TestModel2, 'other_model__symbol')
        self.assertEqual(symbol_field.choices, [('*', '*')])


class TestForm(ModelQueryForm):

    class Meta:
        model = TestModel2
        fields = []
        query_fields = [
            ('name', QueryChoiceField, 'name'),
            ('other_model', QueryMultipleCheckboxField, 'other_model'),
            ('other_model_name', QueryRadioField, 'other_model__name'),
            ('other_model_symbol', QueryMultipleChoiceField, 'other_model__symbol'),
        ]


class ModelQueryFormTests(TestCase):

    def test_form_has_fields(self):
        """
        Instantiate a ModelQueryForm and make sure that it's query_fields are built with the correct type
        """

        form = TestForm()
        form_fields = [field.name for field in form]

        # There should be all 4 (and no more) fields in the form
        self.assertEqual(form_fields, ['name', 'other_model', 'other_model_name', 'other_model_symbol'])

        # Check the types are all correct
        self.assertIsInstance(form['name'].field, QueryChoiceField)
        self.assertIsInstance(form['other_model'].field, QueryMultipleCheckboxField)
        self.assertIsInstance(form['other_model_name'].field, QueryRadioField)
        self.assertIsInstance(form['other_model_symbol'].field, QueryMultipleChoiceField)

    def test_form_query_fields(self):
        """
        Test that fields in the form have initialised themselves and set their choices correctly
        """

        # Create 2 TestModel1's and a TestModel2
        test1 = TestModel1(name='foo', symbol="*")
        test1.save()
        test2 = TestModel1(name='spam', symbol="*")
        test2.save()
        test3 = TestModel2(name='bar')
        test3.save()

        # Instantiate the form, and check the fields all have queried to get their correct choices
        form = TestForm()
        self.assertEqual(form['name'].field.choices, [('bar', 'bar')])
        self.assertEqual(form['other_model'].field.choices, [(test1.pk, str(test1)), (test2.pk, str(test2))])
        self.assertEqual(form['other_model_name'].field.choices, [('foo', 'foo'), ('spam', 'spam')])
        self.assertEqual(form['other_model_symbol'].field.choices, [('*', '*')])

    def test_form_prepopulation(self):
        """
        Test that prepopulating the form with a dictionary (or, more usually some request data) does produce a form
        with the values populated, and that the form is valid
        """

        # Create 2 TestModel1's and a TestModel2
        test1 = TestModel1(name='foo', symbol="*")
        test1.save()
        test2 = TestModel1(name='spam', symbol="*")
        test2.save()
        test3 = TestModel2(name='eggs')
        test3.save()
        test4 = TestModel2(name='bar')
        test4.save()

        # Instantiate the form, and check the fields all have queried to get their correct choices
        form = TestForm({'other_model_symbol': ['*'], 'other_model_name': 'foo'})
        self.assertEqual(form['other_model_symbol'].value(), ['*'])
        self.assertEqual(form['other_model_name'].value(), 'foo')
        # Check the form is valid
        self.assertTrue(form.is_valid())

    def test_form_KNOWN_FAILURE(self):
        """
        XXX: This shows a known bug with the form, as yet to be fixed
        """

        # Create a test model
        test3 = TestModel2(name='eggs')
        test3.save()

        # Instantiate the form populating the 'name' attribute
        form = TestForm({'name': 'eggs'})

        # XXX: The form INVALID
        # XXX: This seems to be special and unique to the 'name'
        # XXX: Chaning the type of the field, or the value in the database doesn't help
        # XXX: But changing the name of the 'name' field to something like 'xname' does fix the issue
        self.assertTrue(not form.is_valid())
