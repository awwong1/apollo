# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'RG', help_text=b'What type of station is this?', max_length=2, choices=[(b'RG', b'Rig'), (b'OF', b'Office'), (b'OT', b'Other')])),
                ('name', models.CharField(help_text=b'What is the name of this station?', max_length=255)),
                ('description', models.TextField(help_text=b'What is the description for this station? How does a user get to this station?', blank=True)),
                ('uuid', models.CharField(default=uuid.uuid4, help_text=b'What is the universally unique identifier for this station?', unique=True, max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StationBusiness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business', models.ForeignKey(help_text=b'Which business comprises this station to business membership?', to='business.Business')),
                ('station', models.ForeignKey(help_text=b'Which station comprises this station to business membership?', to='station.Station')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StationRental',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'DR', help_text=b'What is the status of this rental?', max_length=2, choices=[(b'DR', b'Delivery Requested'), (b'DS', b'Delivered to Station')])),
                ('last_modified', models.DateTimeField(help_text=b'When was this rental last modified?', auto_now=True)),
                ('equipment', models.ForeignKey(help_text=b'Which equipment is this rental representing?', to='assets.Equipment')),
                ('station', models.ForeignKey(help_text=b'Which station is this rental located at?', to='station.Station')),
            ],
            options={
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
