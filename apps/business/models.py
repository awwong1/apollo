from cities_light.models import City
from django.contrib.auth.models import User
from django.db import models


class Business(models.Model):
    """
    Business model, holds administrative business state, billing information.
    """
    name = models.CharField(
        max_length=60, unique=True, help_text="What is the name of this business?"
    )
    description = models.TextField(
        blank=True,
        help_text="What is the description for this business?"
    )
    address_1 = models.CharField(
        max_length=60, help_text="What is the address of this business?"
    )
    address_2 = models.CharField(
        max_length=60, blank=True, help_text="What is the address of this business?"
    )
    city = models.ForeignKey(
        City, blank=True, null=True, help_text="Which city does this business belong in?"
    )
    postal_code = models.CharField(
        max_length=6, help_text="What is the postal code of this business?"
    )

    class Meta:
        verbose_name_plural = "businesses"

    def __unicode__(self):
        return self.name


class BusinessMembership(models.Model):
    """
    Mapping between users and businesses. Defines business administrator permissions.
    """
    user = models.ForeignKey(
        User, help_text="Which user is part of this membership?"
    )
    business = models.ForeignKey(
        Business, help_text="Which business is part of this membership?"
    )
    user_accepted = models.BooleanField(
        default=False, help_text="Has the user accepted this membership?"
    )
    business_accepted = models.BooleanField(
        default=False, help_text="Has the business accepted this membership?"
    )
    business_administrator = models.BooleanField(
        default=False, help_text="Is this user an administrator of this business?"
    )

    class Meta:
        unique_together = ("user", "business")
        index_together = ("user", "business")

    def __unicode__(self):
        return self.user.username + u":" + self.business.nam