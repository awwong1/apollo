from applications.charge_list.models import ChargeList, ActivityCharge, TimeCharge, UnitCharge, \
    ActivityChargeActivityCount
from django.contrib import admin

admin.site.register(ChargeList)
admin.site.register(ActivityCharge)
admin.site.register(TimeCharge)
admin.site.register(UnitCharge)
admin.site.register(ActivityChargeActivityCount)
