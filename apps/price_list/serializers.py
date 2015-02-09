from apps.price_list.models import PriceList, TimePriceListItem, ActivityPriceListItem, UnitPriceListItem, \
    PriceListBundle
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class PriceListSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="price-list-detail")

    class Meta:
        model = PriceList
        read_only_fields = ('id',)


class ActivityPriceListItemSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="activity-price-list-item-detail")
    price_list = relations.HyperlinkedRelatedField(
        view_name="price-list-detail", queryset=PriceList.objects.all(),
        help_text="Which price list does this price list item belong in?", required=True,
    )

    class Meta:
        model = ActivityPriceListItem
        read_only_fields = ('id',)


class TimePriceListItemSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="time-price-list-item-detail")
    price_list = relations.HyperlinkedRelatedField(
        view_name="price-list-detail", queryset=PriceList.objects.all(),
        help_text="Which price list does this price list item belong in?", required=True,
    )

    class Meta:
        model = TimePriceListItem
        read_only_fields = ('id',)


class UnitPriceListItemSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="unit-price-list-item-detail")
    price_list = relations.HyperlinkedRelatedField(
        view_name="price-list-detail", queryset=PriceList.objects.all(),
        help_text="Which price list does this price list item belong in?", required=True,
    )

    class Meta:
        model = UnitPriceListItem
        read_only_fields = ('id',)


class PriceListBundleSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="price-list-bundle-detail")
    price_list = relations.HyperlinkedRelatedField(
        view_name="price-list-detail", queryset=PriceList.objects.all(),
        help_text="Which price list does this price list item belong in?", required=True,
    )
    activity_bundle_items = relations.HyperlinkedRelatedField(
        view_name="activity-price-list-item-detail", queryset=ActivityPriceListItem.objects.all(),
        help_text="Which activity items are included in this bundle?", many=True, allow_null=True
    )
    time_bundle_items = relations.HyperlinkedRelatedField(
        view_name="time-price-list-item-detail", queryset=TimePriceListItem.objects.all(),
        help_text="Which time items are included in this bundle?", many=True, allow_null=True
    )
    unit_bundle_items = relations.HyperlinkedRelatedField(
        view_name="unit-price-list-item-detail", queryset=UnitPriceListItem.objects.all(),
        help_text="Which unit items are included in this bundle?", many=True, allow_null=True
    )

    class Meta:
        model = PriceListBundle
        read_only_fields = ('id',)