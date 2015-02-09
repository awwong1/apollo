from apps.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem, \
    PriceListBundle
from django.contrib import admin

admin.site.register(PriceList)
admin.site.register(ActivityPriceListItem)
admin.site.register(TimePriceListItem)
admin.site.register(UnitPriceListItem)
admin.site.register(PriceListBundle)