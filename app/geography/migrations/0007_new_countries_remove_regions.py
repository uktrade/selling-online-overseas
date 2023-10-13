# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-01 08:33
from __future__ import unicode_literals

import os
import csv

from django.db import migrations, connections

from core.utils import fix_model_index


fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
csvfilename = os.path.join(fixture_dir, '0007_country-records.csv')

map_new_countries_to_old = {
    'Czechia': 'Czech Republic'
}


def load_fixture(apps, schema_editor):

    if connections.databases['default']['NAME'][:4] == 'test':
        return

    new_country_names = []
    Country = apps.get_model('geography', 'Country')
    fix_model_index(Country)

    with open(csvfilename, 'rt') as csvfile:
        # Loop over the CSV file getting the new countries
        reader = csv.reader(csvfile)
        for row in reader:
            if row[9]:
                # These are old countries with an expiration date
                continue

            # Get the new country name, and the alternate name
            country_name = row[5]
            country_alternate_name = row[6]
            # Append to a list of new names, so we can remove all unmatched old ones later
            new_country_names.append(country_name)

            if country_name in map_new_countries_to_old:
                # Get the old country out of the DB, and change it's name
                old_country_name = map_new_countries_to_old[country_name]
                country = Country.objects.get(name=old_country_name)
                country.name = country_name
            else:
                # Get or create a country with the new name, set it's alternate name
                country, created = Country.objects.get_or_create(name=country_name)

            # Set the country's alternate name
            country.alternate_name = country_alternate_name
            country.save()
   
    # Special migration for 'Global' country, all markets linked to this, to ALL new individual countries
    all_new = Country.objects.filter(name__in=new_country_names)
    Market = apps.get_model('markets', 'Market')

    markets = Market.objects.filter(countries_served=Country.objects.filter(name='Global')[0])
    for market in markets:
        market.countries_served.set(all_new)
        market.save()

    # Now delete all old countries that aren't in the new list
    redundant = Country.objects.exclude(name__in=new_country_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0006_country_alternate_name'),
        ('markets', '0048_auto_20161104_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='region',
        ),
        migrations.RunPython(load_fixture),
        migrations.DeleteModel(
            name='Region',
        ),
    ]
