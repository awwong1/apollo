from apollo.viewsets import UserViewSet
from apps.business.viewsets import BusinessViewSet, BusinessMembershipViewSet
from apps.equipment.viewsets import EquipmentViewSet, ServiceViewSet
from apps.price_list.viewsets import PriceListViewSet, ActivityPriceListItemViewSet, TimePriceListItemViewSet, \
    UnitPriceListItemViewSet, PriceListBundleViewSet
from apps.station.viewsets import StationViewSet, StationBusinessViewSet
from apps.terms_of_service.viewsets import TermsOfServiceViewSet
from cities_light.contrib.restframework3 import CityModelViewSet, CountryModelViewSet, RegionModelViewSet
from rest_framework.routers import DefaultRouter

# Internal API Definition
router = DefaultRouter()
router.register(r'account/user', UserViewSet, base_name='user')
router.register(r'account/terms_of_service', TermsOfServiceViewSet, base_name='terms-of-service')
router.register(r'business/business', BusinessViewSet, base_name='business')
router.register(r'business/business_membership', BusinessMembershipViewSet, base_name='business-membership')
router.register(r'equipment/equipment', EquipmentViewSet, base_name='equipment')
router.register(r'equipment/service', ServiceViewSet, base_name='service')
router.register(r'station/station', StationViewSet, base_name='station')
router.register(r'station/station_business', StationBusinessViewSet, base_name='station-business')
router.register(r'price_list/price_list', PriceListViewSet, base_name='price-list')
router.register(r'price_list/activity_item', ActivityPriceListItemViewSet, base_name='activity-price-list-item')
router.register(r'price_list/time_item', TimePriceListItemViewSet, base_name='time-price-list-item')
router.register(r'price_list/unit_item', UnitPriceListItemViewSet, base_name='unit-price-list-item')
router.register(r'price_list/bundle', PriceListBundleViewSet, base_name='price-list-bundle')
# Cities light contrib rest framework 3
router.register(r'cities', CityModelViewSet, base_name='cities-light-api-city')
router.register(r'countries', CountryModelViewSet, base_name='cities-light-api-country')
router.register(r'regions', RegionModelViewSet, base_name='cities-light-api-region')