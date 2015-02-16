from applications.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem, \
    PriceListItemEquipment, PriceListItemService
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class PriceListSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="price-list-detail")

    class Meta:
        model = PriceList


class ActivityPriceListItemSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="activity-price-list-item-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    terms_of_service = relations.HyperlinkedRelatedField(view_name="terms-of-service-detail", read_only=True)

    class Meta:
        model = ActivityPriceListItem


class TimePriceListItemSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="time-price-list-item-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    terms_of_service = relations.HyperlinkedRelatedField(view_name="terms-of-service-detail", read_only=True)

    class Meta:
        model = TimePriceListItem


class UnitPriceListItemSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="unit-price-list-item-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    terms_of_service = relations.HyperlinkedRelatedField(view_name="terms-of-service-detail", read_only=True)

    class Meta:
        model = UnitPriceListItem


class PriceListItemEquipmentSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="price-list-item-equipment-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    equipment = relations.HyperlinkedRelatedField(view_name="equipment-detail", read_only=True)

    class Meta:
        model = PriceListItemEquipment


class PriceListItemServiceSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="price-list-item-equipment-detail")
    price_list = relations.HyperlinkedRelatedField(view_name="price-list-detail", read_only=True)
    service = relations.HyperlinkedRelatedField(view_name="service-detail", read_only=True)

    class Meta:
        model = PriceListItemService
