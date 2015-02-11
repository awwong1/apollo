from django.conf.urls import patterns, url
from apps.assets import views

urlpatterns = patterns(
    '',
    url(r'^equipment/$', views.EquipmentViewList.as_view(), name='equipment_list'),
    url(r'^equipment/create/$', views.EquipmentViewCreate.as_view(), name='equipment_create'),
    url(r'^equipment/(?P<pk>\d)/$', views.EquipmentViewDetail.as_view(), name='equipment_detail'),
    url(r'^equipment/(?P<pk>\d)/update/$', views.EquipmentViewUpdate.as_view(), name='equipment_update'),
    url(r'^equipment/(?P<pk>\d)/delete/$', views.EquipmentViewDelete.as_view(), name='equipment_delete'),
)