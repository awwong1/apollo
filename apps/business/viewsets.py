import re
from apps.business.models import Business, BusinessMembership
from apps.business.serializers import BusinessMembershipSerializer, BusinessSerializer
from rest_framework import viewsets, mixins, status


class BusinessViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Businesses. To define city choices, supply a city parameter (city name, partial) to the url.

    Examples:

    - <a href="/api/business/business/?city=calgary">/api/business/business/?city=calgary</a>,
        cities with *calgary* in the name
    - <a href="/api/business/business/?city=den">/api/business/business/?city=den</a>, cities with *den* in the name
    """
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        return serializer_class(*args, context=context, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset


class BusinessMembershipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Businesses Memberships. When creating business memberships, supply user, business, and business
    administrator fields. When editing, only business administrator field is toggleable. No business may not remove
    their last administrator.
    """
    queryset = BusinessMembership.objects.all()
    serializer_class = BusinessMembershipSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.request.GET.get('q', None):
            return queryset.filter(business__name__icontains=self.request.GET['q'])
        return queryset
