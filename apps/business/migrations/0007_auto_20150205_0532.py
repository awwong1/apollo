# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_auto_20150205_0409'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'default_permissions': ('add', 'change', 'delete'), 'verbose_name_plural': 'businesses', 'permissions': (('add_businessmembership', 'Can add a business membership for this business'),)},
        ),
        migrations.AlterField(
            model_name='businessmembership',
            name='business',
            field=models.ForeignKey(editable=False, to='business.Business', help_text=b'Which business is part of this membership?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='businessmembership',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, help_text=b'Which user is part of this membership?'),
            preserve_default=True,
        ),
    ]
