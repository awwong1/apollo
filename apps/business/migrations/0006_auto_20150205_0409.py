# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_auto_20150205_0033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'default_permissions': ('add', 'change', 'delete'), 'verbose_name_plural': 'businesses', 'permissions': (('add_business_membership', 'Can add a business membership for this business'),)},
        ),
        migrations.AlterModelOptions(
            name='businessmembership',
            options={'default_permissions': ('change', 'delete')},
        ),
        migrations.RemoveField(
            model_name='businessmembership',
            name='business_accepted',
        ),
        migrations.RemoveField(
            model_name='businessmembership',
            name='user_accepted',
        ),
    ]
