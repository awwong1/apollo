from apps.terms_of_service.models import TermsOfService
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class TermsOfServiceSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="terms-of-service-detail")

    class Meta:
        model = TermsOfService
        read_only_fields = ('id',)