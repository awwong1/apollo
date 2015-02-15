# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='activate',
            field=models.ForeignKey(blank=True, to='assets.Equipment', help_text=b'Which equipment does this service activate?', null=True),
            preserve_default=True,
        ),
    ]
