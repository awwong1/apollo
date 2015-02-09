# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0004_auto_20150209_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitypricelistitem',
            name='price_list',
            field=models.ForeignKey(related_name='activitypricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item belong in?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timepricelistitem',
            name='price_list',
            field=models.ForeignKey(related_name='timepricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item belong in?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unitpricelistitem',
            name='price_list',
            field=models.ForeignKey(related_name='unitpricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item belong in?'),
            preserve_default=True,
        ),
    ]
