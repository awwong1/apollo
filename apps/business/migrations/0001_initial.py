# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '0003_auto_20141120_0342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'What is the name of this business?', unique=True, max_length=60)),
                ('description', models.TextField(help_text=b'What is the description for this business?', blank=True)),
                ('address_1', models.CharField(help_text=b'What is the address of this business?', max_length=60)),
                ('address_2', models.CharField(help_text=b'What is the address of this business?', max_length=60, blank=True)),
                ('postal_code', models.CharField(help_text=b'What is the postal code of this business?', max_length=6)),
                ('city', models.ForeignKey(blank=True, to='cities_light.City', help_text=b'Which city does this business belong in?', null=True)),
            ],
            options={
                'verbose_name_plural': 'businesses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BusinessMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business', models.ForeignKey(help_text=b'Which business is part of this membership? Cannot be edited once membership is created.', to='business.Business')),
                ('user', models.ForeignKey(help_text=b'Which user is part of this membership? Cannot be edited once membership is created.', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='businessmembership',
            unique_together=set([('user', 'business')]),
        ),
    ]
