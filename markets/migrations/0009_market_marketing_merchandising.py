# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 16:03
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0008_market_famous_brands_on_marketplace'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='marketing_merchandising',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
