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

    fieldsets = (
        ('Marketplace Description', {
            'fields': (
                ('name', 'slug', 'logo'),
                'description',
                'web_address',
            )
        }),
        ('Department of International Trade tips and terms', {
            'fields': (
                'dit_advisor_tip',
                'ukti_terms',
            )
        }),
        ('Platform Details', {
            'fields': (
                ('countries_served', 'web_traffic',),
                ('product_categories', 'prohibited_items',),
                'product_type',
                ('customer_support_channels', 'seller_support_channels'),
                ('customer_support_hours', 'seller_support_hours'),
                'customer_demographics',
                'marketing_merchandising',
                'famous_brands_on_marketplace',
            )
        }),
        ('Organise Translation', {
            'fields': (
                ('translation_verbal', 'translation_verbal_notes',),
                ('translation_application_process', 'translation_application_process_notes',),
                ('translation_product_content', 'translation_product_content_notes',),
                ('translation_seller_support', 'translation_seller_support_notes',),
            )
        }),
        ('Setup', {
            'fields': (
                ('local_bank_account_needed', 'local_bank_account_needed_notes',),
                ('local_incorporation_needed', 'local_incorporation_needed_notes',),
                ('product_details_upload', 'product_details_upload_notes',),
            )
        }),
        ('Agree to', {
            'fields': (
                ('exclusivity_required', 'exclusivity_required_notes',),
            )
        }),
        ('Finance', {
            'fields': (
                ('payment_terms_days', 'currency_of_payments',),
                ('registration_fees_currency', 'registration_fees', 'registration_fees_notes',),
                ('deposit_currency', 'deposit', 'deposit_notes',),
                ('membership_fees_currency', 'membership_fees', 'membership_fees_frequency',),
                ('commission_lower', 'commission_upper', 'commission_notes',),
                ('fee_per_listing', 'fee_per_listing_notes',),
            )
        }),
        ('Logisitics', {
            'fields': (
                'seller_model',
                ('logistics_structure', 'logistics_structure_notes'),
                ('shipping_tracking_required', 'shipping_tracking_required_notes',),
                ('local_return_address_required', 'local_return_address_required_notes',)
            )
        }),
        ('What should I do next?', {
            'fields': (
                'signup_address',
            )
        }),
    )


class MarketSignOffAdmin(MarketAdmin):
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
