from django.contrib.admin import widgets
from django import forms
from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms

from .models import (
    Market, Logo, PublishedMarket, SupportChannel, UploadMethod, Currency, Brand, SellerModel, LogisticsModel
)
from .forms import LogoAdminForm
from reversion.admin import VersionAdmin
from django.utils.safestring import mark_safe


admin.site.register(SupportChannel)
admin.site.register(UploadMethod)
admin.site.register(Currency)
admin.site.register(Brand)
admin.site.register(SellerModel)
admin.site.register(LogisticsModel)


class MarketForm(forms.ModelForm):

    class Meta:
        model = Market
        exclude = ['live_version']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            market = kwargs['instance']
            if market is None:
                return
        except KeyError:
            # Adding a new market, so there is no instance, return early
            return

        try:
            published_market, created = PublishedMarket.objects.get_or_create(id=market.id)

            for field_name, field in self.fields.items():
                try:
                    market_value = getattr(market, field_name)
                    published_market_value = getattr(published_market, field_name)

                    if hasattr(market_value, 'all'):
                        market_value = set([item.id for item in market_value.all()])
                        published_market_value = set([item.id for item in published_market_value.all()])

                    if market_value != published_market_value:
                        field.label_suffix = mark_safe(' <span style="color: red; font-weight: bold;">(edited)</span>')
                except AttributeError:
                    continue

        except PublishedMarket.DoesNotExist:
            # No PublishedMarket exists, nothing to compare to, just pass
            pass


@admin.register(Market)
class MarketAdmin(VersionAdmin):

    list_display = ['name', 'web_address']
    ordering = ['name']
    readonly_fields = ['slug']
    filter_horizontal = ['countries_served', 'product_categories', 'famous_brands_on_marketplace']
    checkbox_widget_fields = ['customer_support_channels']
    form = MarketForm

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

    def get_urls(self):
        """
        Add the publishing URL to the ModelAdmin
        """

        urls = super().get_urls()
        custom_urls = [
            url(r'^(?P<pk>[0-9]+)/publish/$', self.admin_site.admin_view(self.publish_view), name="publish_market"),
        ]
        return custom_urls + urls

    def publish_view(self, request, pk):
        """
        Special view for handling publishing of markets.  Checks the can_publish permission, and redirects to the main
        markets list upon success
        """

        if not request.user.has_perm('markets.can_publish'):
            return HttpResponseForbidden()

        try:
            market = get_object_or_404(Market, pk=pk)
            market.validate_for_publishing()
            market.publish(request.user)
            self.message_user(request, "Market published.", level=messages.SUCCESS)
        except ValidationError as errors:
            self.message_user(request, "Failed to publish Market.", level=messages.ERROR)
            for error in errors:
                self.message_user(request, error, level=messages.ERROR)

        url = reverse('admin:markets_market_change', args=[pk])
        return HttpResponseRedirect("{0}?publish".format(url))

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Override the widgets for ManyToMany fields, to set to either a left-to-right filter widget (if specified in the
        list above), or a multiple-checkbox widget otherwise
        """

        kwargs['widget'] = forms.CheckboxSelectMultiple()

        return super(admin.ModelAdmin, self).formfield_for_manytomany(db_field, request=request, **kwargs)

    def response_post_save_change(self, request, obj):

        # Default response
        resp = super().response_post_save_change(request, obj)

        # Check that you clicked the button `_publish`
        if '_publish' in request.POST:
            url = reverse('admin:publish_market', args=[obj.pk])
            return HttpResponseRedirect(url)
        else:
            # Otherwise, just use default behavior
            return resp


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    form = LogoAdminForm
