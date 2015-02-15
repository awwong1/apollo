from apollo.choices import PRICE_LIST_RELEASE
from applications.charge_list.models import ChargeList
from applications.price_list.models import PriceList
from applications.station.models import Station
from django.forms import ModelForm


class ChargeListForm(ModelForm):
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