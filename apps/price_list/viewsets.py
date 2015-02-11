from apps.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem, \
    PriceListBundle
from apps.price_list.serializers import PriceListSerializer, ActivityPriceListItemSerializer, \
    TimePriceListItemSerializer, UnitPriceListItemSerializer, PriceListBundleSerializer
from rest_framework import mixins, viewsets


class PriceListViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                       mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Price Lists. To search, supply a 'q' get parameter to the url to filter on price list name.
    """
    serializer_class = PriceListSerializer

    def get_queryset(self):
        queryset = PriceList.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.GET['q'])
        return queryset


class ActivityPriceListItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity Price List Items. To search, supply a 'q' get parameter to the url to filter on price list item
    name.
    """
    serializer_class = ActivityPriceListItemSerializer

    def get_queryset(self):
        queryset = ActivityPriceListItem.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.get['q'])
        return queryset


class TimePriceListItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Time Price List Items. To search, supply a 'q' get parameter to the url to filter on price list item
    name.
    """
    serializer_class = TimePriceListItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = TimePriceListItem.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.get['q'])
        return queryset


class UnitPriceListItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Unit Price List Items. To search, supply a 'q' get parameter to the url to filter on price list item
    name.
    """
    serializer_class = UnitPriceListItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = UnitPriceListItem.objects.all()
        if self.request.GET.get('q', None):
            return queryset.filter(name__icontains=self.request.get['q'])
        return queryset


class PriceListBundleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Price List Bundles. To search, supply a 'price_list' get parameter to the url to filter on the price
    list primary key (id).
    """
    serializer_class = PriceListBundleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = PriceListBundle.objects.all()
        if self.request.GET.get('price_list', None):
            return queryset.filter(price_list__pk=self.request.get['price_list'])
        return queryset