from django.conf.urls import patterns, url
from apps.price_list import views

urlpatterns = patterns(
    '',
    # Price List
    url(r'^$', views.PriceListViewList.as_view(), name='pricelist_list'),
    url(r'^create/$', views.PriceListViewCreate.as_view(), name='pricelist_create'),
    url(r'^(?P<pl_id>\d*)/$', views.PriceListViewDetail.as_view(), name='pricelist_detail'),
    url(r'^(?P<pl_id>\d*)/update/$', views.PriceListViewUpdate.as_view(), name='pricelist_update'),
    url(r'^(?P<pl_id>\d*)/delete/$', views.PriceListViewDelete.as_view(), name='pricelist_delete'),
    # Equipment Relation
    url(r'^(?P<pl_id>\d*)/create/equipment_relation/' +
        '(?P<item_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        views.PriceListItemEquipmentViewCreate.as_view(),
        name='equipment_pricelistitem_create'),
    url('equipment_relation/(?P<pk>\d*)/$', views.PriceListItemEquipmentViewDetail.as_view(),
        name='equipment_pricelistitem_detail'),
    url('equipment_relation/(?P<pk>\d*)/update/$', views.PriceListItemEquipmentViewUpdate.as_view(),
        name='equipment_pricelistitem_update'),
    url('equipment_relation/(?P<pk>\d*)/delete/$', views.PriceListItemEquipmentViewDelete.as_view(),
        name='equipment_pricelistitem_delete'),
    # Service Relation
    url(r'^(?P<pl_id>\d*)/create/service_relation/' +
        '(?P<item_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        views.PriceListItemServiceViewCreate.as_view(),
        name='service_pricelistitem_create'),
    url('service_relation/(?P<pk>\d*)/$', views.PriceListItemServiceViewDetail.as_view(),
        name='service_pricelistitem_detail'),
    url('service_relation/(?P<pk>\d*)/update/$', views.PriceListItemServiceViewUpdate.as_view(),
        name='service_pricelistitem_update'),
    url('service_relation/(?P<pk>\d*)/delete/$', views.PriceListItemServiceViewDelete.as_view(),
        name='service_pricelistitem_delete'),
    # Generic Price List Item Redirection
    url('^(?P<pl_id>\d*)/(?P<item_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        views.PriceListItemRedirect, name='pricelistitem_redirect'),
    # Activity Item
    url(r'^(?P<pl_id>\d*)/create/activity/$', views.ActivityPriceListItemViewCreate.as_view(),
        name='activity_pricelistitem_create'),
    url(r'^activity/(?P<pk>\d*)/$', views.ActivityPriceListItemViewDetail.as_view(),
        name='activity_pricelistitem_detail'),
    url(r'^activity/(?P<pk>\d*)/update/$', views.ActivityPriceListItemViewUpdate.as_view(),
        name='activity_pricelistitem_update'),
    url(r'^activity/(?P<pk>\d*)/delete/$', views.ActivityPriceListItemViewDelete.as_view(),
        name='activity_pricelistitem_delete'),
    # Time Item
    url(r'^(?P<pl_id>\d*)/create/time/$', views.TimePriceListItemViewCreate.as_view(),
        name='time_pricelistitem_create'),
    url(r'^time/(?P<pk>\d*)/$', views.TimePriceListItemViewDetail.as_view(),
        name='time_pricelistitem_detail'),
    url(r'^time/(?P<pk>\d*)/update/$', views.TimePriceListItemViewUpdate.as_view(),
        name='time_pricelistitem_update'),
    url(r'^time/(?P<pk>\d*)/delete/$', views.TimePriceListItemViewDelete.as_view(),
        name='time_pricelistitem_delete'),
    # Unit Item
    url(r'^(?P<pl_id>\d*)/create/unit/$', views.UnitPriceListItemViewCreate.as_view(),
        name='unit_pricelistitem_create'),
    url(r'^unit/(?P<pk>\d*)/$', views.UnitPriceListItemViewDetail.as_view(),
        name='unit_pricelistitem_detail'),
    url(r'^unit/(?P<pk>\d*)/update/$', views.UnitPriceListItemViewUpdate.as_view(),
        name='unit_pricelistitem_update'),
    url(r'^unit/(?P<pk>\d*)/delete/$', views.UnitPriceListItemViewDelete.as_view(),
        name='unit_pricelistitem_delete'),
)