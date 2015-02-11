# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0012_auto_20150210_2349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'default_permissions': ('add', 'change'), 'verbose_name_plural': 'businesses'},
        ),
        migrations.AlterModelOptions(
            name='businessmembership',
            options={'default_permissions': ('add', 'change')},
        ),
        migrations.AlterIndexTogether(
            name='businessmembership',
            index_together=set([('user', 'business')]),
        ),
    ]
