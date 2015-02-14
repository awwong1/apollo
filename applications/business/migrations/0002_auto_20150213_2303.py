# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='city',
            field=models.CharField(help_text=b'Which city is this business located in?', max_length=60),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='business',
            name='country',
            field=models.CharField(help_text=b'Which country is this business located in?', max_length=60),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='business',
            name='region',
            field=models.CharField(help_text=b'Which province, territory, or region is this business located in?', max_length=60),
            preserve_default=True,
        ),
    ]
