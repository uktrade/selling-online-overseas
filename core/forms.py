from django import forms
from django.db import models


class QueryChoiceMixin(object):
    """
    Mixin for a choice field, that takes a model and an attribute of that model, and gets all distinct values for that
    attribute from the database, and uses that to generate the choices of the field
    """

    def __init__(self, model, attr, *args, **kwargs):
        components = attr.split('__')
        attr = components.pop()

        for component in components:
            model = model._meta.get_field(component).related_model

        model_field = model._meta.get_field(attr)
        if isinstance(model_field, models.ManyToManyField):
            related_model = model_field.related_model
            choices = [(model.pk, "{0}".format(model)) for model in related_model.objects.all()]
        elif len(model_field.choices) > 0:
            choices = model_field.choices
        else:
            choices = model.objects.all().values_list(attr, attr).distinct().order_by(attr)

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

    def __init__(self, *args, **kwargs):
        return super().__init__(widget=forms.CheckboxSelectMultiple(), *args, **kwargs)


class QueryRadioField(QueryChoiceField):
    """
    A convinience model identical to the QueryChoiceField, but that uses a default radio select as it's
    widget, rather than a multi-select box
    """

    def __init__(self, *args, **kwargs):
        return super().__init__(widget=forms.RadioSelect(), *args, **kwargs)
