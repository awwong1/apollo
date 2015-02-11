from apps.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem, \
    PriceListBundle, ActivityBundleItem, TimeBundleItem, UnitBundleItem
from django.forms import ModelForm


class ActivityPriceListItemForm(ModelForm):
    class Meta:
        model = ActivityPriceListItem
        fields = "__all__"


class TimePriceListItemForm(ModelForm):
    class Meta:
        model = TimePriceListItem
        fields = "__all__"


class UnitPriceListItemForm(ModelForm):
    class Meta:
        model = UnitPriceListItem
        fields = "__all__"


class PriceListBundleForm(ModelForm):
    class Meta:
        model = PriceListBundle
        fields = "__all__"


class ActivityBundleItemForm(ModelForm):
    class Meta:
        model = ActivityBundleItem
        fields = "__all__"


class TimeBundleItemForm(ModelForm):
    class Meta:
        model = TimeBundleItem
        fields = "__all__"


class UnitBundleItemForm(ModelForm):
    class Meta:
        model = UnitBundleItem
        fields = "__all__"