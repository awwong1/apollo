from apollo.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for built in Django User model.
    Read only, as user logic is delegated to Django All Auth.
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(username__icontains=self.request.get['q'])
        return queryset