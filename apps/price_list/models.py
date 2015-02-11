from copy import copy
from uuid import uuid4
from decimal import Decimal
import re
from apollo.choices import PRICE_LIST_STATUS_TYPES, PRICE_LIST_PRE_RELEASE, TIME_MEASUREMENT_CHOICES
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models


class PriceList(models.Model):
    """
    Model for the price list object.
    """
    status = models.CharField(
        max_length=2, choices=PRICE_LIST_STATUS_TYPES, default=PRICE_LIST_PRE_RELEASE,
        help_text="What is the status of this price list?"
    )
    name = models.CharField(
        max_length=255, help_text="What is the name of this price list?"
    )
    description = models.TextField(
        help_text="What is the description for this price list?"
    )

    class Meta:
        verbose_name = "Price List"
        verbose_name_plural = "Price Lists"

    def clean(self):
        if self.pk is not None:
            price_list_existing = PriceList.objects.get(pk=self.pk)
            if price_list_existing.status != PRICE_LIST_PRE_RELEASE:
                raise ValidationError("Price lists cannot be edited once released.")

    def create_next_price_list(self, name=None, description=None):
        """
        Creates a new price list from this price list, including all of the associated price list items.

        deepcopy didn't work, according to my unit tests:
            next_price_list = deepcopy(self)
            next_price_list.pk = None
            next_price_list.save()
            return next_price_list
        failed to generate the price list item references
        """
        next_price_list = copy(self)
        next_price_list.pk = None
        next_price_list.status = PRICE_LIST_PRE_RELEASE
        if name:
            next_price_list.name = name
        if description:
            next_price_list.description = description
        next_price_list.save()
        for activity_item in self.activitypricelistitem_set.all():
            next_activity_item = copy(activity_item)
            next_activity_item.price_list = next_price_list
            next_activity_item.pk = None
            next_activity_item.save()
        for time_item in self.timepricelistitem_set.all():
            next_time_item = copy(time_item)
            next_time_item.price_list = next_price_list
            next_time_item.pk = None
            next_time_item.save()
        for unit_item in self.unitpricelistitem_set.all():
            next_unit_item = copy(unit_item)
            next_unit_item.price_list = next_price_list
            next_unit_item.pk = None
            next_unit_item.save()
        for bundle in self.pricelistbundle_set.all():
            bundle.create_bundle_for_price_list(next_price_list)
        return next_price_list

    def __str__(self):
        return "({status}) {0}: {1}".format(self.pk, self.name, status=self.get_status_display())

    def __unicode__(self):
        return u"({status}) {0}: {1}".format(self.pk, self.name, status=self.get_status_display())


class AbstractPriceListItem(models.Model):
    """
    Abstract model for the Price List Item object.
    """
    price_list = models.ForeignKey(
        'PriceList', related_name='%(class)s_set',
        help_text="Which price list does this price list item belong in?"
    )
    item_uuid = models.CharField(
        max_length=36, default=uuid4,
        help_text="What is the item specific UUID for this price list item? Must be unique per price list.",
        validators=[RegexValidator(regex="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")]
    )
    name = models.CharField(
        max_length=60,
        help_text="What is the name of this price list item?"
    )
    description = models.TextField(
        help_text="What is the description of this price list item?", blank=True
    )
    equipment = models.ManyToManyField(
        'equipment.Equipment', null=True, blank=True,
        help_text="Which pieces of equipment does this price list item associate with? (May be empty)"
    )
    services = models.ManyToManyField(
        'equipment.Service', null=True, blank=True,
        help_text="Which services does this price list item associate with? (May be empty)"
    )
    terms_of_service = models.ForeignKey(
        'terms_of_service.TermsOfService',
        help_text="Which terms of service must a user agree to before using purchasing this price list item?"
    )

    class Meta:
        abstract = True
        unique_together = ('price_list', 'item_uuid')
        index_together = ('price_list', 'item_uuid')

    def clean(self):
        if self.price_list.status != PRICE_LIST_PRE_RELEASE:
            raise ValidationError(
                "Price list has been released. Cannot modify associated price list items."
            )
        if re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", self.item_uuid) is None:
            raise ValidationError(
                "Invalid UUID provided, please ensure proper uuid format"
            )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name


class ActivityPriceListItem(AbstractPriceListItem):
    """
    Model for activity based price list items. Pricing is based by price per unit over unit measurement.
    """
    price_per_unit = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text="How much does this price list item cost per unit measurement?"
    )
    unit_measurement = models.CharField(
        max_length=15, default="Unit",
        help_text="What is the unit measurement for this activity? (Example: 'hour' or 'kb')"
    )


class TimePriceListItem(AbstractPriceListItem):
    """
    Model for time based price list items. Pricing is by price per number of minutes.
    """
    price_per_time = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text="How much does this price list item cost per unit of time?"
    )
    unit_time = models.PositiveIntegerField(
        choices=TIME_MEASUREMENT_CHOICES,
        help_text="What is the unit of time measurement?"
    )


class UnitPriceListItem(AbstractPriceListItem):
    """
    Model for unit based price list items. Pricing is price per unit.
    Suitable for flat rate charges, such as a charge to deliver a piece of equipment/part
    """
    price_per_unit = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text="How much does this price list item cost?"
    )


class PriceListBundle(models.Model):
    """
    Model for bundles within a price list. Will contain a set of price list items with an applied discount for all
    abstract items.
    """
    price_list = models.ForeignKey(
        'PriceList', help_text="Which price list does this bundle belong to?"
    )
    activity_bundle_items = models.ManyToManyField(
        ActivityPriceListItem, help_text="Which activity items are included in this bundle?"
    )
    time_bundle_items = models.ManyToManyField(
        TimePriceListItem, help_text="Which time items are included in this bundle?"
    )
    unit_bundle_items = models.ManyToManyField(
        UnitPriceListItem, help_text="Which unit items are included in this bundle?"
    )
    percent_discount = models.PositiveSmallIntegerField(
        help_text="What percent discount should be applied for this bundle? (Value between 0 and 100 percent)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def create_bundle_for_price_list(self, price_list):
        """
        Method for creating a new bundle from an old bundle with reference to a new price list.
        """
        next_bundle = copy(self)
        next_bundle.pk = None
        next_bundle.price_list = price_list
        next_bundle.save()
        for activity_item in self.activity_bundle_items.all():
            next_act_item = ActivityPriceListItem.objects.get(item_uuid=activity_item.item_uuid, price_list=price_list)
            next_bundle.activity_bundle_items.add(next_act_item)
        for time_item in self.time_bundle_items.all():
            next_time_item = TimePriceListItem.objects.get(item_uuid=time_item.item_uuid, price_list=price_list)
            next_bundle.time_bundle_items.add(next_time_item)
        for unit_item in self.unit_bundle_items.all():
            next_unit_item = UnitPriceListItem.objects.get(item_uuid=unit_item.item_uuid, price_list=price_list)
            next_bundle.unit_bundle_items.add(next_unit_item)
        next_bundle.save()
        return next_bundle

    def get_bundle_items_cost(self, item_classes=[ActivityPriceListItem, TimePriceListItem, UnitPriceListItem]):
        """
        Returns a dictionary of the bundle items and their new cost after the bundle percent discount is applied
        :return: Dictionary[Activity/Time/Unit Price List Item] = (Cost Tuple)/Cost Value
        """
        multiplier = Decimal((100.0 - self.percent_discount) / 100.0)
        data_dict = dict()
        for class_type in item_classes:
            if class_type == ActivityPriceListItem:
                for activity_item in self.activity_bundle_items.all():
                    data_dict[activity_item] = (
                        activity_item.price_per_unit * multiplier, activity_item.unit_measurement
                    )
            elif class_type == TimePriceListItem:
                for time_item in self.time_bundle_items.all():
                    data_dict[time_item] = (
                        time_item.price_per_time * multiplier, time_item.unit_time
                    )
            elif class_type == UnitPriceListItem:
                for unit_item in self.unit_bundle_items.all():
                    data_dict[unit_item] = unit_item.price_per_unit * multiplier
        return data_dict

    def clean(self):
        if self.price_list.status != PRICE_LIST_PRE_RELEASE:
            raise ValidationError("Price list has been released. Cannot modify associated bundle.")
        if self.percent_discount < 0:
            raise ValidationError("Bundle discount cannot be below 0%.")
        elif self.percent_discount > 100:
            raise ValidationError("Bundle discount percent cannot be above 100%.")

    def __str__(self):
        return "%(price_list)s Bundle: %(bundle_pk)s" % {'price_list': self.price_list.name, 'bundle_pk': self.pk}

    def __unicode__(self):
        return u"%(price_list)s Bundle: %(bundle_pk)s" % {'price_list': self.price_list.name, 'bundle_pk': self.pk}
