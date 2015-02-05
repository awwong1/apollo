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
                ('city', models.ForeignKey(help_text=b'Which city does this business belong in?', to='cities_light.City')),
            ],
            options={
                'verbose_name_plural': 'businesses',
                'permissions': ('edit_business_instance', 'Can edit this business instance'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BusinessMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_accepted', models.BooleanField(default=False, help_text=b'Has the user accepted this membership?')),
                ('business_accepted', models.BooleanField(default=False, help_text=b'Has the business accepted this membership?')),
                ('business_administrator', models.BooleanField(default=False, help_text=b'Is this user an administrator of this business?')),
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
        migrations.AlterIndexTogether(
            name='businessmembership',
            index_together=set([('user', 'business')]),
        ),
    ]
