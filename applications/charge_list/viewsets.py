from applications.charge_list.models import ChargeList, ActivityCharge, ActivityChargeActivityCount, TimeCharge, \
    UnitCharge
from applications.charge_list.serializers import ChargeListSerializer, ActivityChargeSerializer, \
    ActivityChargeActivityCountSerializer, TimeChargeSerializer, UnitChargeSerializer
from rest_framework import viewsets


class ChargeListViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Charge Lists
    """
    serializer_class = ChargeListSerializer
    queryset = ChargeList.objects.all()


class ActivityChargeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity Charges
    """
    serializer_class = ActivityChargeSerializer
    queryset = ActivityCharge.objects.all()


class ActivityChargeActivityCountViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity Charge Activity Counts
    """
    serializer_class = ActivityChargeActivityCountSerializer
    queryset = ActivityChargeActivityCount.objects.all()


class TimeChargeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Time Charges
    """
    serializer_class = TimeChargeSerializer
    queryset = TimeCharge.objects.all()


class UnitChargeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Unit Charges
    """
    serializer_class = UnitChargeSerializer
    queryset = UnitCharge.objects.all()
