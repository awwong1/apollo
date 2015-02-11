# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price_list', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityBundleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_price_list_item', models.ForeignKey(help_text=b'Which activity price list item does this bundle item represent?', to='price_list.ActivityPriceListItem')),
                ('bundle', models.ForeignKey(help_text=b'Which bundle does this bundle price list item belong to?', to='price_list.PriceListBundle')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeBundleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bundle', models.ForeignKey(help_text=b'Which bundle does this bundle price list item belong to?', to='price_list.PriceListBundle')),
                ('time_price_list_item', models.ForeignKey(help_text=b'Which time price list item does this bundle item represent?', to='price_list.TimePriceListItem')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnitBundleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bundle', models.ForeignKey(help_text=b'Which bundle does this bundle price list item belong to?', to='price_list.PriceListBundle')),
                ('unit_price_list_item', models.ForeignKey(help_text=b'Which unit price list item does this bundle item represent?', to='price_list.UnitPriceListItem')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='pricelistbundle',
            name='activity_bundle_items',
        ),
        migrations.RemoveField(
            model_name='pricelistbundle',
            name='time_bundle_items',
        ),
        migrations.RemoveField(
            model_name='pricelistbundle',
            name='unit_bundle_items',
        ),
        migrations.AddField(
            model_name='pricelistbundle',
            name='description',
            field=models.TextField(default=b'', help_text=b'What is the description of this bundle?', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pricelistbundle',
            name='name',
            field=models.CharField(default=b'Bundle', help_text=b'What is the name of this bundle?', max_length=100),
            preserve_default=True,
        ),
    ]
