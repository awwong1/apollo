from apollo.choices import PRICE_LIST_PRE_RELEASE
from apps.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem
from django.forms import ModelForm


class PriceListForm(ModelForm):
    class Meta:
        model = PriceList
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PriceListForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance') is None:
            self.fields['status'].choices = ((PRICE_LIST_PRE_RELEASE, "Pre-Release"),)

    def save(self, commit=True):
        return super(PriceListForm, self).save(commit=commit)


class ActivityPriceListItemForm(ModelForm):
    class Meta:
        model = ActivityPriceListItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        price_list_id = kwargs.pop('price_list_id', None)
        super(ActivityPriceListItemForm, self).__init__(*args, **kwargs)
        if price_list_id is not None:
            self.fields['price_list'].queryset = PriceList.objects.filter(pk=price_list_id)
            self.fields['price_list'].empty_label = None
        else:
            pass


class TimePriceListItemForm(ModelForm):
    class Meta:
        model = TimePriceListItem
        fields = "__all__"


class UnitPriceListItemForm(ModelForm):
    class Meta:
        model = UnitPriceListItem
        fields = "__all__"
