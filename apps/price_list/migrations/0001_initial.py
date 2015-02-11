# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('terms_of_service', '0001_initial'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityPriceListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_uuid', models.CharField(default=uuid.uuid4, help_text=b'What is the item specific UUID for this price list item? Must be unique per price list.', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')])),
                ('name', models.CharField(help_text=b'What is the name of this price list item?', max_length=60)),
                ('description', models.TextField(help_text=b'What is the description of this price list item?', blank=True)),
                ('price_per_unit', models.DecimalField(help_text=b'How much does this price list item cost per unit measurement?', max_digits=7, decimal_places=2)),
                ('unit_measurement', models.CharField(default=b'Unit', help_text=b"What is the unit measurement for this activity? (Example: 'hour' or 'kb')", max_length=15)),
                ('equipment', models.ManyToManyField(help_text=b'Which pieces of equipment does this price list item associate with? (May be empty)', to='equipment.Equipment', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'PR', help_text=b'What is the status of this price list?', max_length=2, choices=[(b'PR', b'Pre-Release'), (b'RE', b'Release')])),
                ('name', models.CharField(help_text=b'What is the name of this price list?', max_length=255)),
                ('description', models.TextField(help_text=b'What is the description for this price list?')),
            ],
            options={
                'verbose_name': 'Price List',
                'verbose_name_plural': 'Price Lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PriceListBundle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percent_discount', models.PositiveSmallIntegerField(help_text=b'What percent discount should be applied for this bundle? (Value between 0 and 100 percent)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('activity_bundle_items', models.ManyToManyField(help_text=b'Which activity items are included in this bundle?', to='price_list.ActivityPriceListItem')),
                ('price_list', models.ForeignKey(help_text=b'Which price list does this bundle belong to?', to='price_list.PriceList')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimePriceListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_uuid', models.CharField(default=uuid.uuid4, help_text=b'What is the item specific UUID for this price list item? Must be unique per price list.', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')])),
                ('name', models.CharField(help_text=b'What is the name of this price list item?', max_length=60)),
                ('description', models.TextField(help_text=b'What is the description of this price list item?', blank=True)),
                ('price_per_time', models.DecimalField(help_text=b'How much does this price list item cost per unit of time?', max_digits=7, decimal_places=2)),
                ('unit_time', models.PositiveIntegerField(help_text=b'What is the unit of time measurement?', choices=[(60, b'Hour'), (1440, b'Day')])),
                ('equipment', models.ManyToManyField(help_text=b'Which pieces of equipment does this price list item associate with? (May be empty)', to='equipment.Equipment', null=True, blank=True)),
                ('price_list', models.ForeignKey(related_name='timepricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item belong in?')),
                ('services', models.ManyToManyField(help_text=b'Which services does this price list item associate with? (May be empty)', to='equipment.Service', null=True, blank=True)),
                ('terms_of_service', models.ForeignKey(help_text=b'Which terms of service must a user agree to before using purchasing this price list item?', to='terms_of_service.TermsOfService')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitPriceListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_uuid', models.CharField(default=uuid.uuid4, help_text=b'What is the item specific UUID for this price list item? Must be unique per price list.', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')])),
                ('name', models.CharField(help_text=b'What is the name of this price list item?', max_length=60)),
                ('description', models.TextField(help_text=b'What is the description of this price list item?', blank=True)),
                ('price_per_unit', models.DecimalField(help_text=b'How much does this price list item cost?', max_digits=7, decimal_places=2)),
                ('equipment', models.ManyToManyField(help_text=b'Which pieces of equipment does this price list item associate with? (May be empty)', to='equipment.Equipment', null=True, blank=True)),
                ('price_list', models.ForeignKey(related_name='unitpricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item belong in?')),
                ('services', models.ManyToManyField(help_text=b'Which services does this price list item associate with? (May be empty)', to='equipment.Service', null=True, blank=True)),
                ('terms_of_service', models.ForeignKey(help_text=b'Which terms of service must a user agree to before using purchasing this price list item?', to='terms_of_service.TermsOfService')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='unitpricelistitem',
            unique_together=set([('price_list', 'item_uuid')]),
        ),
        migrations.AlterIndexTogether(
            name='unitpricelistitem',
            index_together=set([('price_list', 'item_uuid')]),
        ),
        migrations.AlterUniqueTogether(
            name='timepricelistitem',
            unique_together=set([('price_list', 'item_uuid')]),
        ),
        migrations.AlterIndexTogether(
            name='timepricelistitem',
            index_together=set([('price_list', 'item_uuid')]),
        ),
        migrations.AddField(
            model_name='pricelistbundle',
            name='time_bundle_items',
            field=models.ManyToManyField(help_text=b'Which time items are included in this bundle?', to='price_list.TimePriceListItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pricelistbundle',
            name='unit_bundle_items',
            field=models.ManyToManyField(help_text=b'Which unit items are included in this bundle?', to='price_list.UnitPriceListItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activitypricelistitem',
            name='price_list',
            field=models.ForeignKey(related_name='activitypricelistitem_set', to='price_list.PriceList', help_text=b'Which price list does this price list item belong in?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activitypricelistitem',
            name='services',
            field=models.ManyToManyField(help_text=b'Which services does this price list item associate with? (May be empty)', to='equipment.Service', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activitypricelistitem',
            name='terms_of_service',
            field=models.ForeignKey(help_text=b'Which terms of service must a user agree to before using purchasing this price list item?', to='terms_of_service.TermsOfService'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='activitypricelistitem',
            unique_together=set([('price_list', 'item_uuid')]),
        ),
        migrations.AlterIndexTogether(
            name='activitypricelistitem',
            index_together=set([('price_list', 'item_uuid')]),
        ),
    ]
