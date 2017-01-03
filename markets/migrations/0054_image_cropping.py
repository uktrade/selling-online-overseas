# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-22 14:37
from __future__ import unicode_literals

import base64
import os

from django.conf import settings
from django.db import migrations, models
import image_cropping.fields
from PIL import Image


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0053_load_intial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='logo',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '400x302', adapt_rotation=False, allow_fullsize=False,
                                                        free_crop=False, help_text=None, hide_image_field=False,
                                                        size_warning=False, verbose_name='cropping'),
        ),
        migrations.AddField(
            model_name='logo',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
