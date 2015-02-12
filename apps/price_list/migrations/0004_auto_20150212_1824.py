# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0003_auto_20150212_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricelist',
            options={'ordering': ['-id'], 'verbose_name': 'Price List', 'verbose_name_plural': 'Price Lists'},
        ),
    ]
