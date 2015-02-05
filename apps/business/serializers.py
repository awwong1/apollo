from apps.business.models import Business, BusinessMembership
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework import relations


class BusinessSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="apollo-api-business-detail")
    city = relations.HyperlinkedIdentityField(view_name="cities-light-api-city-detail")

    class Meta:
        model = Business
        read_only_fields = ('id', 'admin_business',)


class BusinessMembershipSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="apollo-api-business-membership-detail")
    business = relations.HyperlinkedIdentityField(view_name="apollo-api-business-detail")

    class Meta:
        model = BusinessMembership
        read_only_fields = ('id', )