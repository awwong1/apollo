# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20150213_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessmembership',
            name='business',
            field=models.ForeignKey(help_text=b'Which business is part of this membership?', to='business.Business'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='businessmembership',
            name='user',
            field=models.ForeignKey(help_text=b'Which user is part of this membership?', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
