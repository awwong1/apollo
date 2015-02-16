from applications.station import views
from django.conf.urls import url, patterns

urlpatterns = patterns(
    '',
    # Station Generic Views
    url(r'^create/(?P<business_pk>\d*)/$', views.StationViewCreate.as_view(), name='station_create'),
    url(r'^(?P<pk>\d*)/$', views.StationViewDetail.as_view(), name='station_detail'),
    url(r'^$', views.StationViewList.as_view(), name='station_list'),
    url(r'^(?P<pk>\d*)/update/$', views.StationViewUpdate.as_view(), name='station_update'),
    url(r'^(?P<pk>\d*)/delete/$', views.StationViewDelete.as_view(), name='station_delete'),
    # Station Business Association Generic Views
    url(r'^station_business/(?P<station_pk>\d*)/create/$', views.StationBusinessViewCreate.as_view(),
        name='stationbusiness_create'),
    url(r'station_business/(?P<pk>\d*)/delete/$', views.StationBusinessViewDelete.as_view(),
        name='stationbusiness_delete'),
    # Station Rentals associated generic views
    url(r'^station_rental/(?P<pk>\d*)/update/$', views.StationRentalViewUpdate.as_view(),
        name='stationrental_update'),
    url(r'station_rental/(?P<pk>\d*)/delete/$', views.StationRentalViewDelete.as_view(),
        name='stationrental_delete'),
)