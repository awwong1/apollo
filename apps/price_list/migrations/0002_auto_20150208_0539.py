# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitpricelistitem',
            name='unit_name',
        ),
        migrations.AlterField(
            model_name='activitypricelistitem',
            name='description',
            field=models.TextField(help_text=b'What is the description of this price list item?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activitypricelistitem',
            name='item_uuid',
            field=models.CharField(default=uuid.uuid4, help_text=b'What is the item specific UUID for this price list item? Must be unique per price list.', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activitypricelistitem',
            name='price_list',
            field=models.ForeignKey(related_name='activitypricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item apply to?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activitypricelistitem',
            name='unit_measurement',
            field=models.CharField(default=b'Unit', help_text=b"What is the unit measurement for this activity? (Example: 'hour' or 'kb')", max_length=15),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timepricelistitem',
            name='description',
            field=models.TextField(help_text=b'What is the description of this price list item?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timepricelistitem',
            name='item_uuid',
            field=models.CharField(default=uuid.uuid4, help_text=b'What is the item specific UUID for this price list item? Must be unique per price list.', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timepricelistitem',
            name='price_list',
            field=models.ForeignKey(related_name='timepricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item apply to?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unitpricelistitem',
            name='description',
            field=models.TextField(help_text=b'What is the description of this price list item?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unitpricelistitem',
            name='item_uuid',
            field=models.CharField(default=uuid.uuid4, help_text=b'What is the item specific UUID for this price list item? Must be unique per price list.', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unitpricelistitem',
            name='price_list',
            field=models.ForeignKey(related_name='unitpricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item apply to?'),
            preserve_default=True,
        ),
    ]
