# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0003_bundle'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceListBundle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percent_discount', models.PositiveSmallIntegerField(help_text=b'What percent discount should be applied for this bundle? (Value between 0 and 100 percent)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('activity_bundle_items', models.ManyToManyField(help_text=b'Which activity items are included in this bundle?', to='price_list.ActivityPriceListItem')),
                ('price_list', models.ForeignKey(help_text=b'Which price list does this bundle belong to?', to='price_list.PriceList')),
                ('time_bundle_items', models.ManyToManyField(help_text=b'Which time items are included in this bundle?', to='price_list.TimePriceListItem')),
                ('unit_bundle_items', models.ManyToManyField(help_text=b'Which unit items are included in this bundle?', to='price_list.UnitPriceListItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='activity_bundle_items',
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='price_list',
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='time_bundle_items',
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='unit_bundle_items',
        ),
        migrations.DeleteModel(
            name='Bundle',
        ),
    ]
