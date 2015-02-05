from apollo.viewsets import UserViewSet
from apps.business.viewsets import BusinessViewSet, BusinessMembershipViewSet
from cities_light.contrib.restframework3 import CityModelViewSet, CountryModelViewSet, RegionModelViewSet
from rest_framework.routers import DefaultRouter

# Internal API Definition
router = DefaultRouter()
router.register(r'business', BusinessViewSet, base_name='business')
router.register(r'business_membership', BusinessMembershipViewSet, base_name='business-membership')
# Built in user model
router.register(r'user', UserViewSet, base_name='user')
# Cities light contrib rest framework 3
router.register(r'cities', CityModelViewSet, base_name='cities-light-api-city')
router.register(r'countries', CountryModelViewSet, base_name='cities-light-api-country')
router.register(r'regions', RegionModelViewSet, base_name='cities-light-api-region')