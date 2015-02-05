from django.contrib.auth.models import User
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class UserSerializer(HyperlinkedModelSerializer):
    """
    Serializer for built in Django User model.
    """
    url = relations.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'email',)