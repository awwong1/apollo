from apps.business.models import Business
from apps.station.models import Station
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class StationSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="station-detail")

    class Meta:
        model = Station
        read_only_fields = ('id',)


class StationBusinessSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="station-business-detail")
    business = relations.HyperlinkedRelatedField(view_name="business-detail", queryset=Business.objects.all())
    station = relations.HyperlinkedRelatedField(view_name="station-detail", queryset=Station.objects.all())

    class Meta:
        model = Station
        read_only_fields = ('id',)
