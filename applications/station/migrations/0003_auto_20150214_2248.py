# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0002_station_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='type',
            field=models.CharField(default=b'RG', help_text=b'What type of station is this?', max_length=2, choices=[(b'RG', b'Rig'), (b'OF', b'Office'), (b'OT', b'Other')]),
            preserve_default=True,
        ),
    ]
