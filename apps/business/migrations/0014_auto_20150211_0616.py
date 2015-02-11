# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0013_auto_20150211_0512'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'verbose_name_plural': 'businesses'},
        ),
        migrations.AlterModelOptions(
            name='businessmembership',
            options={},
        ),
    ]
