"""
Rest framework classes for Business application
"""
from apps.business.models import Business, BusinessMembership
from cities_light.models import City
from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework import relations


# Serializers
class BusinessSerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for a Business.

    Cities are too numerous with default django cities straight call, queryset must be reduced further in API.
    Example: "/api/business/?q_city=calgary"
    """
    url = relations.HyperlinkedIdentityField(view_name="business-detail")
    # Set for API Query performance, limit the cities in the queryset options
    city = relations.HyperlinkedRelatedField(
        view_name="cities-light-api-city-detail", queryset=City.objects.all(),
        help_text="Which city does this business belong in?"
    )

    class Meta:
        model = Business
        read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        q_city = kwargs['context']['request'].GET.get('city', None)
        super(BusinessSerializer, self).__init__(*args, **kwargs)
        if q_city:
            self.fields['city'].queryset = City.objects.filter(search_names__icontains=q_city)
        else:
            self.fields['city'].queryset = City.objects.none()


class BusinessMembershipSerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for a Business Relationship (Creation)
    """
    url = relations.HyperlinkedIdentityField(view_name="business-membership-detail")
    business = relations.HyperlinkedRelatedField(view_name="business-detail", queryset=Business.objects.all())
    user = relations.HyperlinkedRelatedField(view_name="user-detail", queryset=User.objects.all())

    class Meta:
        model = BusinessMembership
        read_only_fields = ('id', )


class EditBusinessMembershipSerializer(HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer for a Business Relationship (Modification).
    Can only toggle business administrator status.
    """
    url = relations.HyperlinkedIdentityField(view_name="business-membership-detail")
    business = relations.HyperlinkedRelatedField(view_name="business-detail", read_only=True)
    user = relations.HyperlinkedRelatedField(view_name="user-detail", read_only=True)

    class Meta:
        model = BusinessMembership
        read_only_fields = ('id', 'user', 'business')