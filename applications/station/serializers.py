from applications.station.models import Station, StationBusiness
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class StationSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="station-detail")

    class Meta:
        model = Station


class StationBusinessSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="station-business-detail")
    business = relations.HyperlinkedRelatedField(view_name="business-detail", read_only=True)
    station = relations.HyperlinkedRelatedField(view_name="station-detail", read_only=True)

    class Meta:
        model = StationBusiness


class StationRentalSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="station-rental-detail")
    station = relations.HyperlinkedRelatedField(view_name="station-detail", read_only=True)
    equipment = relations.HyperlinkedRelatedField(view_name="equipment-detail", read_only=True)