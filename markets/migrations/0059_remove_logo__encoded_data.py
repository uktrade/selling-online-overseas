# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-22 14:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0058_image_cropping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logo',
            name='_encoded_data',
        ),
    ]
