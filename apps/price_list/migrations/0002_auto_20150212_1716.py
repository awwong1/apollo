# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('price_list', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceListItemEquipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polymorphic_item_uuid', models.CharField(help_text=b'What is the item specific UUID?', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')])),
                ('count', models.PositiveSmallIntegerField(default=1, help_text=b'How many counts of equipment should this price list item reference?', validators=[django.core.validators.MinValueValidator(1)])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('equipment', models.ForeignKey(related_name='equipment', to='assets.Equipment', help_text=b'Which equipment does this price list item map to?')),
                ('price_list', models.ForeignKey(help_text=b'Which price list does this bundle item reference?', to='price_list.PriceList')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PriceListItemService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('polymorphic_item_uuid', models.CharField(help_text=b'What is the item specific UUID?', max_length=36, validators=[django.core.validators.RegexValidator(regex=b'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')])),
                ('count', models.PositiveSmallIntegerField(default=1, help_text=b'How many counts of equipment should this price list item reference?', validators=[django.core.validators.MinValueValidator(1)])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('price_list', models.ForeignKey(help_text=b'Which price list does this bundle item reference?', to='price_list.PriceList')),
                ('service', models.ForeignKey(related_name='service', to='assets.Service', help_text=b'Which service does this price list item map to?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='activitybundleitem',
            name='activity_price_list_item',
        ),
        migrations.RemoveField(
            model_name='activitybundleitem',
            name='bundle',
        ),
        migrations.DeleteModel(
            name='ActivityBundleItem',
        ),
        migrations.RemoveField(
            model_name='pricelistbundle',
            name='price_list',
        ),
        migrations.RemoveField(
            model_name='timebundleitem',
            name='bundle',
        ),
        migrations.RemoveField(
            model_name='timebundleitem',
            name='time_price_list_item',
        ),
        migrations.DeleteModel(
            name='TimeBundleItem',
        ),
        migrations.RemoveField(
            model_name='unitbundleitem',
            name='bundle',
        ),
        migrations.DeleteModel(
            name='PriceListBundle',
        ),
        migrations.RemoveField(
            model_name='unitbundleitem',
            name='unit_price_list_item',
        ),
        migrations.DeleteModel(
            name='UnitBundleItem',
        ),
    ]
