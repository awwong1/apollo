from apps.business.models import Business, BusinessMembership
from apps.business.serializers import BusinessMembershipSerializer, BusinessSerializer, EditBusinessMembershipSerializer
from rest_framework import viewsets


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Businesses. To define city choices, supply a city parameter (city name, partial) to the url.

    Examples: "/api/business/?city=calgary", "/api/business/?city=den"
    """
    serializer_class = BusinessSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        return serializer_class(*args, context=context, **kwargs)

    def get_queryset(self):
        queryset = Business.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset


class BusinessMembershipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Businesses Memberships.
    """

    def get_queryset(self):
        queryset = BusinessMembership.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(business__name__icontains=self.request.GET['q'])
        return queryset

    def get_serializer_class(self):
        if self.request.method not in ('PUT', 'PATCH'):
            return BusinessMembershipSerializer
        return EditBusinessMembershipSerializer