from applications.charge_list import views
from django.conf.urls import url, patterns

urlpatterns = patterns(
    '',
    url(r'^create/(?P<station_pk>\d*)/$', views.ChargeListViewCreate.as_view(), name='chargelist_create'),
    url(r'^$', views.ChargeListViewList.as_view(), name='chargelist_list'),
    # Charge Catalog Views
    url(r'^(?P<chargelist_pk>\d*)/create/activitycharge/$', views.ActivityChargeViewCreate.as_view(),
        name='activitycharge_create'),
    url(r'^(?P<chargelist_pk>\d*)/create/timecharge/$', views.TimeChargeViewCreate.as_view(),
        name='timecharge_create'),
    url(r'^(?P<chargelist_pk>\d*)/create/unitcharge/$', views.UnitChargeViewCreate.as_view(),
        name='unitcharge_create'),
)