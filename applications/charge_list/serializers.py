from applications.charge_list.models import ChargeList, ActivityCharge, TimeCharge, UnitCharge, \
    ActivityChargeActivityCount
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class ChargeListSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="charge-list-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    station = relations.HyperlinkedRelatedField(view_name="station-detail", read_only=True)

    class Meta:
        model = ChargeList


class ActivityChargeSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="activity-charge-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    charge_list = relations.HyperlinkedRelatedField(view_name="charge-list-detail", read_only=True)
    billing_business = relations.HyperlinkedRelatedField(view_name="business-detail", read_only=True)

    class Meta:
        model = ActivityCharge


class TimeChargeSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="time-charge-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    charge_list = relations.HyperlinkedRelatedField(view_name="charge-list-detail", read_only=True)
    billing_business = relations.HyperlinkedRelatedField(view_name="business-detail", read_only=True)

    class Meta:
        model = TimeCharge


class ActivityChargeActivityCountSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="activity-charge-activity-count-detail")
    activity_charge = relations.HyperlinkedRelatedField(view_name="activity-charge-detail", read_only=True)

    class Meta:
        model = ActivityChargeActivityCount


class UnitChargeSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="unit-charge-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    charge_list = relations.HyperlinkedRelatedField(view_name="charge-list-detail", read_only=True)
    billing_business = relations.HyperlinkedRelatedField(view_name="business-detail", read_only=True)

    class Meta:
        model = UnitCharge
