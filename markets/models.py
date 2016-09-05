from __future__ import unicode_literals
import base64
import datetime

from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField

from geography.models import Country

# SAMPLE DATA
PLATFORM_BRAND_POSITION = (
    ('0', 'Luxury'),
    ('1', 'Mid rage'),
    ('2', 'Discount')
)

LOGISTICS_MODELS = (
    ('0', 'Dropshipping'),
    ('1', 'Warehousing'),
    ('2', 'Other')
)


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        ordering = ('name',)


class Logo(models.Model):
    name = models.CharField(max_length=200)
    _encoded_data = models.TextField()

    def base64_logo(self):
        return self._encoded_data

    def __str__(self):
        return "{0}".format(self.name)


class SupportChannel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        ordering = ('-name',)


class UploadMethod(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        ordering = ('-name',)


class Currency(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return "{0} {1}".format(self.name, self.symbol)

    class Meta:
        verbose_name_plural = "Currencies"
        ordering = ('-name',)


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        ordering = ('-name',)


class Market(models.Model):
    last_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200, null=True, blank=True)
    logo = models.ForeignKey('Logo', null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    web_address = models.URLField(max_length=200, blank=True, null=True)
    countries_served = models.ManyToManyField(Country)
    product_categories = models.ManyToManyField(ProductCategory)

    web_traffic = models.CharField(max_length=30, null=True, blank=True)
    famous_brands_on_marketplace = models.ManyToManyField(Brand, blank=True)

    customer_support_channels = models.ManyToManyField(SupportChannel, blank=True,
                                                       related_name="%(app_label)s_%(class)s_customer_related")
    seller_support_channels = models.ManyToManyField(SupportChannel, blank=True,
                                                     related_name="%(app_label)s_%(class)s_seller_related")

    customer_demographics = RichTextField(null=True, blank=True)

    marketing_merchandising = RichTextField(null=True, blank=True)

    product_details_upload = models.ManyToManyField(UploadMethod, blank=True,
                                                    verbose_name="Product Details upload process")

    payment_terms_days = models.IntegerField(null=True, blank=True)
    payment_terms_days_notes = models.CharField(max_length=200, blank=True, null=True, verbose_name='notes')

    currency_of_payments = models.ManyToManyField(Currency, blank=True)

    logistics_structure = models.CharField(choices=LOGISTICS_MODELS, max_length=1, null=True, blank=True)
    logistics_structure_notes = models.CharField(max_length=200, blank=True, null=True, verbose_name='notes')
    platform_type = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.CharField(choices=PLATFORM_BRAND_POSITION, max_length=1, null=True, blank=True)

    commission = models.CharField(max_length=10, null=True, blank=True)
    commission_notes = models.CharField(max_length=255, null=True, blank=True)

    ukti_terms = RichTextField(null=True, blank=True)

    local_bank_account_needed = models.BooleanField(default=False, verbose_name="Local Bank Account Needed")
    local_bank_account_needed_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")
    local_incorporation_needed = models.BooleanField(default=False, verbose_name="Local Incorporation Needed")
    local_incorporation_needed_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")

    exclusivity_required = models.BooleanField(default=False, verbose_name="Onboarding Requirements Exclusivity")
    exclusivity_required_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")

    translation_verbal = models.BooleanField(default=False, verbose_name="Translation Needed - Verbal")
    translation_verbal_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")
    translation_application_process = models.BooleanField(default=False,
                                                          verbose_name="Translation Needed - Application process")
    translation_application_process_notes = models.CharField(max_length=255, null=True, blank=True,
                                                             verbose_name="Notes")

    translation_product_content = models.BooleanField(default=False,
                                                      verbose_name="Translation Needed - product content")

    translation_product_content_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")
    translation_customer_service = models.BooleanField(default=False,
                                                       verbose_name="Translation Needed - Customer Service")
    translation_customer_service_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")

    payment_terms_rate_fixed = models.BooleanField(default=False, verbose_name="Payment Terms - Exchange rate fixed")
    payment_terms_rate_fixed_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")
    registration_fees = models.BooleanField(default=False, verbose_name="Pricing/Fees - Registration")
    registration_fees_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")
    fee_per_listing = models.BooleanField(default=False, verbose_name="Pricing/Fees - Fee per Listing")
    fee_per_listing_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")
    membership_fees = models.BooleanField(default=False, verbose_name="Pricing/Fees - Recurring membership fees")
    membership_fees_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")

    shipping_tracking_required = models.BooleanField(default=False, verbose_name="Shipping Tracking Required")
    shipping_tracking_required_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")
    local_return_address_required = models.BooleanField(default=False, verbose_name="Local return address required?")
    local_return_address_required_notes = models.CharField(max_length=255, null=True, blank=True, verbose_name="Notes")

    def __str__(self):
        return "{0}".format(self.name)

    class Meta:
        ordering = ('-name',)
