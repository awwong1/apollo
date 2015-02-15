from applications.charge_list import views
from django.conf.urls import url, patterns

urlpatterns = patterns(
    '',
    url(r'^create/(?P<station_pk>\d*)/$', views.ChargeListViewCreate.as_view(), name='chargelist_create'),
    url(r'^$', views.ChargeListViewList.as_view(), name='chargelist_list'),
)