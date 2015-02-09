# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0010_business_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='created_by',
        ),
    ]
