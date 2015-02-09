# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0009_auto_20150205_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, help_text=b'Which user created this business?', null=True),
            preserve_default=True,
        ),
    ]
