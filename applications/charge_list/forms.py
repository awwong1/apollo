from apollo.choices import PRICE_LIST_RELEASE
from applications.business.models import Business
from applications.charge_list.models import ChargeList, ActivityCharge, TimeCharge, ActivityChargeActivityCount, \
    UnitCharge
from applications.price_list.models import PriceList, TimePriceListItem, ActivityPriceListItem, UnitPriceListItem
from applications.station.models import Station
from django import forms


class ChargeListForm(forms.ModelForm):
    class Meta:
        model = ChargeList
        fields = ("station", "price_list")

    def __init__(self, *args, **kwargs):
        station_pk = kwargs.pop('station_pk', None)
        super(ChargeListForm, self).__init__(*args, **kwargs)
        if station_pk is not None:
            self.fields['station'].queryset = Station.objects.filter(pk=station_pk)
        if kwargs.get('instance', None) is not None:
            self.fields['station'].queryset = Station.objects.filter(pk=kwargs['instance'].station.pk)
        # The following commented code throws AssertionError 'Cannot filter a query once a slice has been taken.'
        # self.fields['price_list'].queryset = PriceList.objects.filter(status=PRICE_LIST_RELEASE)[0:1]
        released_pls = PriceList.objects.filter(status=PRICE_LIST_RELEASE)
        if len(released_pls) > 0:
            self.fields['price_list'].queryset = PriceList.objects.filter(pk=released_pls[0].pk)
            self.fields['price_list'].empty_label = None
        else:
            self.fields['price_list'].queryset = PriceList.objects.none()
        self.fields['station'].empty_label = None
        self.fields['station'].widget.attrs['readonly'] = 'readonly'


class ActivityChargeCatalog(forms.Form):
    activity_items = forms.ModelChoiceField(queryset=ActivityPriceListItem.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        price_list_pk = kwargs.pop('price_list_pk', None)
        super(ActivityChargeCatalog, self).__init__(*args, **kwargs)
        if price_list_pk is not None:
            self.fields['activity_items'].queryset = ActivityPriceListItem.objects.filter(price_list__pk=price_list_pk)


class TimeChargeCatalog(forms.Form):
    time_items = forms.ModelChoiceField(queryset=TimePriceListItem.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        price_list_pk = kwargs.pop('price_list_pk', None)
        super(TimeChargeCatalog, self).__init__(*args, **kwargs)
        if price_list_pk is not None:
            self.fields['time_items'].queryset = TimePriceListItem.objects.filter(price_list__pk=price_list_pk)


class UnitChargeCatalog(forms.Form):
    unit_items = forms.ModelChoiceField(queryset=UnitPriceListItem.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        price_list_pk = kwargs.pop('price_list_pk', None)
        super(UnitChargeCatalog, self).__init__(*args, **kwargs)
        if price_list_pk is not None:
            self.fields['unit_items'].queryset = UnitPriceListItem.objects.filter(price_list__pk=price_list_pk)


class ActivityChargeForm(forms.ModelForm):
    class Meta:
        model = ActivityCharge
        fields = "__all__"
        exclude = ['price_per_unit_override', 'services_active']

    def __init__(self, *args, **kwargs):
        chargelist_pk = kwargs.pop('chargelist_pk', None)
        activitypli_pk = kwargs.pop('activitypli_pk', None)
        super(ActivityChargeForm, self).__init__(*args, **kwargs)
        if chargelist_pk is not None:
            charge_list_queryset = ChargeList.objects.filter(pk=chargelist_pk)
            self.fields['charge_list'].queryset = charge_list_queryset
            self.fields['charge_list'].empty_label = None
            self.fields['charge_list'].widget.attrs['readonly'] = 'readonly'
            self.fields['billing_business'].empty_label = None
            self.fields['billing_business'].queryset = Business.objects.filter(
                stationbusiness__station=charge_list_queryset[0].station)
        if activitypli_pk is not None:
            self.fields['price_list_item'].queryset = ActivityPriceListItem.objects.filter(pk=activitypli_pk)
            self.fields['price_list_item'].empty_label = None
            self.fields['price_list_item'].widget.attrs['readonly'] = 'readonly'


class ActivityChargeUpdateForm(forms.ModelForm):
    class Meta:
        model = ActivityCharge
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ActivityChargeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['charge_list'].queryset = ChargeList.objects.filter(pk=kwargs['instance'].charge_list.pk)
        self.fields['charge_list'].empty_label = None
        self.fields['charge_list'].widget.attrs['readonly'] = 'readonly'
        self.fields['price_list_item'].queryset = ActivityPriceListItem.objects.filter(
            pk=kwargs['instance'].price_list_item.pk)
        self.fields['price_list_item'].empty_label = None
        self.fields['price_list_item'].widget.attrs['readonly'] = 'readonly'


class ActivityChargeActivityForm(forms.ModelForm):
    class Meta:
        model = ActivityChargeActivityCount
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        activitycharge_pk = kwargs.pop('activitycharge_pk', None)
        super(ActivityChargeActivityForm, self).__init__(*args, **kwargs)
        if activitycharge_pk is not None:
            self.fields['activity_charge'].queryset = ActivityCharge.objects.filter(pk=activitycharge_pk)
            self.fields['activity_charge'].empty_label = None
            self.fields['activity_charge'].widget.attrs['readonly'] = 'readonly'


class TimeChargeForm(forms.ModelForm):
    class Meta:
        model = TimeCharge
        fields = "__all__"
        exclude = ['price_per_time_override', 'services_active', 'time_start', 'time_end']

    def __init__(self, *args, **kwargs):
        chargelist_pk = kwargs.pop('chargelist_pk', None)
        timepli_pk = kwargs.pop('timepli_pk', None)
        super(TimeChargeForm, self).__init__(*args, **kwargs)
        if chargelist_pk is not None:
            charge_list_queryset = ChargeList.objects.filter(pk=chargelist_pk)
            self.fields['charge_list'].queryset = charge_list_queryset
            self.fields['charge_list'].empty_label = None
            self.fields['charge_list'].widget.attrs['readonly'] = 'readonly'
            self.fields['billing_business'].empty_label = None
            self.fields['billing_business'].queryset = Business.objects.filter(
                stationbusiness__station=charge_list_queryset[0].station)
        if timepli_pk is not None:
            self.fields['price_list_item'].queryset = TimePriceListItem.objects.filter(pk=timepli_pk)
            self.fields['price_list_item'].empty_label = None
            self.fields['price_list_item'].widget.attrs['readonly'] = 'readonly'


class TimeChargeUpdateForm(forms.ModelForm):
    class Meta:
        model = TimeCharge
        fields = "__all__"
        help_texts = {
            'time_start': 'In UTC time, when does this time charge begin billing? (YYYY-MM-DD HH:MM:SS)',
            'time_end': 'In UTC time, when does this time charge end billing? (YYYY-MM-DD HH:MM:SS)',
        }

    def __init__(self, *args, **kwargs):
        super(TimeChargeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['charge_list'].queryset = ChargeList.objects.filter(pk=kwargs['instance'].charge_list.pk)
        self.fields['charge_list'].empty_label = None
        self.fields['charge_list'].widget.attrs['readonly'] = 'readonly'
        self.fields['price_list_item'].queryset = TimePriceListItem.objects.filter(
            pk=kwargs['instance'].price_list_item.pk)
        self.fields['price_list_item'].empty_label = None
        self.fields['price_list_item'].widget.attrs['readonly'] = 'readonly'


class UnitChargeForm(forms.ModelForm):
    class Meta:
        model = UnitCharge
        fields = "__all__"
        exclude = ['price_per_unit_override', 'services_active']

    def __init__(self, *args, **kwargs):
        chargelist_pk = kwargs.pop('chargelist_pk', None)
        unitpli_pk = kwargs.pop('unitpli_pk', None)
        super(UnitChargeForm, self).__init__(*args, **kwargs)
        if chargelist_pk is not None:
            charge_list_queryset = ChargeList.objects.filter(pk=chargelist_pk)
            self.fields['charge_list'].queryset = charge_list_queryset
            self.fields['charge_list'].empty_label = None
            self.fields['charge_list'].widget.attrs['readonly'] = 'readonly'
            self.fields['billing_business'].empty_label = None
            self.fields['billing_business'].queryset = Business.objects.filter(
                stationbusiness__station=charge_list_queryset[0].station)
        if unitpli_pk is not None:
            self.fields['price_list_item'].queryset = UnitPriceListItem.objects.filter(pk=unitpli_pk)
            self.fields['price_list_item'].empty_label = None
            self.fields['price_list_item'].widget.attrs['readonly'] = 'readonly'


class UnitChargeUpdateForm(forms.ModelForm):
    class Meta:
        model = UnitCharge
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(UnitChargeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['charge_list'].queryset = ChargeList.objects.filter(pk=kwargs['instance'].charge_list.pk)
        self.fields['charge_list'].empty_label = None
        self.fields['charge_list'].widget.attrs['readonly'] = 'readonly'
        self.fields['price_list_item'].queryset = UnitPriceListItem.objects.filter(
            pk=kwargs['instance'].price_list_item.pk)
        self.fields['price_list_item'].empty_label = None
        self.fields['price_list_item'].widget.attrs['readonly'] = 'readonly'
