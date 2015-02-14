from apollo.choices import CHARGE_LIST_STATUS_CHOICES, CHARGE_LIST_OPEN, CHARGE_LIST_CLOSED_PAYMENT_RESOLVED, \
    PRICE_LIST_RELEASE
from django.core.exceptions import ValidationError
from django.db import models


class ChargeList(models.Model):
    price_list = models.ForeignKey(
        'price_list.PriceList', help_text="Which price list does this charge list reference?"
    )
    station = models.ForeignKey(
        'station.Station', help_text="Which station does this charge list reference?"
    )
    status = models.CharField(
        max_length=2, default=CHARGE_LIST_OPEN,
        choices=CHARGE_LIST_STATUS_CHOICES, help_text="What is the status of this charge list?"
    )

    class Meta:
        ordering = ['-pk']

    def clean(self):
        if self.price_list.status != PRICE_LIST_RELEASE:
            raise ValidationError({'price_list': 'Price list must be in released state before it can be used.'})
        station_charge_lists = self.station.chargelist_set.all()
        open_lists = station_charge_lists.filter(status=CHARGE_LIST_OPEN)
        if len(open_lists) > 0 and open_lists[0].pk != self.pk:
            raise ValidationError("Only one charge list may be open per station at any given time.")

    def __str__(self):
        return "({status}) {pricelist} {station}".format(status=self.get_status_display(), pricelist=self.price_list,
                                                         station=self.station)

    def __unicode__(self):
        return u"({status}) {pricelist} {station}".format(status=self.get_status_display(), pricelist=self.price_list,
                                                          station=self.station)


class AbstractChargeListItem(models.Model):
    charge_list = models.ForeignKey('ChargeList', help_text="Which charge list does this charge list item reference?")
    billing_business = models.ForeignKey('business.Business', help_text="Which business is this charge billed to?")
    last_modified = models.DateTimeField(auto_now=True, help_text="When was this charge list modified?")

    def clean(self):
        """
        Ensures that the billing business is part of the station's business members, status is not payment resolved
        Ensure that price list item matches charge list price list
        """
        valid_bu = len(self.charge_list.station.stationbusiness_set.all().filter(business=self.billing_business)) == 1
        if not valid_bu:
            raise ValidationError(
                {'billing_business': 'This business is not in a station business relationship with this station.'}
            )
        if self.charge_list.status == CHARGE_LIST_CLOSED_PAYMENT_RESOLVED:
            raise ValidationError('This charge list has already been closed and payment has been resolved.')
        if self.price_list_item.price_list != self.charge_list.price_list:
            raise ValidationError(
                {'price_list_item', 'This price list item is invalid for the charge list specified price list.'}
            )

    class Meta:
        ordering = ['-pk']
        abstract = True


class ActivityCharge(AbstractChargeListItem):
    price_list_item = models.ForeignKey(
        'price_list.ActivityPriceListItem',
        help_text="Which actvitiy price list item does this charge list item reference"
    )
    price_per_unit_override = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True,
        help_text="How much does this price list item cost per unit measurement? (Overrides original price)"
    )

    def __str__(self):
        price = self.price_per_unit_override
        if not price:
            price = self.price_list_item.price_per_unit
        return "{name} (${price}/{measurement})".format(
            name=self.price_list_item, price=price,
            measurement=self.price_list_item.unit_measurement
        )

    def __unicode__(self):
        price = self.price_per_unit_override
        if not price:
            price = self.price_list_item.price_per_unit
        return u"{name} (${price}/{measurement})".format(
            name=self.price_list_item, price=price,
            measurement=self.price_list_item.unit_measurement
        )


class ActivityChargeActivityCount(models.Model):
    activity_charge = models.ForeignKey(
        ActivityCharge, help_text="Which activity charge is this activity charge activity count applied to?"
    )
    activity_count = models.PositiveIntegerField(
        help_text="How many units of activity is being applied to this activity charge?"
    )
    last_modified = models.DateTimeField(auto_now=True, help_text="When was this activity last created/modified?")

    def __str__(self):
        return "{count} {unit}".format(count=self.activity_count,
                                       unit=self.activity_charge.price_list_item.get_unit_measurement_display())

    def __unicode__(self):
        return u"{count} {unit}".format(count=self.activity_count,
                                        unit=self.activity_charge.price_list_item.get_unit_measurement_display())


class TimeCharge(AbstractChargeListItem):
    price_list_item = models.ForeignKey(
        'price_list.TimePriceListItem',
        help_text="Which time price list item does this charge list item reference"
    )
    price_per_time_override = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True,
        help_text="How much does this price list item cost per unit of time?"
    )
    time_start = models.DateTimeField(blank=True, help_text="When does this time charge begin billing?")
    time_end = models.DateTimeField(blank=True, help_text="When does this time charge end billing?")

    def clean(self):
        if self.time_start:
            if self.time_end and self.time_end < self.time_start:
                raise ValidationError({'time_end': 'Charge billing time cannot end before it began.'})
        elif self.time_end:
            raise ValidationError({'time_start': 'Charges with an end time must have a start time specified.'})

    def __str__(self):
        price = self.price_per_time_override
        if not price:
            price = self.price_list_item.price_per_unit
        return "{name} (${price}/{measurement})".format(
            name=self.price_list_item, price=price,
            measurement=self.price_list_item.get_unit_time_display()
        )

    def __unicode__(self):
        price = self.price_per_time_override
        if not price:
            price = self.price_list_item.price_per_unit
        return u"{name} (${price}/{measurement})".format(
            name=self.price_list_item, price=price,
            measurement=self.price_list_item.get_unit_time_display()
        )


class UnitCharge(AbstractChargeListItem):
    price_list_item = models.ForeignKey(
        'price_list.UnitPriceListItem',
        help_text="Which unit price list item does this charge list item reference"
    )
    price_per_unit_override = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True,
        help_text="How much does this price list item cost?"
    )

    def __str__(self):
        price = self.price_per_time_override
        if not price:
            price = self.price_list_item.price_per_unit
        return "{name} (${price})".format(
            name=self.price_list_item, price=price,
        )

    def __unicode__(self):
        price = self.price_per_time_override
        if not price:
            price = self.price_list_item.price_per_unit
        return u"{name} (${price})".format(
            name=self.price_list_item, price=price,
        )
