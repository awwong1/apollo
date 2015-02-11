from apps.station.models import Station, StationBusiness
from apps.station.serializers import StationSerializer, StationBusinessSerializer
from rest_framework import mixins, viewsets


class StationViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Stations. To search, supply a 'q' get parameter to the url to filter on station name.
    """
    serializer_class = StationSerializer

    def get_queryset(self):
        queryset = Station.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset


class StationBusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Station Businesses. To search, supply a 'q' get parameter to the url to filter on station name.
    """
    serializer_class = StationBusinessSerializer

    def get_queryset(self):
        queryset = StationBusiness.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(station__name__icontains=self.request.GET['q'])
        return queryset