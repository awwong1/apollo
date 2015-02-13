from apollo.choices import PRICE_LIST_PRE_RELEASE
from apps.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem, \
    PriceListItemEquipment, PriceListItemService
from django.forms import ModelForm


class PriceListForm(ModelForm):
    class Meta:
        model = PriceList
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PriceListForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance') is None:
            self.fields['status'].choices = ((PRICE_LIST_PRE_RELEASE, "Pre-Release"),)


class ActivityPriceListItemForm(ModelForm):
    class Meta:
        model = ActivityPriceListItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        price_list_id = kwargs.pop('pl_id', None)
        super(ActivityPriceListItemForm, self).__init__(*args, **kwargs)
        if price_list_id is not None:
            self.fields['price_list'].queryset = PriceList.objects.filter(pk=price_list_id)
        elif kwargs.get('instance') is not None:
            self.fields['price_list'].queryset = PriceList.objects.filter(pk=kwargs['instance'].price_list.pk)
        self.fields['price_list'].empty_label = None
        self.fields['price_list'].widget.attrs['readonly'] = 'readonly'


class TimePriceListItemForm(ModelForm):
    class Meta:
        model = TimePriceListItem
        fields = "__all__"


class UnitPriceListItemForm(ModelForm):
    class Meta:
        model = UnitPriceListItem
        fields = "__all__"


class PriceListItemEquipmentForm(ModelForm):
    class Meta:
        model = PriceListItemEquipment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        pl_id = kwargs.pop('pl_id', None)
        uuid = kwargs.pop('item_uuid', None)
        super(PriceListItemEquipmentForm, self).__init__(*args, **kwargs)
        if pl_id is not None:
            self.fields['price_list'].queryset = PriceList.objects.filter(pk=pl_id)
        if uuid is not None:
            self.fields['item_uuid'].initial = uuid
        if kwargs.get('instance') is not None:
            self.fields['price_list'].queryset = PriceList.objects.filter(pk=kwargs['instance'].price_list.pk)
            self.fields['item_uuid'].initial = kwargs['instance'].item_uuid
        self.fields['price_list'].empty_label = None
        self.fields['price_list'].widget.attrs['readonly'] = 'readonly'
        self.fields['item_uuid'].widget.attrs['readonly'] = 'readonly'


class PriceListItemServiceForm(ModelForm):
    class Meta:
        model = PriceListItemService
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        pl_id = kwargs.pop('pl_id', None)
        uuid = kwargs.pop('item_uuid', None)
        super(PriceListItemServiceForm, self).__init__(*args, **kwargs)
        if pl_id is not None:
            self.fields['price_list'].queryset = PriceList.objects.filter(pk=pl_id)
        if uuid is not None:
            self.fields['item_uuid'].initial = uuid
        if kwargs.get('instance') is not None:
            self.fields['price_list'].queryset = PriceList.objects.filter(pk=kwargs['instance'].price_list.pk)
            self.fields['item_uuid'].initial = kwargs['instance'].item_uuid
        self.fields['price_list'].empty_label = None
        self.fields['price_list'].widget.attrs['readonly'] = 'readonly'
        self.fields['item_uuid'].widget.attrs['readonly'] = 'readonly'