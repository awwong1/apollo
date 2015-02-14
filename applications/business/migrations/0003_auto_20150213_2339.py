# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20150213_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='address_2',
            field=models.CharField(help_text=b'What is the address of this business? (Continued)', max_length=60, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='business',
            name='region',
            field=models.CharField(help_text=b'Which province, territory, or region is this business located in?', max_length=60, blank=True),
            preserve_default=True,
        ),
    ]
