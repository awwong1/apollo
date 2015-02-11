# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0011_remove_business_created_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'default_permissions': ('add', 'change'), 'verbose_name_plural': 'businesses', 'permissions': (('add_businessmembership', 'Can add a business membership for this business'), ('change_businessmembership', 'Can add a business membership for this business'), ('delete_businessmembership', 'Can add a business membership for this business'))},
        ),
        migrations.AlterModelOptions(
            name='businessmembership',
            options={'default_permissions': ()},
        ),
    ]
