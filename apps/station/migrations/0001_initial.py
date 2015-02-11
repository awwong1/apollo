# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0011_remove_business_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'What is the name of this station?', max_length=255)),
                ('description', models.TextField(help_text=b'What is the description for this station? How does a user get to this station?', blank=True)),
                ('uuid', models.CharField(default=uuid.uuid4, help_text=b'What is the universally unique identifier for this station?', unique=True, max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')])),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete'),
                'permissions': (('add_stationbusiness', 'Can add a station business for this station'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StationBusiness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('station_administrator', models.BooleanField(default=False, help_text=b'Is this station an administrator of this business?')),
                ('business', models.ForeignKey(help_text=b'Which business comprises this station to business membership?', to='business.Business')),
                ('station', models.ForeignKey(help_text=b'Which station comprises this station to business membership?', to='station.Station')),
            ],
            options={
                'default_permissions': ('change', 'delete'),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='stationbusiness',
            unique_together=set([('station', 'business')]),
        ),
        migrations.AlterIndexTogether(
            name='stationbusiness',
            index_together=set([('station', 'business')]),
        ),
    ]
