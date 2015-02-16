from applications.business.models import Business, BusinessMembership
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class BusinessSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="business-detail")

    class Meta:
        model = Business


class BusinessMembershipSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="business-membership-detail")
    business = relations.HyperlinkedRelatedField(view_name="business-detail", read_only=True)

    class Meta:
        model = BusinessMembership
