from uuid import uuid4
from itertools import chain
from apollo.choices import PRICE_LIST_STATUS_TYPES, PRICE_LIST_PRE_RELEASE, TIME_MEASUREMENT_CHOICES
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    def get_item_from_uuid(self, item_uuid):
        items = self.activitypricelistitem_set.all().filter(item_uuid=item_uuid)
        if len(items) > 0:
            return items[0]
        items = self.timepricelistitem_set.all().filter(item_uuid=item_uuid)
        if len(items) > 0:
            return items[0]
        items = self.unitpricelistitem_set.all().filter(item_uuid=item_uuid)
        if len(items) > 0:
            return items[0]
        return None

    def __str__(self):
        return "({status}) {0}: {1}".format(self.pk, self.name, status=self.get_status_display())

    def __unicode__(self):
        return u"({status}) {0}: {1}".format(self.pk, self.name, status=self.get_status_display())


@receiver(post_save, sender=PriceList)
def price_list_post_save_callback(sender, instance, created, **kwargs):
    """
    When creating a new price list, populate all fields with the previous price list's data
    """
    if created:
        price_lists = sender.objects.all()
        if len(price_lists) < 2:
            return
        last_price_list = price_lists[1]
        for activity_item in last_price_list.activitypricelistitem_set.all():
            activity_item.pk = None
            activity_item.price_list = instance
            activity_item.save()
        for time_item in last_price_list.timepricelistitem_set.all():
            time_item.pk = None
            time_item.price_list = instance
            time_item.save()
        for unit_item in last_price_list.unitpricelistitem_set.all():
            unit_item.pk = None
            unit_item.price_list = instance
            unit_item.save()
        for equipmentplir in last_price_list.pricelistitemequipment_set.all():
            equipmentplir.pk = None
            equipmentplir.price_list = instance
            equipmentplir.save()
        for serviceplir in last_price_list.pricelistitemservice_set.all():
            serviceplir.pk = None
            serviceplir.price_list = instance
            serviceplir.save()


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
        help_text="What is the description of this price list item?"
    )
    terms_of_service = models.ForeignKey(
        'terms_of_service.TermsOfService',
        help_text="Which terms of service must a user agree to before using purchasing this price list item?"
    )

    class Meta:
        abstract = True
        index_together = ('price_list', 'item_uuid')
        # Django bug, this is not enforced!!
        # https://code.djangoproject.com/ticket/16732
        unique_together = ('price_list', 'item_uuid')

    def clean(self):
        if self.price_list.status != PRICE_LIST_PRE_RELEASE:
            raise ValidationError(
                {'price_list': "Price list has been released. Cannot modify associated price list items."})
        if self.pk is None:
            # Workaround for the unique together bug, disabled item_uuid in update in models and form field
            activity_items = ActivityPriceListItem.objects.filter(price_list=self.price_list)
            time_items = TimePriceListItem.objects.filter(price_list=self.price_list)
            unit_items = UnitPriceListItem.objects.filter(price_list=self.price_list)
            for item in chain(activity_items, time_items, unit_items):
                if item.item_uuid == self.item_uuid:
                    raise ValidationError({'item_uuid': "Price list item with this item uuid already exists!"})

    def delete(self, using=None):
        PriceListItemEquipment.objects.filter(price_list=self.price_list, item_uuid=self.item_uuid).delete()
        PriceListItemService.objects.filter(price_list=self.price_list, item_uuid=self.item_uuid).delete()
        super(AbstractPriceListItem, self).delete(using=using)

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

    def clean_fields(self, exclude=None):
        if self.pk is not None:
            self.item_uuid = ActivityPriceListItem.objects.get(pk=self.pk).item_uuid
        return super(ActivityPriceListItem, self).clean_fields(exclude=exclude)

    def __str__(self):
        return "{name} (${price}/{measurement})".format(name=self.name, price=self.price_per_unit,
                                                        measurement=self.unit_measurement)

    def __unicode__(self):
        return u"{name} (${price}/{measurement})".format(name=self.name, price=self.price_per_unit,
                                                         measurement=self.unit_measurement)


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

    def clean_fields(self, exclude=None):
        if self.pk is not None:
            self.item_uuid = TimePriceListItem.objects.get(pk=self.pk).item_uuid
        return super(TimePriceListItem, self).clean_fields(exclude=exclude)

    def __str__(self):
        return "{name} (${price}/{measurement})".format(name=self.name, price=self.price_per_time,
                                                        measurement=self.get_unit_time_display())

    def __unicode__(self):
        return u"{name} (${price}/{measurement})".format(name=self.name, price=self.price_per_time,
                                                         measurement=self.get_unit_time_display())


class UnitPriceListItem(AbstractPriceListItem):
    """
    Model for unit based price list items. Pricing is price per unit.
    Suitable for flat rate charges, such as a charge to deliver a piece of equipment/part
    """
    price_per_unit = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text="How much does this price list item cost?"
    )

    def clean_fields(self, exclude=None):
        if self.pk is not None:
            self.item_uuid = UnitPriceListItem.objects.get(pk=self.pk).item_uuid
        return super(UnitPriceListItem, self).clean_fields(exclude=exclude)

    def __str__(self):
        return "{name} (${price})".format(name=self.name, price=self.price_per_unit)

    def __unicode__(self):
        return u"{name} (${price})".format(name=self.name, price=self.price_per_unit)


class PriceListItemEquipment(models.Model):
    """
    Model through relation for mapping equipment to specific price list items
    """
    price_list = models.ForeignKey('PriceList', help_text="Which price list does this equipment item reference?")
    item_uuid = models.CharField(
        max_length=36, help_text="What is the price list item specific UUID?",
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

    class Meta:
        unique_together = ('price_list', 'item_uuid', 'equipment')

    def clean(self):
        price_list_items = list(
            chain(self.price_list.activitypricelistitem_set.all(), self.price_list.timepricelistitem_set.all(),
                  self.price_list.unitpricelistitem_set.all()))
        for price_list_item in price_list_items:
            if self.item_uuid == price_list_item.item_uuid:
                return
        raise ValidationError({'item_uuid': 'This uuid does not map to any price list item within this price list!'})

    def __str__(self):
        return "{equipment} x {count}".format(equipment=self.equipment, count=self.count)

    def __unicode__(self):
        return u"{equipment} x {count}".format(equipment=self.equipment, count=self.count)


class PriceListItemService(models.Model):
    """
    Model through relation for mapping services to specific price list items
    """
    price_list = models.ForeignKey('PriceList', help_text="Which price list does this service item reference?")
    item_uuid = models.CharField(
        max_length=36, help_text="What is the price list item specific UUID?",
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

    class Meta:
        unique_together = ('price_list', 'item_uuid', 'service')

    def clean(self):
        price_list_items = list(
            chain(self.price_list.activitypricelistitem_set.all(), self.price_list.timepricelistitem_set.all(),
                  self.price_list.unitpricelistitem_set.all()))
        for price_list_item in price_list_items:
            if self.item_uuid == price_list_item.item_uuid:
                return
        raise ValidationError({'item_uuid': 'This uuid does not map to any price list item within this price list!'})

    def __str__(self):
        return "{service} x {count}".format(service=self.service, count=self.count)

    def __unicode__(self):
        return u"{service} x {count}".format(service=self.service, count=self.count)


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
