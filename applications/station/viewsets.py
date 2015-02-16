from applications.station.models import Station, StationBusiness, StationRental
from applications.station.serializers import StationSerializer, StationBusinessSerializer, StationRentalSerializer
from rest_framework import viewsets


class StationViewSet(viewsets.ModelViewSet):
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
    ViewSet for Station Businesses.
    """
    serializer_class = StationBusinessSerializer
    queryset = StationBusiness.objects.all()


class StationRentalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Station Rentals.
    """
    serializer_class = StationRentalSerializer
    queryset = StationRental.objects.all()