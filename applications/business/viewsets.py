from applications.business.models import BusinessMembership, Business
from applications.business.serializers import BusinessSerializer, BusinessMembershipSerializer
from rest_framework import viewsets


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business. To search, supply a 'q' get parameter to the url to filter on equipment name.
    """
    serializer_class = BusinessSerializer

    def get_queryset(self):
        queryset = Business.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset


class BusinessMembershipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Business Memberships. To search, supply a 'q' get parameter to the url to filter on service name.
    """
    serializer_class = BusinessMembershipSerializer

    def get_queryset(self):
        queryset = BusinessMembership.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset