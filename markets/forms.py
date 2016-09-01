import base64
from django import forms
from core.forms import (
    QueryChoiceField, QueryMultipleCheckboxField, QueryRadioField, QueryMultipleChoiceField, ModelQueryForm
)
from .models import Market, Logo, Region


class FilteringForm(ModelQueryForm):
    """
    Form for initial filtering of markets on the first page of the journey
    """

    class Meta:
        model = Market
        fields = []
        query_fields = [
            ('platform_type', QueryMultipleCheckboxField, 'platform_type'),
            ('product_type', QueryChoiceField, 'product_type'),
            ('logistics_structure', QueryMultipleCheckboxField, 'logistics_structure'),
            ('countries_served', QueryChoiceField, 'countries_served__name'),
            ('product_categories', QueryMultipleChoiceField, 'product_categories__name'),
        ]


class MarketFilterForm(ModelQueryForm):
    """
    The filters that appear on the results listing page, for furhter filtering of Markets
    """

    class Meta:
        model = Market
        fields = []
        query_fields = [
            ('platform_type', QueryMultipleCheckboxField, 'platform_type'),
            ('product_type', QueryMultipleCheckboxField, 'product_type'),
            ('logistics_structure', QueryMultipleCheckboxField, 'logistics_structure'),
            ('countries_served', QueryMultipleCheckboxField, 'countries_served__name'),
            ('product_categories', QueryMultipleCheckboxField, 'product_categories__name'),
            ('region', QueryMultipleCheckboxField, 'countries_served__region__name'),
        ]


class LogoAdminForm(forms.ModelForm):

    class Meta:
        model = Logo
        exclude = ['_encoded_data']

    logo = forms.ImageField(label='Upload PNG')

    def clean_logo(self):
        try:
            assert self.files['logo'].name.lower().endswith('.png')
            encoded = "data:image/png;base64,{}".format(
                base64.b64encode(self.files['logo'].read()).decode("utf-8"))
            setattr(self, '_encoded_file_data', encoded)
        except:
            raise forms.ValidationError("Invalid PNG file uploaded.")

    def save(self, *args, **kwargs):
        self.instance._encoded_data = getattr(self, '_encoded_file_data')
        return super(LogoAdminForm, self).save(*args, **kwargs)
