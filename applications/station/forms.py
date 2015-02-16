from applications.assets.models import Equipment
from applications.station.models import StationBusiness, Station, StationRental
from django.forms import ModelForm


class StationBusinessForm(ModelForm):
    class Meta:
        model = StationBusiness
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        station_pk = kwargs.pop('station_pk', None)
        super(StationBusinessForm, self).__init__(*args, **kwargs)
        if station_pk is not None:
            self.fields['station'].queryset = Station.objects.filter(pk=station_pk)
        elif kwargs.get('instance', None) is not None:
            self.fields['station'].queryset = Station.objects.filter(pk=kwargs['instance'].station.pk)
        self.fields['business'].empty_label = None
        self.fields['station'].empty_label = None
        self.fields['station'].widget.attrs['readonly'] = 'readonly'


class StationRentalForm(ModelForm):
    class Meta:
        model = StationRental
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(StationRentalForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            self.fields['station'].queryset = Station.objects.filter(pk=instance.station.pk)
            self.fields['equipment'].queryset = Equipment.objects.filter(pk=instance.equipment.pk)
            self.fields['station'].empty_label = None
            self.fields['equipment'].empty_label = None
            self.fields['station'].widget.attrs['readonly'] = 'readonly'
            self.fields['equipment'].widget.attrs['readonly'] = 'readonly'
