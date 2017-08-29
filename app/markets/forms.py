from django import forms

from . import BOOL_CHOICES
from .models import Market, Logo

from core.forms import (
    QueryChoiceField, QueryMultipleCheckboxField, QueryRadioField, QueryMultipleChoiceField, ModelQueryForm
)


class MarketListFilterForm(ModelQueryForm):
    """
    The filters that appear on the results listing page, for furhter filtering of Markets.
    NOTE: The query_fields on this form must be a superset of those on the FitleringForm class
    """

    # Need to add these 2 fields manually, so that they can be MultipleChoice fields
    # If added as part of the model form, they would be TypedChoice, and not able to take both True AND False
    local_bank_account_needed = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                          required=False, choices=BOOL_CHOICES)
    local_incorporation_needed = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                           required=False, choices=BOOL_CHOICES)

    translation_verbal = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                   required=False, choices=BOOL_CHOICES)
    translation_application_process = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                required=False, choices=BOOL_CHOICES)
    translation_product_content = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                            required=False, choices=BOOL_CHOICES)
    translation_seller_support = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                           required=False, choices=BOOL_CHOICES)

    class Meta:
        model = Market
        fields = []
        query_fields = [
            ('product_positioning', QueryMultipleCheckboxField, 'product_positioning__name'),
            ('logistics_structure', QueryMultipleCheckboxField, 'logistics_structure__name'),
            ('operating_countries', QueryMultipleCheckboxField, 'operating_countries__name'),
            ('product_categories', QueryMultipleCheckboxField, 'product_categories__name'),
        ]
