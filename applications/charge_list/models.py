from decimal import Decimal
from apollo.choices import CHARGE_LIST_STATUS_CHOICES, CHARGE_LIST_OPEN, CHARGE_LIST_CLOSED_PAYMENT_RESOLVED, \
    PRICE_LIST_RELEASE, TIME_MEASUREMENT_DAY, TIME_MEASUREMENT_HOUR
from applications.price_list.models import PriceListItemService
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


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

    def get_active_services(self):
        """
        Get a dictionary of billing businesses and their active activation regex ids.
        """
        business_services = dict()
        for act_charge in self.activitycharge_set.all().filter(services_active=True):
            services = []
            act_pli = act_charge.price_list_item
            act_services = PriceListItemService.objects.filter(item_uuid=act_pli.item_uuid,
                                                               price_list=act_pli.price_list)
            for act_service in act_services:
                for iteration in range(0, act_service.count):
                    services.append(act_service.service.activation_id)
            if act_charge.billing_business in business_services.keys():
                existing_services = business_services[act_charge.billing_business]
                existing_services.extend(services)
                business_services[act_charge.billing_business] = existing_services
            else:
                business_services[act_charge.billing_business] = services
        for time_charge in self.timecharge_set.all().filter(services_active=True):
            services = []
            time_pli = time_charge.price_list_item
            time_services = PriceListItemService.objects.filter(item_uuid=time_pli.item_uuid,
                                                                price_list=time_pli.price_list)
            for time_service in time_services:
                for iteration in range(0, time_service.count):
                    services.append(time_service.service.activation_id)
            if time_charge.billing_business in business_services.keys():
                existing_services = business_services[time_charge.billing_business]
                existing_services.extend(services)
                business_services[time_charge.billing_business] = existing_services
            else:
                business_services[time_charge.billing_business] = services
        for unit_charge in self.unitcharge_set.all().filter(services_active=True):
            services = []
            unit_pli = unit_charge.price_list_item
            unit_services = PriceListItemService.objects.filter(item_uuid=unit_pli.item_uuid,
                                                                price_list=unit_pli.price_list)
            for unit_service in unit_services:
                for iteration in range(0, unit_service.count):
                    services.append(unit_service.service.activation_id)
            if unit_charge.billing_business in business_services.keys():
                existing_services = business_services[unit_charge.billing_business]
                existing_services.extend(services)
                business_services[unit_charge.billing_business] = existing_services
            else:
                business_services[unit_charge.billing_business] = services
        return business_services


class AbstractChargeListItem(models.Model):
    charge_list = models.ForeignKey('ChargeList', help_text="Which charge list does this charge list item reference?")
    billing_business = models.ForeignKey('business.Business', help_text="Which business is this charge billed to?")
    last_modified = models.DateTimeField(auto_now=True, help_text="When was this charge list modified?")
    services_active = models.BooleanField(default=True, help_text="Are these charge's associated services enabled?")

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
                {'price_list_item': 'This price list item is invalid for the charge list specified price list.'}
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
        max_digits=7, decimal_places=2, blank=True, null=True,
        help_text="How much does this price list item cost per unit measurement? (Overrides original price)"
    )

    def __str__(self):
        price = self.price_per_unit_override
        if price is None:
            price = self.price_list_item.price_per_unit
        return "{name} (${price}/{measurement})".format(
            name=self.price_list_item.name, price=price,
            measurement=self.price_list_item.unit_measurement
        )

    def __unicode__(self):
        price = self.price_per_unit_override
        if price is None:
            price = self.price_list_item.price_per_unit
        return u"{name} (${price}/{measurement})".format(
            name=self.price_list_item.name, price=price,
            measurement=self.price_list_item.unit_measurement
        )

    def get_cost(self):
        """
        Return the raw decimal value for what this charge costs
        :return:
        """
        base_price = self.price_list_item.price_per_unit
        if self.price_per_unit_override:
            base_price = self.price_per_unit_override
        charge_activities = self.activitychargeactivitycount_set.all()
        price = Decimal(0.0)
        for ca in charge_activities:
            price += Decimal(ca.activity_count * base_price)
        return price


class ActivityChargeActivityCount(models.Model):
    activity_charge = models.ForeignKey(
        ActivityCharge, help_text="Which activity charge is this activity charge activity count applied to?"
    )
    activity_count = models.PositiveIntegerField(
        help_text="How many units of activity is being applied to this activity charge?",
        validators=[MinValueValidator(1)]
    )
    last_modified = models.DateTimeField(auto_now=True, help_text="When was this activity last created/modified?")

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return "{count} {unit}".format(count=self.activity_count,
                                       unit=self.activity_charge.price_list_item.unit_measurement)

    def __unicode__(self):
        return u"{count} {unit}".format(count=self.activity_count,
                                        unit=self.activity_charge.price_list_item.unit_measurement)


class TimeCharge(AbstractChargeListItem):
    price_list_item = models.ForeignKey(
        'price_list.TimePriceListItem',
        help_text="Which time price list item does this charge list item reference"
    )
    price_per_time_override = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True,
        help_text="How much does this price list item cost per unit of time?"
    )
    time_start = models.DateTimeField(blank=True, null=True, help_text="When does this time charge begin billing?")
    time_end = models.DateTimeField(blank=True, null=True, help_text="When does this time charge end billing?")

    def clean(self):
        if self.time_start:
            if self.time_end and self.time_end < self.time_start:
                raise ValidationError({'time_end': 'Charge billing time cannot end before it began.'})
            if timezone.now() < self.time_start:
                raise ValidationError({'time_start': 'Charge cannot begin billing in the future.'})
        elif self.time_end:
            raise ValidationError({'time_start': 'Charges with an end time must have a start time specified.'})

    def __str__(self):
        price = self.price_per_time_override
        if price is None:
            price = self.price_list_item.price_per_time
        return "{name} (${price}/{measurement})".format(
            name=self.price_list_item.name, price=price,
            measurement=self.price_list_item.get_unit_time_display()
        )

    def __unicode__(self):
        price = self.price_per_time_override
        if price is None:
            price = self.price_list_item.price_per_time
        return u"{name} (${price}/{measurement})".format(
            name=self.price_list_item.name, price=price,
            measurement=self.price_list_item.get_unit_time_display()
        )

    def get_cost(self):
        """
        Return the raw decimal value for what this charge costs
        :return:
        """
        base_price = self.price_list_item.price_per_time
        if self.price_per_time_override:
            base_price = self.price_per_unit_override
        price = Decimal(0.0)
        if self.time_start is not None:
            end = self.time_end
            if end is None:
                end = timezone.now()
            diff_time = end - self.time_start
            if self.price_list_item.unit_time == TIME_MEASUREMENT_DAY:
                price = base_price * Decimal(diff_time.days)
            elif self.price_list_item.unit_time == TIME_MEASUREMENT_HOUR:
                price += Decimal(diff_time.days) * 24 * base_price
                price += Decimal(diff_time.seconds/3600) * base_price
        return price


class UnitCharge(AbstractChargeListItem):
    price_list_item = models.ForeignKey(
        'price_list.UnitPriceListItem',
        help_text="Which unit price list item does this charge list item reference"
    )
    price_per_unit_override = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True,
        help_text="How much does this price list item cost?"
    )

    def __str__(self):
        price = self.price_per_time_override
        if price is None:
            price = self.price_list_item.price_per_unit
        return "{name} (${price})".format(
            name=self.price_list_item.name, price=price,
        )

    def __unicode__(self):
        price = self.price_per_time_override
        if price is None:
            price = self.price_list_item.price_per_unit
        return u"{name} (${price})".format(
            name=self.price_list_item.name, price=price,
        )
