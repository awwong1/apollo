from applications.charge_list.models import ChargeList, ActivityCharge, TimeCharge, UnitCharge
from django.contrib import admin

admin.site.register(ChargeList)
admin.site.register(ActivityCharge)
admin.site.register(TimeCharge)
admin.site.register(UnitCharge)
