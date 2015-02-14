from applications.station.models import StationBusiness, Station
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
