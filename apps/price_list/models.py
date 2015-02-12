from copy import copy
from uuid import uuid4
from itertools import chain
from apollo.choices import PRICE_LIST_STATUS_TYPES, PRICE_LIST_PRE_RELEASE, TIME_MEASUREMENT_CHOICES
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.shortcuts import get_object_or_404


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
        ordering = ['-id']

    def clean(self):
        """
        Only one price list may exist in the pre-release state at a time. Price lists should not change after release.
        """
        if self.pk is not None:
            price_list_existing = PriceList.objects.get(pk=self.pk)
            if price_list_existing.status != PRICE_LIST_PRE_RELEASE:
                raise ValidationError("Price lists cannot be edited once released.")
        pre_released = PriceList.objects.filter(status=PRICE_LIST_PRE_RELEASE)
        if len(pre_released) > 0 and pre_released[0].pk != self.pk:
            raise ValidationError("Only one price list may be in the pre-release state at a time!")

    def delete(self, *args, **kwargs):
        """
        Only non released price lists may be deleted.
        """
        existing = get_object_or_404(PriceList, pk=self.pk)
        if existing.status != PRICE_LIST_PRE_RELEASE:
            return
        else:
            return super(PriceList, self).delete(*args, **kwargs)

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
            raise ValidationError({'price_list': "Price list has been released. Cannot modify associated price list items."})

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name


class PriceListItemEquipment(models.Model):
    """
    Model through relation for mapping equipment to specific price list items
    """
    price_list = models.ForeignKey('PriceList', help_text="Which price list does this bundle item reference?")
    item_uuid = models.CharField(
        max_length=36, help_text="What is the item specific UUID?",
        validators=[RegexValidator(regex="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")]
    )
    equipment = models.ForeignKey(
        'assets.Equipment', related_name="equipment",
        help_text="Which equipment does this price list item map to?"
    )
    count = models.PositiveSmallIntegerField(
        help_text="How many counts of equipment should this price list item reference?",
        default=1, validators=[MinValueValidator(1)]
    )

    def clean(self):
        price_list_items = list(
            chain(self.price_list.activitypricelistitem_set.all(), self.price_list.timepricelistitem_set.all(),
                  self.price_list.unitpricelistitem_set.all()))
        for price_list_item in price_list_items:
            if self.item_uuid == price_list_item.item_uuid:
                return
        raise ValidationError({'item_uuid': 'This uuid does not map to any price list item within this price list!'})


class PriceListItemService(models.Model):
    """
    Model through relation for mapping services to specific price list items
    """
    price_list = models.ForeignKey('PriceList', help_text="Which price list does this bundle item reference?")
    item_uuid = models.CharField(
        max_length=36, help_text="What is the item specific UUID?",
        validators=[RegexValidator(regex="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")]
    )
    service = models.ForeignKey(
        'assets.Service', related_name="service",
        help_text="Which service does this price list item map to?"
    )
    count = models.PositiveSmallIntegerField(
        help_text="How many counts of equipment should this price list item reference?",
        default=1, validators=[MinValueValidator(1)]
    )


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


'''
class PriceListBundle(models.Model):
    """
    Model for bundles within a price list. Will contain a set of price list items with an applied discount for all
    abstract items.
    """
    price_list = models.ForeignKey(
        'PriceList', help_text="Which price list does this bundle belong to?"
    )
    name = models.CharField(
        max_length=100, help_text="What is the name of this bundle?", default="Bundle"
    )
    description = models.TextField(
        help_text="What is the description of this bundle?", default="", blank=True
    )
    percent_discount = models.PositiveSmallIntegerField(
        help_text="What percent discount should be applied for this bundle? (Value between 0 and 100 percent)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    bundle_items = models.ManyToManyField(
        'PolymorphicBundleItem', through='BundleItemAttribute',
        help_text="Which bundle items belong in this price list bundle?"
    )

    def clean(self):
        if self.price_list.status != PRICE_LIST_PRE_RELEASE:
            raise ValidationError("Price list has been released. Cannot modify associated bundle.")

    def __str__(self):
        return "%(price_list)s, %(name)s" % {'price_list': self.price_list.name, 'name': self.name}

    def __unicode__(self):
        return u"%(price_list)s, %(name)s" % {'price_list': self.price_list.name, 'name': self.name}


class BundleItemAttribute(models.Model):
    """
    Model for the relation between the polymorphic bundle items and the related bundle.
    """
    bundle = models.ForeignKey(
        'PriceListBundle', help_text="Which bundle does this bundle item attribute relate to?"
    )
    bundle_item = models.ForeignKey(
        'PolymorphicBundleItem', help_text="Which bundle item does this bundle item attribute relate to?"
    )
    count = models.PositiveSmallIntegerField(
        help_text="How many counts of equipment should this price list item reference?",
        default=1, validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return "%(name)s: %(count)s x %(bundle_item)s" % {'name': self.name, 'count': self.count,
                                                          'bundle_item': self.bundle_item.polymorphic_item_uuid}

    def __unicode__(self):
        return u"%(name)s: %(count)s x %(bundle_item)s" % {'name': self.name, 'count': self.count,
                                                           'bundle_item': self.bundle_item.polymorphic_item_uuid}

    def clean(self):
        if self.bundle.price_list != self.bundle_item.price_list:
            raise ValidationError({'bundle_item': 'Bundle item must belong in the same price list as the bundle!'})


class PolymorphicBundleItem(models.Model):
    """
    Model for the base abstract bundle item.
    """
    price_list = models.ForeignKey('PriceList', help_text="Which price list does this bundle item reference?")
    content_type = models.ForeignKey(ContentType)
    polymorphic_item_uuid = models.CharField(
        max_length=36, help_text="What is the item specific UUID?",
        validators=[RegexValidator(regex="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")]
    )
    polymorphic_bundle_item = GenericForeignKey(
        'item_uuid', 'content_type'
    )
'''
