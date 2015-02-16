# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'What is the name of this equipment?', unique=True, max_length=60)),
                ('description', models.TextField(help_text=b'What is the description for this equipment?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'What is the human display readable name of this service?', unique=True, max_length=255)),
                ('activation_id', models.CharField(default=b'', help_text=b'What is the Python re module activation regex for this service?', unique=True, max_length=255)),
                ('activate', models.ForeignKey(blank=True, to='assets.Equipment', help_text=b'Which equipment does this service activate?', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
