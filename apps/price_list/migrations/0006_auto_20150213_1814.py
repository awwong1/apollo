# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0005_auto_20150212_2239'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pricelistitemservice',
            unique_together=set([('price_list', 'item_uuid', 'service')]),
        ),
    ]
