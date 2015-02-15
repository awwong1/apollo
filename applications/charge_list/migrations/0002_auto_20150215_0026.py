# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charge_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitycharge',
            name='services_active',
            field=models.BooleanField(default=True, help_text=b"Are these charge's associated services enabled?"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timecharge',
            name='services_active',
            field=models.BooleanField(default=True, help_text=b"Are these charge's associated services enabled?"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='unitcharge',
            name='services_active',
            field=models.BooleanField(default=True, help_text=b"Are these charge's associated services enabled?"),
            preserve_default=True,
        ),
    ]
