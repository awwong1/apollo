# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charge_list', '0003_auto_20150215_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitychargeactivitycount',
            options={'ordering': ['-pk']},
        ),
    ]
