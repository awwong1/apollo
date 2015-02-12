# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0004_auto_20150212_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricelistitemequipment',
            name='item_uuid',
            field=models.CharField(help_text=b'What is the price list item specific UUID?', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pricelistitemequipment',
            name='price_list',
            field=models.ForeignKey(help_text=b'Which price list does this equipment item reference?', to='price_list.PriceList'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pricelistitemservice',
            name='item_uuid',
            field=models.CharField(help_text=b'What is the price list item specific UUID?', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pricelistitemservice',
            name='price_list',
            field=models.ForeignKey(help_text=b'Which price list does this service item reference?', to='price_list.PriceList'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pricelistitemequipment',
            unique_together=set([('price_list', 'item_uuid', 'equipment')]),
        ),
    ]
