from django import forms
from django.db import models


class QueryChoiceMixin(object):
    """
    Mixin for a choice field, that takes a model and an attribute of that model, and gets all distinct values for that
    attribute from the database, and uses that to generate the choices of the field
    """

    def __init__(self, model, attribute, *args, **kwargs):
        """
        Get and set up the choices for the field from the database.
        Take a model to query, and the standard djagno '__' delimited syntax for related models.
        e.g. MyQueryField(model=MyModel, attr='my_related_model__name')
        """

        # NOTE: This could (arguably should) be done in the _get_choices method property.  But that doesn't work well
        # NOTE: for radio/checkbox widgets in the template.  Collecting the choices in the init means that you can
        # NOTE: treat the field normally in the templates, but means that you can't define this field normally in the
        # NOTE: form.  See tests for examples.

        # Split the attr into it's components
        self.attribute = attribute
        components = self.attribute.split('__')
        # Get the last part of the attribute, which is the ultimate attribute we're after
        attr_name = components.pop()

        for component in components:
            # Progessively get the related models that are in the components
            model = model._meta.get_field(component).related_model

        # Now get the field of the model
        model_field = model._meta.get_field(attr_name)

        if len(model_field.choices) > 0:
            # The field has predefined choices, use those
            choices = model_field.choices
        elif isinstance(model_field, models.ManyToManyField):
            # The fiels is a many to many, get the model and make a list of tuples like [(pk, model) ...]
            related_model = model_field.related_model
            choices = [(model.pk, "{0}".format(model)) for model in related_model.objects.all()]
        else:
            # Get distinct values for attribute of the model from the database, and build choices like [(val, val) ...]
            choices = model.objects.all().values_list(attr_name, attr_name).distinct().order_by(attr_name)

        return super().__init__(choices=choices, required=False, *args, **kwargs)


class QueryChoiceField(QueryChoiceMixin, forms.ChoiceField):
    """
    A convinience model using QueryChoiceMixin and ChoiceField, that provide a ChoiceField that set it's own choices
    """

    pass


class QueryMultipleChoiceField(QueryChoiceMixin, forms.MultipleChoiceField):
    """
    A convinience model using QueryChoiceMixin and MultipleChoiceField, that provide a MultipleChoiceField that set
    it's own choices
    """

    pass


class QueryMultipleCheckboxField(QueryMultipleChoiceField):
    """
    A convinience model identical to the QueryMultipleChoiceField, but that uses a default mutliple checkbox as it's
    widget, rather than a multi-select box
    """

    widget = forms.CheckboxSelectMultiple


class QueryRadioField(QueryChoiceField):
    """
    A convinience model identical to the QueryChoiceField, but that uses a default radio select as it's
    widget, rather than a multi-select box
    """

    widget = forms.RadioSelect


class ModelQueryForm(forms.ModelForm):
    """
    A Model form that can have a specified list of query_fields, and it will automatically convert these into the
    specified type query field, and initialise them.  Requires a Meta attribute like:
        query_fields = [
            ('attribute_name', QueryField),
            ('other_attribute', QueryMultipleCheckboxField),
            ...
        ]
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise the form, creating/initialising the query fields along the way.
        """

        super().__init__(*args, **kwargs)

        try:
            query_fields = self.Meta.query_fields
        except AttributeError:
            query_fields = []

        for field_name, field_type, attribute in query_fields:
            self.fields[field_name] = field_type(self.Meta.model, attribute)
