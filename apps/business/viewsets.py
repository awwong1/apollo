import re
from apps.business.models import Business, BusinessMembership
from apps.business.permissions import BusinessPermission, BusinessMembershipPermission
from apps.business.serializers import BusinessMembershipSerializer, BusinessSerializer, EditBusinessMembershipSerializer
from rest_framework import viewsets, mixins, status


class BusinessViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Businesses. To define city choices, supply a city parameter (city name, partial) to the url.

    Examples:

    - <a href="/api/business/?city=calgary">/api/business/?city=calgary</a>, city options named *calgary*
    - <a href="/api/business/?city=den">/api/business/?city=den</a>, city options named *den*
    """
    serializer_class = BusinessSerializer
    permission_classes = [BusinessPermission]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        return serializer_class(*args, context=context, **kwargs)

    def get_queryset(self):
        queryset = Business.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Using the rest framework, if a user creates a valid business, auto create the business membership.
        """
        create_ret_val = super(BusinessViewSet, self).create(request, *args, **kwargs)
        if create_ret_val.status_code == status.HTTP_201_CREATED:
            key = int(re.search("([\d]*)/$", create_ret_val.data['url']).group(1))
            BusinessMembership.objects.create(
                business=Business.objects.get(pk=key),
                user=request.user,
                business_administrator=True
            )
        return create_ret_val


class BusinessMembershipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Businesses Memberships. When creating business memberships, supply user, business, and business
    administrator fields. When editing, only business administrator field is toggleable. No business may not remove
    their last administrator.
    """
    serializer_class = BusinessMembershipSerializer
    permission_classes = [BusinessMembershipPermission]

    def get_queryset(self):
        queryset = BusinessMembership.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(business__name__icontains=self.request.GET['q'])
        return queryset

    def get_serializer_class(self):
        if self.request.method not in ('PUT', 'PATCH'):
            return BusinessMembershipSerializer
        return EditBusinessMembershipSerializer