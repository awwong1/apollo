from applications.assets.models import Equipment, Service
from rest_framework import relations
from rest_framework.serializers import HyperlinkedModelSerializer


class EquipmentSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="equipment-detail")

    class Meta:
        model = Equipment
        read_only_fields = ('id',)


class ServiceSerializer(HyperlinkedModelSerializer):
    url = relations.HyperlinkedIdentityField(view_name="service-detail")
    activate = relations.HyperlinkedRelatedField(
        view_name="equipment-detail", queryset=Equipment.objects.all(),
        help_text="Which equipment does this service activate?"
    )

    class Meta:
        model = Service
        read_only_fields = ('id',)