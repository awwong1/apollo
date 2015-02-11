# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terms_of_service', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='termsofservice',
            old_name='date_created',
            new_name='last_modified',
        ),
    ]
