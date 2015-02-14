from django.contrib.auth.models import User
from django.db import models


class Business(models.Model):
    """
    Business model, holds billing information.
    """
    name = models.CharField(
        max_length=60, unique=True, help_text="What is the name of this business?"
    )
    description = models.TextField(
        blank=True, help_text="What is the description for this business?"
    )
    address_1 = models.CharField(
        max_length=60, help_text="What is the address of this business?"
    )
    address_2 = models.CharField(
        max_length=60, blank=True, help_text="What is the address of this business? (Continued)"
    )
    country = models.CharField(
        max_length=60, help_text="Which country is this business located in?"
    )
    region = models.CharField(
        max_length=60, blank=True, help_text="Which province, territory, or region is this business located in?"
    )
    city = models.CharField(
        max_length=60, help_text="Which city is this business located in?"
    )
    postal_code = models.CharField(
        max_length=6, help_text="What is the postal/zip code of this business?"
    )

    class Meta:
        verbose_name_plural = "businesses"

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return u"%s" % self.name


class BusinessMembership(models.Model):
    """
    Mapping between users and businesses.
    """
    user = models.ForeignKey(
        User, help_text="Which user is part of this membership? Cannot be edited once membership is created."
    )
    business = models.ForeignKey(
        Business, help_text="Which business is part of this membership? Cannot be edited once membership is created."
    )

    class Meta:
        unique_together = ("user", "business")

    def __str__(self):
        return "{business}: {uname}".format(uname=self.user.username, business=self.business.name)

    def __unicode__(self):
        return u"{business}: {uname}".format(uname=self.user.username, business=self.business.name)