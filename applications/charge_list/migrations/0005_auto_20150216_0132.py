# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('charge_list', '0004_auto_20150215_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitychargeactivitycount',
            name='activity_count',
            field=models.PositiveIntegerField(help_text=b'How many units of activity is being applied to this activity charge?', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
