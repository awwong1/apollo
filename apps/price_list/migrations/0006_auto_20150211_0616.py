# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0005_auto_20150209_0341'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricelist',
            options={'verbose_name': 'Price List', 'verbose_name_plural': 'Price Lists'},
        ),
    ]
