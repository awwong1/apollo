from applications.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem, \
    PriceListItemEquipment, PriceListItemService
from applications.price_list.serializers import PriceListSerializer, ActivityPriceListItemSerializer, \
    TimePriceListItemSerializer, UnitPriceListItemSerializer, PriceListItemEquipmentSerializer, \
    PriceListItemServiceSerializer
from rest_framework import viewsets


class PriceListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Price Lists
    """
    serializer_class = PriceListSerializer
    queryset = PriceList.objects.all()


class ActivityPriceListItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity Price List Items
    """
    serializer_class = ActivityPriceListItemSerializer
    queryset = ActivityPriceListItem.objects.all()


class TimePriceListItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Time Price List Items
    """
    serializer_class = TimePriceListItemSerializer
    queryset = TimePriceListItem.objects.all()


class UnitPriceListItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Unit Price List Items
    """
    serializer_class = UnitPriceListItemSerializer
    queryset = UnitPriceListItem.objects.all()


class PriceListItemEquipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Price list item equipment relations
    """
    serializer_class = PriceListItemEquipmentSerializer
    queryset = PriceListItemEquipment.objects.all()


class PriceListItemServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Price list item service relations
    """
    serializer_class = PriceListItemServiceSerializer
    queryset = PriceListItemService.objects.all()
