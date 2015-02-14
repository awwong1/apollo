from django.conf.urls import patterns, url
from applications.assets import views

urlpatterns = patterns(
    '',
    url(r'^equipment/$', views.EquipmentViewList.as_view(), name='equipment_list'),
    url(r'^equipment/create/$', views.EquipmentViewCreate.as_view(), name='equipment_create'),
    url(r'^equipment/(?P<pk>\d)/$', views.EquipmentViewDetail.as_view(), name='equipment_detail'),
    url(r'^equipment/(?P<pk>\d)/update/$', views.EquipmentViewUpdate.as_view(), name='equipment_update'),
    url(r'^equipment/(?P<pk>\d)/delete/$', views.EquipmentViewDelete.as_view(), name='equipment_delete'),
    url(r'^service/$', views.ServiceViewList.as_view(), name='service_list'),
    url(r'^service/create/$', views.ServiceViewCreate.as_view(), name='service_create'),
    url(r'^service/(?P<pk>\d)/$', views.ServiceViewDetail.as_view(), name='service_detail'),
    url(r'^service/(?P<pk>\d)/update/$', views.ServiceViewUpdate.as_view(), name='service_update'),
    url(r'^service/(?P<pk>\d)/delete/$', views.ServiceViewDelete.as_view(), name='service_delete'),

)