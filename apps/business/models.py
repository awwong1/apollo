from cities_light.models import City
from django.contrib.auth.models import User, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm, remove_perm


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
        permissions = (("add_businessmembership", "Can add a business membership for this business"),)
        default_permissions = ('add', 'change', 'delete')

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
    business_administrator = models.BooleanField(
        default=False, help_text="Is this user an administrator of this business?"
    )

    class Meta:
        unique_together = ("user", "business")
        default_permissions = ('change', 'delete')

    def delete(self, *args, **kwargs):
        # Do not allow deletion if the current membership is the business last administrator.
        if self.business_administrator:
            business_admins = self.business.businessmembership_set.all().filter(business_administrator=True)
            if len(business_admins) == 1:
                raise LastAdministratorException('Cannot delete the last administrator in a business')
        return super(BusinessMembership, self).delete(*args, **kwargs)

    def clean(self):
        # Do not allow modification of membership such that there are no administrators
        business_admins = self.business.businessmembership_set.all().filter(business_administrator=True)
        if len(business_admins) == 1:
            if business_admins[0].pk == self.pk and self.business_administrator is False:
                raise LastAdministratorException('Cannot remove administrator status from last business administrator')
        # Do not allow modification of user and business after creation, revert fields back to original state
        if self.pk is not None:
            existing = BusinessMembership.objects.get(pk=self.pk)
            self.user = existing.user
            self.business = existing.business

    def __str__(self):
        return "{business}{admin}: {uname}".format(uname=self.user.username, business=self.business.name,
                                                   admin=' (admin)' if self.business_administrator else ' ')

    def __unicode__(self):
        return u"{business}{admin}: {uname}".format(uname=self.user.username, business=self.business.name,
                                                    admin=u' (admin)' if self.business_administrator else u' ')


class LastAdministratorException(Exception):
    # Exception for deleting the last administrator in a business
    pass


@receiver(post_save, sender=BusinessMembership)
def business_membership_post_save_callback(sender, instance, **kwargs):
    # Administrators can change this business and add/change business memberships for this business, non-admins cannot
    if instance.business_administrator:
        assign_perm('business.change_business', instance.user, instance.business)
        assign_perm('business.add_businessmembership', instance.user, instance.business)
        for business_membership in instance.business.businessmembership_set.all():
            assign_perm('business.change_businessmembership', instance.user, business_membership)
            assign_perm('business.delete_businessmembership', instance.user, business_membership)
    else:
        remove_perm('business.change_business', instance.user, instance.business)
        remove_perm('business.add_businessmembership', instance.user, instance.business)
        for business_membership in instance.business.businessmembership_set.all():
            remove_perm('business.change_businessmembership', instance.user, business_membership)
            remove_perm('business.delete_businessmembership', instance.user, business_membership)


@receiver(post_save, sender=User)
def user_post_save_callback_business(sender, instance, created, **kwargs):
    # All users can add businesses. On user creation, explicitly define permission to add a business.
    if created:
        add_business = Permission.objects.get(codename='add_business')
        instance.user_permissions.add(add_business)