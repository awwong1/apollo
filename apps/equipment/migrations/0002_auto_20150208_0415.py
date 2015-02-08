# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='auth_id',
        ),
        migrations.AddField(
            model_name='service',
            name='activation_id',
            field=models.CharField(default=b'', help_text=b'What is the Python re module activation regex for this service?', unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
