# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20150205_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='city',
            field=models.ForeignKey(blank=True, to='cities_light.City', help_text=b'Which city does this business belong in?'),
            preserve_default=True,
        ),
    ]
