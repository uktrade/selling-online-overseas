# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 12:37
from __future__ import unicode_literals

from django.db import migrations


def move_countries_and_regions(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return

    OrigRegion = apps.get_model('markets', 'Region')
    OrigCountry = apps.get_model('markets', 'Country')
    NewRegion = apps.get_model('geography', 'Region')
    NewCountry = apps.get_model('geography', 'Country')

    for region in OrigRegion.objects.all():
        new_region = NewRegion.objects.create(name=region.name)
        for country in region.country_set.all():
            NewCountry.objects.create(name=country.name, region=new_region)
            country.delete()
        region.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0005_market_famous_brands_on_marketplace'),
        ('geography', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(move_countries_and_regions),
    ]
