from apps.business.models import Business
from apps.business.serializers import BusinessSerializer
from rest_framework import viewsets


class BusinessModelViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    def get_queryset(self):
        queryset = Business.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])