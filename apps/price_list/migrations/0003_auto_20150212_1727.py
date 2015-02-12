# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0002_auto_20150212_1716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricelistitemequipment',
            old_name='polymorphic_item_uuid',
            new_name='item_uuid',
        ),
        migrations.RenameField(
            model_name='pricelistitemservice',
            old_name='polymorphic_item_uuid',
            new_name='item_uuid',
        ),
        migrations.RemoveField(
            model_name='activitypricelistitem',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='activitypricelistitem',
            name='services',
        ),
        migrations.RemoveField(
            model_name='pricelistitemequipment',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='pricelistitemservice',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='timepricelistitem',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='timepricelistitem',
            name='services',
        ),
        migrations.RemoveField(
            model_name='unitpricelistitem',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='unitpricelistitem',
            name='services',
        ),
    ]
