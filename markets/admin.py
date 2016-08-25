from django.contrib import admin

from .models import (Market, ProductCategory, Logo, Region, Country)
from .forms import LogoAdminForm


admin.site.register(Region)
admin.site.register(Country)
admin.site.register(ProductCategory)


class MarketAdmin(admin.ModelAdmin):

    list_display = ['name', 'web_address']
    ordering = ['name']

    fieldsets = (
        ('Platform Basics', {
            'fields': (
                ('name', 'logo',),
                'description',
                'web_address',
            )
        }),
        ('Platform Details', {
            'fields': (
                'countries_served',
                'product_categories',
                'web_traffic',
                ('platform_type', 'product_type'),
                ('customer_support_channels', 'seller_support_channels'),
                'customer_demographics',
            )
        }),
        ('On-Boarding/Application', {
            'fields': (
                ('local_bank_account_needed', 'local_bank_account_needed_notes',),
                ('local_incorporation_needed', 'local_incorporation_needed_notes',),
                ('translation_verbal', 'translation_verbal_notes',),
                ('translation_application_process', 'translation_application_process_notes',),
                ('translation_product_content', 'translation_product_content_notes',),
                ('translation_customer_service', 'translation_customer_service_notes',),
                ('exclusivity_required', 'exclusivity_required_notes',),
                'product_details_upload',
            )
        }),
        ('Finance', {
            'fields': (
                ('currency_of_payments', 'payment_terms_days', 'payment_terms_days_notes',),
                ('commission', 'commission_notes',),
                ('registration_fees', 'registration_fees_notes',),
                ('membership_fees', 'membership_fees_notes',),
                ('fee_per_listing', 'fee_per_listing_notes',),
                'ukti_terms',
            )
        }),
        ('Logisitics', {
            'fields': (
                ('logistics_structure', 'logistics_structure_notes'),
                ('shipping_tracking_required', 'shipping_tracking_required_notes',),
                ('local_return_address_required', 'local_return_address_required_notes',)
            )
        }),
    )


class LogoAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    form = LogoAdminForm


admin.site.register(Market, MarketAdmin)
admin.site.register(Logo, LogoAdmin)
