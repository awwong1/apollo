# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0014_auto_20150211_0616'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='businessmembership',
            index_together=set([]),
        ),
    ]
