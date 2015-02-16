# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0001_initial'),
        ('price_list', '0001_initial'),
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityCharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_modified', models.DateTimeField(help_text=b'When was this charge list modified?', auto_now=True)),
                ('services_active', models.BooleanField(default=True, help_text=b"Are these charge's associated services enabled?")),
                ('price_per_unit_override', models.DecimalField(help_text=b'How much does this price list item cost per unit measurement? (Overrides original price)', null=True, max_digits=7, decimal_places=2, blank=True)),
                ('billing_business', models.ForeignKey(help_text=b'Which business is this charge billed to?', to='business.Business')),
            ],
            options={
                'ordering': ['-pk'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActivityChargeActivityCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_count', models.PositiveIntegerField(help_text=b'How many units of activity is being applied to this activity charge?', validators=[django.core.validators.MinValueValidator(1)])),
                ('last_modified', models.DateTimeField(help_text=b'When was this activity last created/modified?', auto_now=True)),
                ('activity_charge', models.ForeignKey(help_text=b'Which activity charge is this activity charge activity count applied to?', to='charge_list.ActivityCharge')),
            ],
            options={
                'ordering': ['-pk'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChargeList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'OP', help_text=b'What is the status of this charge list?', max_length=2, choices=[(b'OP', b'Open'), (b'CP', b'Closed (Pending Payment)'), (b'CR', b'Closed')])),
                ('price_list', models.ForeignKey(help_text=b'Which price list does this charge list reference?', to='price_list.PriceList')),
                ('station', models.ForeignKey(help_text=b'Which station does this charge list reference?', to='station.Station')),
            ],
            options={
                'ordering': ['-pk'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeCharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_modified', models.DateTimeField(help_text=b'When was this charge list modified?', auto_now=True)),
                ('services_active', models.BooleanField(default=True, help_text=b"Are these charge's associated services enabled?")),
                ('price_per_time_override', models.DecimalField(help_text=b'How much does this price list item cost per unit of time?', null=True, max_digits=7, decimal_places=2, blank=True)),
                ('time_start', models.DateTimeField(help_text=b'When does this time charge begin billing?', null=True, blank=True)),
                ('time_end', models.DateTimeField(help_text=b'When does this time charge end billing?', null=True, blank=True)),
                ('billing_business', models.ForeignKey(help_text=b'Which business is this charge billed to?', to='business.Business')),
                ('charge_list', models.ForeignKey(help_text=b'Which charge list does this charge list item reference?', to='charge_list.ChargeList')),
                ('price_list_item', models.ForeignKey(help_text=b'Which time price list item does this charge list item reference', to='price_list.TimePriceListItem')),
            ],
            options={
                'ordering': ['-pk'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitCharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_modified', models.DateTimeField(help_text=b'When was this charge list modified?', auto_now=True)),
                ('services_active', models.BooleanField(default=True, help_text=b"Are these charge's associated services enabled?")),
                ('price_per_unit_override', models.DecimalField(help_text=b'How much does this price list item cost?', null=True, max_digits=7, decimal_places=2, blank=True)),
                ('billing_business', models.ForeignKey(help_text=b'Which business is this charge billed to?', to='business.Business')),
                ('charge_list', models.ForeignKey(help_text=b'Which charge list does this charge list item reference?', to='charge_list.ChargeList')),
                ('price_list_item', models.ForeignKey(help_text=b'Which unit price list item does this charge list item reference', to='price_list.UnitPriceListItem')),
            ],
            options={
                'ordering': ['-pk'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activitycharge',
            name='charge_list',
            field=models.ForeignKey(help_text=b'Which charge list does this charge list item reference?', to='charge_list.ChargeList'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activitycharge',
            name='price_list_item',
            field=models.ForeignKey(help_text=b'Which actvitiy price list item does this charge list item reference', to='price_list.ActivityPriceListItem'),
            preserve_default=True,
        ),
    ]
