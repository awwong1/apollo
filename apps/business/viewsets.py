from apps.business.models import Business
from apps.business.serializers import BusinessSerializer
from rest_framework import viewsets


class BusinessModelViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
