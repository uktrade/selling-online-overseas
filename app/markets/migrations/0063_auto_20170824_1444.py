# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-24 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0062_auto_20170726_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logo',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '400x302', adapt_rotation=False, allow_fullsize=False,
                                                        free_crop=False,
                                                        help_text='Use cropping tool to cut the image to the right\
                                                                   format. Always leave enough white space around the\
                                                                   edges and try to keep the largest possible size for\
                                                                   good image quality.', hide_image_field=False,
                                                        size_warning=False, verbose_name='cropping'),
        ),
        migrations.AlterField(
            model_name='logo',
            name='image',
            field=models.ImageField(help_text="After choosing an image to upload click 'Save' to access the 'Cropping'\
                                               tool and edit the image", null=True, upload_to=''),
        ),
    ]
