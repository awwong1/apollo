from uuid import uuid4
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class Station(models.Model):
    """
    Object model for determining where physical equipment would be delivered to and which business manages the station.
    Also known as a rig in most cases, however the terminology is now more general (in the future, in case we start
    renting out equipment to other places, like a drilling pit)
    """
    name = models.CharField(
        max_length=255, help_text="What is the name of this station?"
    )
    description = models.TextField(
        blank=True, help_text="What is the description for this station? How does a user get to this station?"
    )
    uuid = models.CharField(
        max_length=36, default=uuid4, unique=True,
        help_text="What is the universally unique identifier for this station?",
        validators=[RegexValidator(regex="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")]
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.name


class StationBusiness(models.Model):
    """
    Object model for linking Stations and Businesses. Determines permissions and purchases for stations.
    Station administrators can invite other businesses into the station.
    """
    business = models.ForeignKey(
        'business.Business', help_text="Which business comprises this station to business membership?"
    )
    station = models.ForeignKey(
        'Station', help_text="Which station comprises this station to business membership?"
    )
    station_administrator = models.BooleanField(
        default=False, help_text="Is this station an administrator of this business?"
    )

    class Meta:
        unique_together = ('station', 'business')
        index_together = ('station', 'business')

    def clean(self):
        # Do not allow modification of membership such that there are no administrators
        station_admins = self.business.stationbusiness_set.all().filter(station_administrator=True)
        if len(station_admins) == 1:
            if station_admins[0].pk == self.pk and self.station_administrator is False:
                raise ValidationError('Cannot remove administrator status from last station administrator')
        # Do not allow modification of user and business after creation, revert fields back to original state
        if self.pk is not None:
            existing = StationBusiness.objects.get(pk=self.pk)
            self.station = existing.station
            self.business = existing.business

    def __str__(self):
        return "{business}{admin}: {uname}".format(uname=self.station.name, business=self.business.name,
                                                   admin=' (Admin)' if self.station_administrator else ' ')

    def __unicode__(self):
        return u"{business}{admin}: {uname}".format(uname=self.station.name, business=self.business.name,
                                                    admin=u' (Admin)' if self.station_administrator else u' ')
