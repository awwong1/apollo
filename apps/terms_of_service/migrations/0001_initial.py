# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TermsOfService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(help_text=b'When was this terms of service created?', auto_now=True)),
                ('title', models.CharField(help_text=b'What is the title of this terms of service document?', max_length=255)),
                ('content', models.TextField(help_text=b'What is the content of this terms of service document?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
