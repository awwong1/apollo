# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'What is the name of this business?', unique=True, max_length=60)),
                ('description', models.TextField(help_text=b'What is the description for this business?', blank=True)),
                ('address_1', models.CharField(help_text=b'What is the address of this business?', max_length=60)),
                ('address_2', models.CharField(help_text=b'What is the address of this business? (Continued)', max_length=60, blank=True)),
                ('country', models.CharField(help_text=b'Which country is this business located in?', max_length=60)),
                ('region', models.CharField(help_text=b'Which province, territory, or region is this business located in?', max_length=60, blank=True)),
                ('city', models.CharField(help_text=b'Which city is this business located in?', max_length=60)),
                ('postal_code', models.CharField(help_text=b'What is the postal/zip code of this business?', max_length=6)),
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
                ('business', models.ForeignKey(help_text=b'Which business is part of this membership?', to='business.Business')),
                ('user', models.ForeignKey(help_text=b'Which user is part of this membership?', to=settings.AUTH_USER_MODEL)),
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
