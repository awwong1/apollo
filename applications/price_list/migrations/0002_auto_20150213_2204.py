# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitypricelistitem',
            name='description',
            field=models.TextField(help_text=b'What is the description of this price list item?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timepricelistitem',
            name='description',
            field=models.TextField(help_text=b'What is the description of this price list item?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unitpricelistitem',
            name='description',
            field=models.TextField(help_text=b'What is the description of this price list item?'),
            preserve_default=True,
        ),
    ]
