from django.contrib.admin import widgets
from django import forms
from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR
from django.template.response import SimpleTemplateResponse

from image_cropping import ImageCroppingMixin

from .models import (
    Market, Logo, PublishedMarket, SupportChannel, UploadMethod, Currency, Brand, SellerModel, LogisticsModel
)
from reversion.admin import VersionAdmin


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
            published_market = PublishedMarket.objects.get(id=market.id)

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

    list_display = ['name', 'web_address', 'is_published']
    ordering = ['name']
    readonly_fields = ['slug']
    filter_horizontal = ['operating_countries', 'product_categories', 'famous_brands_on_marketplace']
    checkbox_widget_fields = ['customer_support_channels']
    form = MarketForm

    fieldsets = (
        ('Marketplace Description', {
            'fields': (
                ('name', 'slug', 'logo'),
                'operating_countries',
                'web_address',
                'e_marketplace_description',
            )
        }),
        ('Department of International Trade tips and terms', {
            'fields': (
                'dit_special_terms',
                'dit_advisor_tip',
            )
        }),
        ('Tell me about this marketplace', {
            'fields': (
                ('number_of_registered_users', 'seller_model', 'product_positioning'),
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
                ('one_off_registration_fee', 'one_off_registration_fee_currency', 'one_off_registration_fee_notes',),
                ('membership_fees', 'membership_fees_currency', 'membership_fees_frequency',),
                ('fee_per_listing', 'fee_per_listing_notes',),
                ('commission_lower', 'commission_upper', 'commission_notes',),
                ('deposit', 'deposit_currency', 'deposit_notes',),
            )
        }),
        ('What does the marketplace need me to do?', {
            'fields': (
                ('translation_requirements', 'translation_notes'),
                ('setup_requirements', 'setup_notes'),
                ('product_exclusivity_required', 'product_exclusivity_required_notes',),
                ('product_details_upload_method', 'product_details_upload_notes',),
            )
        }),
        ('How will I get paid?', {
            'fields': (
                ('sale_to_payment_duration', 'currency_of_payments',),
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
                'explore_the_marketplace',
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

        return HttpResponseRedirect(reverse('admin:markets_market_change', args=[pk]))

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """
        Override the widgets for ManyToMany fields, to set to either a left-to-right filter widget (if specified in the
        list above), or a multiple-checkbox widget otherwise
        """

        kwargs['widget'] = forms.CheckboxSelectMultiple()

        return super(admin.ModelAdmin, self).formfield_for_manytomany(db_field, request=request, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        default = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name[-6:] == '_notes':
            default.widget.attrs = {'cols': '40', 'rows': '2'}
        return default

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
class LogoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']

    def response_add(self, request, obj, post_url_continue=None):
        if IS_POPUP_VAR in request.POST and '_continue' in request.POST:
            to_field = request.POST.get(TO_FIELD_VAR)
            if to_field:
                attr = str(to_field)
            else:
                attr = obj._meta.pk.attname
            value = obj.serializable_value(attr)
            response = SimpleTemplateResponse('admin/markets/logo/popup_response.html', {
                'value': value,
                'obj': obj,
                'reopen': True
            })
        else:
            response = super().response_add(request, obj, post_url_continue)

        return response

    def response_change(self, request, obj):
        if IS_POPUP_VAR in request.POST:
            to_field = request.POST.get(TO_FIELD_VAR)
            attr = str(to_field) if to_field else obj._meta.pk.attname
            # Retrieve the `object_id` from the resolved pattern arguments.
            value = request.resolver_match.args[0]
            new_value = obj.serializable_value(attr)
            response = SimpleTemplateResponse('admin/markets/logo/popup_response.html', {
                'action': 'change',
                'value': value,
                'obj': obj,
                'new_value': new_value,
                'reopen': '_continue' in request.POST
            })
        else:
            response = super().response_change(request, obj)

        return response
