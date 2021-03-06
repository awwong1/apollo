from django.apps import AppConfig, apps
from actstream import registry


class ActivityConfig(AppConfig):
    name = 'applications.activity_config'

    def ready(self):
        registry.register(apps.get_model('auth.user'))  # registers the User (assuming you're using auth.User)
        # Assets Activity Registration
        registry.register(apps.get_model('assets.Equipment'))
        registry.register(apps.get_model('assets.Service'))
        # Business Activity Registration
        registry.register(apps.get_model('business.Business'))
        registry.register(apps.get_model('business.BusinessMembership'))
        # Charge List Activity Registration
        registry.register(apps.get_model('charge_list.ChargeList'))
        registry.register(apps.get_model('charge_list.ActivityCharge'))
        registry.register(apps.get_model('charge_list.TimeCharge'))
        registry.register(apps.get_model('charge_list.UnitCharge'))
        registry.register(apps.get_model('charge_list.ActivityChargeActivityCount'))
        # Price List Activity Registration
        registry.register(apps.get_model('price_list.PriceList'))
        registry.register(apps.get_model('price_list.ActivityPriceListItem'))
        registry.register(apps.get_model('price_list.TimePriceListItem'))
        registry.register(apps.get_model('price_list.UnitPriceListItem'))
        registry.register(apps.get_model('price_list.PriceListItemEquipment'))
        registry.register(apps.get_model('price_list.PriceListItemService'))
        # Station Activity Registration
        registry.register(apps.get_model('station.Station'))
        registry.register(apps.get_model('station.StationBusiness'))
        registry.register(apps.get_model('station.StationRental'))
        # Service Activity Registration
        registry.register(apps.get_model('terms_of_service.TermsOfService'))

