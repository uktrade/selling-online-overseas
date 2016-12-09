from django.contrib.admin import widgets
from django import forms
from django.contrib import admin

from .models import (
    Market, Logo, SupportChannel, UploadMethod, Currency, Brand, SellerModel, LogisticsModel, MarketForSignOff
)
from .forms import LogoAdminForm


admin.site.register(SupportChannel)
admin.site.register(UploadMethod)
admin.site.register(Currency)
admin.site.register(Brand)
admin.site.register(SellerModel)
admin.site.register(LogisticsModel)


class MarketAdmin(admin.ModelAdmin):

    list_display = ['name', 'web_address']
    ordering = ['name']
    readonly_fields = ['slug']
    filtered_widget_fields = ['countries_served', 'product_categories', 'famous_brands_on_marketplace']
    checkbox_widget_fields = ['customer_support_channels']

    fieldsets = (
        ('Marketplace Description', {
            'fields': (
                ('name', 'slug', 'logo'),
                'countries_served',
                'web_address',
                'description',
            )
        }),
        ('Department of International Trade tips and terms', {
            'fields': (
                'ukti_terms',
                'dit_advisor_tip',
            )
        }),
        ('Tell me about this marketplace', {
            'fields': (
                ('web_traffic', 'seller_model', 'product_type'),
                ('product_categories'),
                ('famous_brands_on_marketplace'),
            )
        }),
        ('Who are the customers?', {
            'fields': (
                'customer_demographics',
                ('customer_support_channels', 'customer_support_hours'),
            )
        }),
        ('Fulfilment and delivery', {
            'fields': (
                ('logistics_structure', 'logistics_structure_notes'),
                ('shipping_tracking_required', 'shipping_tracking_required_notes',),
            )
        }),
        ('What costs will I pay this marketplace?', {
            'fields': (
                ('registration_fees', 'registration_fees_currency', 'registration_fees_notes',),
                ('membership_fees', 'membership_fees_currency', 'membership_fees_frequency',),
                ('fee_per_listing', 'fee_per_listing_notes',),
                ('commission_lower', 'commission_upper', 'commission_notes',),
                ('deposit', 'deposit_currency', 'deposit_notes',),
            )
        }),
        ('What does the marketplace need me to do?', {
            'fields': (
                ('translation_verbal', 'translation_verbal_notes',),
                ('translation_application_process', 'translation_application_process_notes',),
                ('translation_product_content', 'translation_product_content_notes',),
                ('translation_seller_support', 'translation_seller_support_notes',),
                ('local_bank_account_needed', 'local_bank_account_needed_notes',),
                ('local_incorporation_needed', 'local_incorporation_needed_notes',),
                ('local_return_address_required', 'local_return_address_required_notes',),
                ('exclusivity_required', 'exclusivity_required_notes',),
                ('product_details_upload', 'product_details_upload_notes',),
            )
        }),
        ('How will I get paid?', {
            'fields': (
                ('payment_terms_days', 'currency_of_payments',),
            )
        }),
        ('What help do they give sellers like me?', {
            'fields': (
                ('marketing_merchandising',),
                ('seller_support_channels', 'seller_support_hours'),
            )
        }),
        ('What should I do next?', {
            'fields': (
                'signup_address',
            )
        }),
    )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in self.filtered_widget_fields:
            kwargs['widget'] = widgets.FilteredSelectMultiple(
                db_field.verbose_name,
                db_field.name in self.filter_vertical
            )
        else:
            kwargs['widget'] = forms.CheckboxSelectMultiple()

        return super(admin.ModelAdmin, self).formfield_for_manytomany(db_field, request=request, **kwargs)


class MarketSignOffAdmin(MarketAdmin):

    list_display = ['name', 'web_address', 'published']

    def _flatten(self, data):
        rdata = []
        for x in data:
            rdata += self._flatten(x) if hasattr(x, '__iter__') and not isinstance(x, str) else [x]
        return rdata

    def get_fieldsets(self, *args, **kwargs):
        fields = super().get_fieldsets(*args, **kwargs)
        return fields + (('Admin', {'fields': ('published',)}),)


class LogoAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    form = LogoAdminForm


admin.site.register(Market, MarketAdmin)
admin.site.register(MarketForSignOff, MarketSignOffAdmin)
admin.site.register(Logo, LogoAdmin)
