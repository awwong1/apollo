from cities_light.models import City
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
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

    def clean(self):
        # Do not allow modification of membership such that there are no administrators
        business_admins = self.business.businessmembership_set.all().filter(business_administrator=True)
        if len(business_admins) == 1:
            if business_admins[0].pk == self.pk and self.business_administrator is False:
                raise ValidationError('Cannot remove administrator status from last business administrator')
        # Do not allow modification of user and business after creation, revert fields back to original state
        if self.pk is not None:
            existing = BusinessMembership.objects.get(pk=self.pk)
            self.user = existing.user
            self.business = existing.business

    def __str__(self):
        return "{business}{admin}: {uname}".format(uname=self.user.username, business=self.business.name,
                                                   admin=' (Admin)' if self.business_administrator else '')

    def __unicode__(self):
        return u"{business}{admin}: {uname}".format(uname=self.user.username, business=self.business.name,
                                                    admin=u' (Admin)' if self.business_administrator else u'')