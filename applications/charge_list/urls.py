from applications.charge_list import views
from django.conf.urls import url, patterns

urlpatterns = patterns(
    '',
    url(r'^create/(?P<station_pk>\d*)/$', views.ChargeListViewCreate.as_view(), name='chargelist_create'),
    url(r'^$', views.ChargeListViewList.as_view(), name='chargelist_pendingpayment_list'),
    url(r'^(?P<pk>\d*)/close/$', views.ChargeListViewClose.as_view(), name='chargelist_close'),
    # Charge Catalog Views
    url(r'^(?P<chargelist_pk>\d*)/create/activitycharge/$', views.ActivityChargeViewCreate.as_view(),
        name='activitycharge_create'),
    url(r'^(?P<chargelist_pk>\d*)/create/timecharge/$', views.TimeChargeViewCreate.as_view(),
        name='timecharge_create'),
    url(r'^(?P<chargelist_pk>\d*)/create/unitcharge/$', views.UnitChargeViewCreate.as_view(),
        name='unitcharge_create'),
    # Activity Charge
    url(r'activitycharge/(?P<pk>\d*)/update/$', views.ActivityChargeViewUpdate.as_view(), name='activitycharge_update'),
    url(r'activitycharge/(?P<pk>\d*)/delete/$', views.ActivityChargeViewDelete.as_view(), name='activitycharge_delete'),
    url(r'activitycharge/(?P<activitycharge_pk>\d*)/create/activity/$',
        views.ActivityChargeActivityViewCreate.as_view(), name='activitychargeactivity_create'),
    url(r'activitycharge/activity/(?P<pk>\d*)/$', views.ActivityChargeActivityViewDelete.as_view(),
        name='activitychargeactivity_delete'),
    # Time Charge
    url(r'timecharge/(?P<pk>\d*)/update/$', views.TimeChargeViewUpdate.as_view(), name='timecharge_update'),
    url(r'timecharge/(?P<pk>\d*)/delete/$', views.TimeChargeViewDelete.as_view(), name='timecharge_delete'),
    # Unit Charge
    url(r'unitcharge/(?P<pk>\d*)/update/$', views.UnitChargeViewUpdate.as_view(), name='unitcharge_update'),
    url(r'unitcharge/(?P<pk>\d*)/delete/$', views.UnitChargeViewDelete.as_view(), name='unitcharge_delete'),
)