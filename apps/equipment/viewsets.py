from apollo.permissions import IsAdminOrReadOnly
from apps.equipment.models import Equipment, Service
from apps.equipment.serializers import EquipmentSerializer, ServiceSerializer
from rest_framework import viewsets


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Equipment. To search, supply a 'q' get parameter to the url to filter on equipment name.
    """
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Equipment.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset


class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Equipment Services. To search, supply a 'q' get parameter to the url to filter on service name.
    """
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Service.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset