from uuid import uuid4
from apollo.choices import STATION_TYPE_CHOICES, STATION_RIG
from django.core.validators import RegexValidator
from django.db import models


class Station(models.Model):
    """
    Object model for determining where physical equipment would be delivered to and which business manages the station.
    Also known as a rig in most cases, however the terminology is now more general (in the future, in case we start
    renting out equipment to other places, like a drilling pit)
    """
    type = models.CharField(
        max_length=60, help_text="What type of station is this?", choices=STATION_TYPE_CHOICES, default=STATION_RIG
    )
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
        return "{type}: {name}".format(type=self.get_type_display(), name=self.name)

    def __unicode__(self):
        return u"{type}: {name}".format(type=self.get_type_display(), name=self.name)


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

    class Meta:
        unique_together = ('station', 'business')
        index_together = ('station', 'business')

    def __str__(self):
        return "{uname}: {business}".format(uname=self.station, business=self.business.name)

    def __unicode__(self):
        return u"{uname}: {business}".format(uname=self.station, business=self.business.name)
