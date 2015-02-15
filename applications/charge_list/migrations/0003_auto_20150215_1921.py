# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charge_list', '0002_auto_20150215_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitycharge',
            name='price_per_unit_override',
            field=models.DecimalField(help_text=b'How much does this price list item cost per unit measurement? (Overrides original price)', null=True, max_digits=7, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timecharge',
            name='price_per_time_override',
            field=models.DecimalField(help_text=b'How much does this price list item cost per unit of time?', null=True, max_digits=7, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timecharge',
            name='time_end',
            field=models.DateTimeField(help_text=b'When does this time charge end billing?', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timecharge',
            name='time_start',
            field=models.DateTimeField(help_text=b'When does this time charge begin billing?', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unitcharge',
            name='price_per_unit_override',
            field=models.DecimalField(help_text=b'How much does this price list item cost?', null=True, max_digits=7, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
