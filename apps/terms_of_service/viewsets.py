from apollo.permissions import IsAdminOrReadOnly
from apps.terms_of_service.models import TermsOfService
from apps.terms_of_service.serializers import TermsOfServiceSerializer
from rest_framework import viewsets, mixins


class TermsOfServiceViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                            mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Terms of Services. To search, supply a 'q' get parameter to the url to filter on TOS title.
    """
    serializer_class = TermsOfServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = TermsOfService.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(title__icontains=self.request.GET['q'])
        return queryset